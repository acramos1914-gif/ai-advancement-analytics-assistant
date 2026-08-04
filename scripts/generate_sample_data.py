"""Generate a reproducible, entirely fictional Salesforce-style gift export."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 1914
ROOT = Path(__file__).resolve().parents[1]


def generate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    n_constituents, n_donors, n_gifts = 5000, 1500, 8000
    first = np.array(["Avery", "Jordan", "Morgan", "Riley", "Cameron", "Taylor", "Casey", "Quinn", "Skyler", "Reese"])
    last = np.array(["Adams", "Brooks", "Carter", "Diaz", "Ellis", "Foster", "Green", "Hayes", "Irwin", "Jones"])
    contacts = pd.DataFrame({
        "constituent_id": [f"C{i:05d}" for i in range(1, n_constituents + 1)],
        "constituent_name": rng.choice(first, n_constituents) + " " + rng.choice(last, n_constituents),
        "constituent_type": rng.choice(["Alumnus", "Parent", "Friend", "Organization"], n_constituents, p=[.62, .18, .15, .05]),
        "preferred_class_year": rng.integers(1955, 2026, n_constituents),
        "city": rng.choice(["New York", "Boston", "Chicago", "Atlanta", "Dallas", "Seattle", "Miami", "Denver"], n_constituents),
        "state": rng.choice(["NY", "MA", "IL", "GA", "TX", "WA", "FL", "CO"], n_constituents),
    })
    contacts["email"] = contacts.constituent_name.str.lower().str.replace(" ", ".") + contacts.constituent_id.str.lower() + "@example.org"
    donor_ids = rng.choice(contacts.constituent_id, n_donors, replace=False)
    weights = rng.pareto(1.8, n_donors) + .15
    chosen = np.concatenate([donor_ids, rng.choice(donor_ids, n_gifts - n_donors, p=weights / weights.sum())])
    rng.shuffle(chosen)
    gift_dates = pd.Timestamp("2021-07-01") + pd.to_timedelta(rng.integers(0, 365 * 5, n_gifts), unit="D")
    gifts = pd.DataFrame({
        "constituent_id": chosen,
        "gift_id": [f"G{i:06d}" for i in range(1, n_gifts + 1)],
        "gift_date": gift_dates,
        "gift_amount": np.round(np.clip(rng.lognormal(6.2, 1.25, n_gifts), 10, 150000), 2),
        "gift_type": rng.choice(["Cash", "Pledge Payment", "Stock", "Matching Gift"], n_gifts, p=[.68, .2, .07, .05]),
        "campaign": rng.choice(["Annual Fund", "Student Success", "Research", "Athletics", "Arts", "Library", "Scholarships", "Health Sciences", "Capital Renewal", "Unrestricted"], n_gifts),
        "designation": rng.choice([f"Designation {i:02d}" for i in range(1, 16)], n_gifts),
        "gift_officer": rng.choice([f"Officer {c}" for c in "ABCDEFGH"], n_gifts),
    })
    data = gifts.merge(contacts, on="constituent_id", how="left")
    columns = ["constituent_id", "constituent_name", "constituent_type", "preferred_class_year", "city", "state", "email", "gift_id", "gift_date", "gift_amount", "gift_type", "campaign", "designation", "gift_officer"]
    data = data[columns]
    # Deliberate quality exceptions for the validation portfolio scenario.
    data["gift_amount"] = data["gift_amount"].astype(object)
    data.loc[:14, "email"] = ""
    data.loc[15:29, "preferred_class_year"] = np.nan
    data.loc[30:39, "state"] = "ZZ"
    data.loc[40:44, "constituent_name"] = data.loc[39, "constituent_name"]
    data.loc[45:49, "gift_amount"] = "malformed"
    data.loc[50:59, "gift_officer"] = ""
    data.loc[60:62, "gift_id"] = data.loc[59, "gift_id"]
    return data


def main() -> None:
    output = ROOT / "data" / "sample" / "fictional_advancement_gifts.csv"
    template = ROOT / "data" / "templates" / "upload_template.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    template.parent.mkdir(parents=True, exist_ok=True)
    data = generate()
    data.to_csv(output, index=False, date_format="%Y-%m-%d")
    data.head(0).to_csv(template, index=False)
    print(f"Generated {len(data):,} fictional gifts at {output}")


if __name__ == "__main__":
    main()
