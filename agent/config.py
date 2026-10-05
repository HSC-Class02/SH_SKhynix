import os

CORP_CODE = os.getenv("DART_CORP_CODE", "00164779")
STOCK_CODE = "000660"
API_KEY = os.getenv("DART_API_KEY", "")
START_YEAR = int(os.getenv("START_YEAR", "2010"))
END_YEAR = int(os.getenv("END_YEAR", "")) if os.getenv("END_YEAR") else None

REPORT_CODES = {
    "11011": "annual",
    "11012": "half-year",
    "11013": "quarterly-Q1",
    "11014": "quarterly-Q3",
}

REPORT_LABELS = {
    "11011": "Annual",
    "11012": "Half-year",
    "11013": "Q1",
    "11014": "Q3 (9M cumulative)",
}
