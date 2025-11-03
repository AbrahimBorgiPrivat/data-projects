import json
from libraries.classes.webscraper import WebScraper
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm

def scrape_items_from_json(
        res_path: Path,
        project: str,
        input_file: str,
        output_file: str,
        selector: str,
        fields: List[Dict[str, Any]],
        wait_selector: Optional[str] = None,
        use_js: bool = True,
        id_keys: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        
    path_json = res_path / project / "json"
    file_path = path_json / input_file
    out_path = path_json / output_file

    if not file_path.exists():
        raise FileNotFoundError(f"Could not find file: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results: List[Dict[str, Any]] = []

    for record in tqdm(data, desc=f"Scraping {input_file} → {output_file}"):
        url = record.get("url")
        if not url:
            continue

        scraper = WebScraper(base_url=url, use_js=use_js)
        scraper.load_page(wait_selector=wait_selector)

        scraped = scraper.extract_many(selector, fields)

        for item in scraped:
            merged = {**{k: record.get(k) for k in (id_keys or [])}, **item}
            results.append(merged)

    path_json.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Saved {len(results)} records → {out_path}")
    return results

