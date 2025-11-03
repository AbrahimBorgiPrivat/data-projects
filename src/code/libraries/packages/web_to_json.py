from libraries.utils.path_config import RES_PATH
from libraries.classes.webscraper import WebScraper
import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

def get_all_seasons():
    path_json = RES_PATH / 'tv1' / 'json' 
    file_path = path_json / 'drtv_programs.json'
    out_path = path_json / "drtv_seasons.json"
    if not file_path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    seasons: List[Dict[str, Any]] = []
    for show in tqdm(data):
        program_id = show.get("program_id")
        url = show.get("url")
        n_seasons = show.get("seasons", 1)
        if n_seasons == 1:
            seasons.append({'program_id': program_id,
                            'season_id': program_id,
                            'season': show['seasons'],
                            'url': url})
        else:
            scraper = WebScraper(base_url=url, use_js=True)
            scraper.load_page(wait_selector="div.d1-drtv-season-list__item")
            selector = "div.d1-drtv-season-list__item a.d1-drtv-season-list__link"
            fields = [
                {
                    "name": "season_id",
                    "source": "attr",
                    "key": "href",
                    "regex": r"_(\d+)(?:\D|$)",
                    "transform": lambda s: int(s) if s else None,
                },
                {
                    "name": "season",
                    "source": "text",
                    "regex": r"(\d+)$",
                    "transform": lambda s: int(s) if s else None,
                },
                {
                    "name": "url",
                    "source": "attr",
                    "key": "href",
                    "join_base": True,
                },
            ]
            show_seasons = scraper.extract_many(selector, fields)
            for s in show_seasons:
                seasons.append({
                    "program_id": program_id,
                    "season_id": s.get("season_id"),
                    "season": s.get("season"),
                    "url": s.get("url"),
                })
    path_json.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(seasons, f, ensure_ascii=False, indent=2)
    return seasons


