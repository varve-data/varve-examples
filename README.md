# Varve Data examples

Python notebooks showing how to use [Varve Data](https://varvedata.com): point-in-time
US company fundamentals and SEC filing events, built directly from EDGAR.

They run on the **free sample** (25 companies with full quarterly and annual history, plus
the last 7 days of filing events), which the code downloads from varvedata.com on first run.

| Notebook | What it shows |
|---|---|
| [01 · Quickstart](notebooks/01_quickstart.ipynb) | Load the sample, look up a company by CIK, chart revenue and margins, compute trailing-twelve-month figures |
| [02 · Point-in-time](notebooks/02_point_in_time.ipynb) | Why lining data up by `period_end` leaks the future (55% of company-months in the sample), and the `merge_asof`-on-`filed` pattern that fixes it |
| [03 · Identifiers and delistings](notebooks/03_identifiers_and_delistings.ipynb) | Tickers that point to two companies (BBBY, GOOGL, DIS), renamed tickers, and companies that no longer exist (SVB, Bed Bath & Beyond, Twitter) |
| [04 · Events](notebooks/04_events.ipynb) | Earnings release times to the second, insider buying, 13D activist stakes, late filings, 8-K items |

## Run them

```bash
git clone https://github.com/OWNER/varve-examples.git
cd varve-examples
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/
```

Or just read them here on GitHub: the outputs are saved in each notebook.

Use the loader in your own code:

```python
from varve_sample import load

q = load("fundamentals_quarterly")    # see FILES in varve_sample.py for every table
```

The Events files cover a rolling 7 days, so their numbers change with each download.
Delete `data/` to fetch a fresh sample.

## The full data

The sample is a slice of the paid datasets:

* **Varve Fundamentals**: 16,000+ US companies since 2009, including delisted ones;
  every figure with the date it became public, and every restatement kept as its own
  version.
* **Varve Events**: earnings release times, 8-Ks, insider trades, 13D/G, offerings and
  late filings, updated every weekday evening, with Corporate Actions (splits and
  listings/delistings).

Pricing, documentation and the methodology guide: [varvedata.com](https://varvedata.com).

## Licence

The code in this repository is MIT-licensed (see [LICENSE](LICENSE)). The data, including
the free sample, is not part of this repository and is covered by the
[Varve Data terms](https://varvedata.com/terms.html): use it for your own analysis, but
don't redistribute it. Attribution ("Source: Varve Data") is appreciated when you publish
results.
