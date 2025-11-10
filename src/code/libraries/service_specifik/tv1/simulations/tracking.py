from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, date, time
from typing import Dict, List, Any, Optional, Tuple
from tqdm import tqdm
from libraries.packages.upsert_data import upsert_insert, build_client

def _dt_range(d_from: date, d_to: date):
    d = d_from
    while d <= d_to:
        yield d
        d += timedelta(days=1)

def _is_weekend(d: date) -> bool:
    return d.weekday() >= 5

def _parse_time_hhmm(t: str) -> time:
    hh, mm = [int(x) for x in t.split(":")]
    return time(23, 59, 59) if hh == 24 else time(hh, mm)

def _pick_weighted(items):
    total = sum(max(0.0, w) for _, w in items)
    if total <= 0: 
        return items[0][0]
    r, acc = random.random() * total, 0
    for payload, w in items:
        acc += max(0.0, w)
        if r <= acc:
            return payload
    return items[-1][0]

def _sample_minutes(dist: Dict[str, float]) -> int:
    mean, std = float(dist.get("mean", 60)), float(dist.get("std", 15))
    vmin, vmax = float(dist.get("min", 10)), float(dist.get("max", 180))
    for _ in range(8):
        x = random.gauss(mean, std)
        if vmin <= x <= vmax:
            return int(round(x))
    return int(round(max(vmin, min(vmax, mean))))

def _weighted_bool(p: float) -> bool:
    return random.random() < max(0.0, min(1.0, p))

def _rand_dt_between(d: date, t_start: time, t_end: time) -> datetime:
    dt_start = datetime.combine(d, t_start)
    dt_end = datetime.combine(d, t_end)
    delta_s = int((dt_end - dt_start).total_seconds())
    return dt_start + timedelta(seconds=random.randint(0, max(0, delta_s)))


