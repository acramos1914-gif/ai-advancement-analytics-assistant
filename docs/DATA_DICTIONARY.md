# Data dictionary

## Required columns

| Column | Meaning |
|---|---|
| `constituent_id` | CRM contact/account identifier used only for deterministic donor counting |
| `constituent_name` | Display name; never sent to AI |
| `gift_id` | Unique transaction identifier |
| `gift_date` | Gift date parseable by pandas |
| `gift_amount` | Positive numeric amount; currency symbols and commas are accepted |

## Optional columns

`constituent_type`, `preferred_class_year`, `city`, `state`, `email`, `gift_type`, `campaign`, `designation`, and `gift_officer` enrich segment analysis. Missing dimensions become `Unknown` or `Unassigned` where appropriate.

Files must be CSV or XLSX and no larger than 25 MB. Rows with invalid dates/amounts, missing IDs, nonpositive amounts, or duplicate gift IDs are excluded.

