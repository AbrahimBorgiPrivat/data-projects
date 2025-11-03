import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional, Callable
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

class WebScraper:
    FieldRule = Dict[str, Any]
    Rule = Dict[str, Any]

    def __init__(
        self,
        base_url: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        use_js: bool = False
    ):
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        self.soup = None
        self.use_js = use_js

    def load_page(
        self,
        url: Optional[str] = None,
        wait_selector: Optional[str] = None,
        click_selector: Optional[str] = None,
        click_until_gone: bool = False
    ) -> None:
        target_url = url or self.base_url
        if not target_url:
            raise ValueError("No URL provided to load_page()")

        if self.use_js:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(target_url, wait_until="networkidle")

                if wait_selector:
                    try:
                        page.wait_for_selector(wait_selector, timeout=10000)
                    except Exception:
                        pass

                if click_selector:
                    while True:
                        try:
                            button = page.query_selector(click_selector)
                            if not button:
                                break
                            button.click()
                            page.wait_for_timeout(1000)
                            if not click_until_gone:
                                break
                        except Exception:
                            break

                html = page.content()
                browser.close()
            self.soup = BeautifulSoup(html, "html.parser")
        else:
            response = requests.get(target_url, headers=self.headers, timeout=30)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")

        if not self.base_url:
            self.base_url = target_url

    @staticmethod
    def _apply_regex(value: Optional[str], pattern: Optional[str]) -> Optional[str]:
        if value is None or not pattern:
            return value
        m = re.search(pattern, value)
        return m.group(1) if m else None

    def _get_field_value(self, el, field: FieldRule) -> Any:
        source = field.get("source", "text")
        regex = field.get("regex")
        join_base = field.get("join_base", False)
        transform: Optional[Callable[[Any], Any]] = field.get("transform")

        if source == "text":
            val = el.get_text(strip=True)
        elif source == "html":
            val = str(el)
        elif source == "attr":
            key = field.get("key")
            val = el.get(key) if key else None
        else:
            val = None

        val = self._apply_regex(val, regex)

        if isinstance(val, str) and join_base:
            val = urljoin(self.base_url or "", val)

        if transform and val is not None:
            try:
                val = transform(val)
            except Exception:
                pass

        return val

    def extract_one(self, selector: str, fields: List[FieldRule]) -> Optional[Dict[str, Any]]:
        if not self.soup:
            raise RuntimeError("No HTML loaded. Call load_page() first.")
        el = self.soup.select_one(selector)
        if not el:
            return None
        out: Dict[str, Any] = {}
        for f in fields:
            out[f["name"]] = self._get_field_value(el, f)
        return out

    def extract_many(self, selector: str, fields: List[FieldRule]) -> List[Dict[str, Any]]:
        if not self.soup:
            raise RuntimeError("No HTML loaded. Call load_page() first.")
        out: List[Dict[str, Any]] = []
        for el in self.soup.select(selector):
            row: Dict[str, Any] = {}
            for f in fields:
                row[f["name"]] = self._get_field_value(el, f)
            out.append(row)
        return out