def generate_streaming_behavior(upsert_runtime_vars: dict) -> List[Dict[str, Any]]:
    client = build_client(
        db_name=upsert_runtime_vars["client"]["db_name"],
        username=upsert_runtime_vars["client"]["username"],
        password=upsert_runtime_vars["client"]["password"],
        server=upsert_runtime_vars["client"]["server"],
        port=upsert_runtime_vars["client"]["port"],
        db_type=upsert_runtime_vars["client"]["db_type"],
    )
    schema = upsert_runtime_vars.get("schema", "tv_one")
    users = client.get_data(f"SELECT user_id, segment_id FROM {schema}.users ORDER BY user_id;")
    if not users:
        return []
    seg_rows = client.get_data(f"SELECT * FROM {schema}.segmentation ORDER BY segment_id;")
    segments = {}
    def _coerce(obj): return json.loads(obj) if isinstance(obj, str) else obj
    for r in seg_rows:
        sid = int(r["segment_id"])
        segments[sid] = {
            "kids_content_share": float(r["kids_content_share"]),
            "preferred_platform_weights": _coerce(r["preferred_platform_weights"]),
            "weekday_windows": _coerce(r["weekday_time_windows"]),
            "weekend_windows": _coerce(r["weekend_time_windows"]),
            "avg_daily_minutes_weekday": _coerce(r["avg_daily_minutes_weekday"]),
            "avg_daily_minutes_weekend": _coerce(r["avg_daily_minutes_weekend"]),
        }
    ep_rows = client.get_data(f"""
        SELECT episode_id, 
                season_id, 
                episode_nr,
               EXTRACT(EPOCH FROM duration_interval) AS duration_s
        FROM {schema}.episodes_view;
    """)
    episodes_by_season: Dict[int, List[Dict[str, Any]]] = {}
    for e in ep_rows:
        sid = int(e["season_id"])
        episodes_by_season.setdefault(sid, []).append(e)
    for sid in episodes_by_season:
        episodes_by_season[sid].sort(key=lambda x: x["episode_nr"])

    if (seed := upsert_runtime_vars.get("seed")) is not None:
        random.seed(seed)
    d_from = datetime.fromisoformat(upsert_runtime_vars["date_from"]).date()
    d_to = datetime.fromisoformat(upsert_runtime_vars["date_to"]).date()
    next_tracking_id = 1
    def _tid():
        nonlocal next_tracking_id
        t = next_tracking_id
        next_tracking_id += 1
        return t

    out = []
    resume_state: Dict[int, Tuple[int, int, float]] = {}
    for the_day in tqdm(_dt_range(d_from, d_to)):
        is_weekend = _is_weekend(the_day)
        for u in users:
            uid, seg = u["user_id"], segments.get(int(u["segment_id"]))
            if not seg: continue
            windows = seg["weekend_windows"] if is_weekend else seg["weekday_windows"]
            for w in windows:
                if not _weighted_bool(float(w["weight"])): 
                    continue
                s_start = _rand_dt_between(the_day, _parse_time_hhmm(w["start"]), _parse_time_hhmm(w["end"]))
                sess_id, platform = _tid(), _pick_weighted(list(seg["preferred_platform_weights"].items()))
                out.append({
                    "tracking_id": sess_id,
                    "tracking_time": s_start.isoformat(timespec="seconds"),
                    "type": "Session starts",
                    "session_id": sess_id,
                    "target_id": None,
                    "platform": platform,
                    "context": json.dumps({"context": "started session"}),
                    "user_id": uid
                })
                budget_s = _sample_minutes(seg["avg_daily_minutes_weekend" if is_weekend else "avg_daily_minutes_weekday"]) * 60
                pointer = resume_state.get(uid)
                if pointer is None:
                    sid = random.choice(list(episodes_by_season.keys()))
                    idx, rem = 0, 0
                else:
                    sid, idx, rem = pointer
                eps = episodes_by_season.get(sid)
                now, remain_budget = s_start, budget_s
                while remain_budget > 0 and eps and idx < len(eps):
                    ep = eps[idx]
                    epid, dur = int(ep["episode_id"]), float(ep["duration_s"] or 0)
                    remaining_episode_time = dur - rem
                    playtime = min(remain_budget, remaining_episode_time)
                    e_tid = _tid()
                    end_t = now + timedelta(seconds=playtime)
                    finished = (playtime + rem) >= dur
                    out.append({
                        "tracking_id": e_tid,
                        "tracking_time": now.isoformat(timespec="seconds"),
                        "type": "Episode starts",
                        "session_id": sess_id,
                        "target_id": epid,
                        "platform": platform,
                        "context": json.dumps({
                            "start_time": now.isoformat(timespec="seconds"),
                            "end_time": end_t.isoformat(timespec="seconds"),
                            "finished": finished
                        }),
                        "user_id": uid
                    })
                    now += timedelta(seconds=playtime)
                    remain_budget -= playtime
                    if finished:
                        idx += 1
                        rem = 0
                        if idx >= len(eps) and remain_budget > 0:
                            sid = random.choice(list(episodes_by_season.keys()))
                            eps = episodes_by_season.get(sid, [])
                            idx, rem = 0, 0
                            continue  # immediately start new episode
                    else:
                        rem += playtime
                        break
                resume_state[uid] = (sid, idx, rem)

    upsert_insert(client=client, upsert_runtime_vars=upsert_runtime_vars, new_data=out)
    return out


from libraries.utils import env

if __name__ == "__main__":
    from pprint import pprint

    upsert_runtime_vars = {
        "client": {
            "db_name": env.TV_OME_DB,
            "username": env.POSTGRES_USERNAME,
            "password": env.POSTGRES_PASSWORD,
            "server": env.POSTGRES_HOST,
            "port": env.POSTGRES_PORT,               # or 5432 if default
            "db_type": env.DB_TYPE
        },
        "schema": "tv_one",
        # --- simulation parameters ---
        "number_of_simulations": 2000,   # soft limit, not strict
        "date_from": "2025-01-05",
        "date_to": "2025-01-07",
        "seed": 42
    }

    print("[INFO] Starting test simulation for streaming behavior...")
    result = generate_streaming_behavior(upsert_runtime_vars)

    print(f"\n[INFO] Simulation finished — {len(result)} tracking events generated.\n")
    print("[INFO] Showing first 10 rows:\n")
    pprint(result[:10])
