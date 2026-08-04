# Governed KPI definitions

- **Total giving:** sum of positive gift amounts in cleaned records.
- **Unique donors:** distinct constituent IDs with at least one cleaned gift.
- **Total gifts:** distinct cleaned gift IDs.
- **Average / median / largest gift:** standard descriptive statistics over cleaned gift amounts.
- **Fiscal year:** calendar year plus one for gifts dated July through December; January through June use the calendar year.
- **New donor:** donor whose first observed giving fiscal year is the latest fiscal year.
- **Retained donor:** donor who gave in both the latest and immediately prior fiscal years.
- **Recovered donor:** latest-year donor who skipped the prior year but gave in an earlier year.
- **LYBUNT:** donor who gave last fiscal year but not the latest year.
- **SYBUNT:** donor with any prior-year gift but none in the latest year.
- **Retention rate:** retained donors divided by prior-year donors.
- **Year-over-year change:** `(latest / prior) - 1` for giving and distinct donors.
- **Top-10% concentration:** share of total giving supplied by the highest-giving 10% of donors, rounded up to one donor.
- **Data-quality score:** one minus detected critical exception count divided by received rows, bounded at zero.

Metrics reflect the observed upload only; they are not forecasts or external benchmarks.

