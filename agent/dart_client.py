import time
import requests

BASE = "https://opendart.fss.or.kr/api"

class DartClient:
    def __init__(self, key: str):
        if not key:
            raise ValueError("DART_API_KEY is not set. Add it to GitHub Actions Secrets.")
        self.key = key
        self.session = requests.Session()

    def get(self, path: str, params: dict, retries: int = 4) -> dict:
        p = dict(params)
        p["crtfc_key"] = self.key
        last = None
        for attempt in range(retries):
            try:
                r = self.session.get(BASE + path, params=p, timeout=60)
                r.raise_for_status()
                data = r.json()
                if data.get("status") == "020" and attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                return data
            except Exception as exc:
                last = exc
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"OpenDART request failed: {last}")

    def financials(self, corp: str, year: int, report_code: str, fs_div: str = "CFS") -> dict:
        return self.get("/fnlttSinglAcntAll.json", {
            "corp_code": corp,
            "bsns_year": str(year),
            "reprt_code": report_code,
            "fs_div": fs_div,
        })
