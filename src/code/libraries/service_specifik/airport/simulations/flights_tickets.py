from __future__ import annotations
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tqdm import tqdm
from libraries.utils.simulations import _binomial
from libraries.packages.upsert_data import upsert_insert, build_client

def _occupancy_prob(dt: datetime) -> float:
    wd = dt.weekday() 
    hour = dt.hour
    base_map = {0: 0.82, 1: 0.83, 2: 0.84, 3: 0.85, 4: 0.88, 5: 0.78, 6: 0.90}
    base = base_map.get(wd, 0.82)
    adj = 0.0
    if 6 <= hour <= 9:     
        adj += 0.1
    if 16 <= hour <= 20:   
        adj += 0.1
    if 11 <= hour <= 14:  
        adj -= 0.02
    if hour >= 22 or hour <= 5:  
        adj -= 0.04
    return max(0.75, min(0.98, base + adj))

def _sample_checkin_time(dt_sched_local: datetime, check_in_type: str) -> datetime:
    if check_in_type == "online":
        earliest = dt_sched_local - timedelta(hours=24)
        latest = dt_sched_local - timedelta(hours=2)
        delta_s = (latest - earliest).total_seconds()
        return earliest + timedelta(seconds=random.uniform(0, delta_s))
    else:
        mean = 2 * 3600
        std = 40 * 60
        for _ in range(10):
            secs = random.gauss(mean, std)
            if 30*60 <= secs <= 6*3600:
                return dt_sched_local - timedelta(seconds=secs)
        secs = max(30*60, min(6*3600, random.gauss(mean, std)))
        return dt_sched_local - timedelta(seconds=secs)

def _sample_security_time(dt_sched_local: datetime, 
                          checkin_time: datetime) -> Optional[datetime]:
    upper = dt_sched_local - timedelta(minutes=20)
    earliest_allowed = dt_sched_local - timedelta(hours=4)
    lower = max(checkin_time, earliest_allowed)
    if lower >= upper:
        candidate = dt_sched_local - timedelta(minutes=30)
        return candidate if candidate > checkin_time else None
    delta_s = (upper - lower).total_seconds()
    return lower + timedelta(seconds=random.uniform(0, delta_s))

def simulate_tickets(upsert_runtime_vars: dict) -> List[Dict[str, object]]:
    client = build_client(db_name=upsert_runtime_vars['client']['db_name'],
                            username=upsert_runtime_vars['client']['username'],
                            password=upsert_runtime_vars['client']['password'],
                            server = upsert_runtime_vars['client']['server'],
                            port=upsert_runtime_vars['client']['port'],
                            db_type=upsert_runtime_vars['client']['db_type'])
    passports = client.get_data('SELECT passport_number FROM cph_airport.passports')     
    flights = client.get_data('''SELECT transaction_id,
                                        status,
                                        scheduled_local,
                                        seats
                                FROM cph_airport.flights fl
                                JOIN cph_airport.aircraft_models am ON am.aircraft_model = fl.aircraft_model''') 
    passport_ids = [p["passport_number"] for p in passports if "passport_number" in p]
    if not passport_ids:
        return []
    last_flight_at: Dict[str, datetime] = {pid: datetime.min for pid in passport_ids}
    out: List[Dict[str, object]] = []
    for fl in tqdm(flights):
        tx_id: str = str(fl["transaction_id"])
        status: str = str(fl["status"])
        dt_sched: datetime = fl["scheduled_local"]  
        seats: int = int(fl["seats"])
        p_occ = _occupancy_prob(dt_sched)
        seats_sold = min(seats, _binomial(seats, p_occ))
        seat_numbers = random.sample(range(1, seats + 1), k=seats_sold)
        chosen_for_flight: set[str] = set()
        assigned = 0
        attempts = 0
        max_attempts = seats_sold * 25 if seats_sold > 0 else 0

        def eligible(pid: str) -> bool:
            return (dt_sched - last_flight_at.get(pid, datetime.min)) >= timedelta(days=upsert_runtime_vars["cooldown_days"])
        
        while assigned < seats_sold and attempts < max_attempts:
            attempts += 1
            pid = random.choice(passport_ids)
            if pid in chosen_for_flight:
                continue
            if not eligible(pid):
                continue
            seat_no = seat_numbers[assigned]
            chosen_for_flight.add(pid)
            last_flight_at[pid] = dt_sched
            check_in_type = "online" if random.random() < 0.75 else "onsite"
            checkin_dt = _sample_checkin_time(dt_sched, check_in_type)
            sec_dt = _sample_security_time(dt_sched, checkin_dt) if status.lower() == "departed" else None
            out.append({
                "unique_id": f"{tx_id}-S:{seat_no}",
                "transaction_id": tx_id,
                "seat_number": seat_no,
                "passport_number": pid,
                "check_in_type": check_in_type,
                "checkin_time": checkin_dt.isoformat(timespec="seconds"),
                "passed_security_time": None if sec_dt is None else sec_dt.isoformat(timespec="seconds"),
            })
            assigned += 1
        if upsert_runtime_vars["force_fill"] and assigned < seats_sold:
            remaining = seats_sold - assigned
            pool = [pid for pid in passport_ids if pid not in chosen_for_flight]
            for i in range(remaining):
                pid = random.choice(pool) if pool else random.choice(passport_ids)
                seat_no = seat_numbers[assigned]
                chosen_for_flight.add(pid)
                last_flight_at[pid] = dt_sched  # still update latest

                check_in_type = "online" if random.random() < 0.75 else "onsite"
                checkin_dt = _sample_checkin_time(dt_sched, check_in_type)
                sec_dt = _sample_security_time(dt_sched, checkin_dt) if status.lower() == "departed" else None

                out.append({
                    "unique_id": f"{tx_id}-S:{seat_no}",
                    "transaction_id": tx_id,
                    "seat_number": seat_no,
                    "passport_number": pid,
                    "check_in_type": check_in_type,
                    "checkin_time": checkin_dt.isoformat(timespec="seconds"),
                    "passed_security_time": None if sec_dt is None else sec_dt.isoformat(timespec="seconds"),
                })
                assigned += 1
    upsert_insert(client=client,
            upsert_runtime_vars=upsert_runtime_vars,
            new_data=out
        )
    return out

