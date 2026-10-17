"""
Load the Varve Data free sample.

The first call downloads the sample zip from varvedata.com into ./data (about 1 MB) and
unpacks it; later calls read the local copy. Delete ./data to fetch a fresh one: the
Events and Corporate Actions files cover the last 7 / 90 days and change every weekday.

    from varve_sample import load
    q = load("fundamentals_quarterly")
"""

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

SAMPLE_URL = "https://varvedata.com/downloads/varve_data_free_sample.zip"
DATA = Path(__file__).resolve().parent / "data"

FILES = {
    "fundamentals_quarterly": "varve_fundamentals_quarterly_sample.csv",
    "fundamentals_annual": "varve_fundamentals_annual_sample.csv",
    "fundamentals_companies": "varve_fundamentals_companies_sample.csv",
    "ticker_history": "varve_fundamentals_ticker_history_sample.csv",
    "company_names": "varve_fundamentals_company_names_sample.csv",
    "company_lineage": "varve_fundamentals_company_lineage_sample.csv",
    "earnings_releases": "varve_events_earnings_releases_last7days.csv",
    "current_reports": "varve_events_current_reports_last7days.csv",
    "ownership_filings": "varve_events_ownership_filings_last7days.csv",
    "late_filings": "varve_events_late_filings_last7days.csv",
    "offerings": "varve_events_offerings_last7days.csv",
    "insider_transactions": "varve_events_insider_transactions_last7days.csv",
    "splits": "varve_corporate_actions_splits_sample.csv",
    "listing_events": "varve_corporate_actions_listing_events_last90days.csv",
}

DATES = {"period_end", "filed", "first_filed", "last_filed", "trans_date", "report_date",
         "announced", "record_date", "payable_date", "effective_date", "ex_date",
         "valid_from", "valid_to", "last_seen", "link_date"}


def download(force=False):
    """fetch and unpack the sample unless it is already in ./data"""
    if not force and all((DATA / f).exists() for f in FILES.values()):
        return DATA
    DATA.mkdir(exist_ok=True)
    r = requests.get(SAMPLE_URL, timeout=60, headers={"User-Agent": "varve-examples"})
    r.raise_for_status()
    zipfile.ZipFile(io.BytesIO(r.content)).extractall(DATA)
    return DATA


def load(table):
    """one sample table as a DataFrame, with date columns parsed"""
    if table not in FILES:
        raise KeyError(f"unknown table {table!r}; choose from {', '.join(FILES)}")
    path = download() / FILES[table]
    df = pd.read_csv(path, low_memory=False)
    for col in DATES & set(df.columns):
        df[col] = pd.to_datetime(df[col], errors="coerce")
    if "accepted_et" in df.columns:
        df["accepted_et"] = pd.to_datetime(df["accepted_et"], errors="coerce")
    return df
