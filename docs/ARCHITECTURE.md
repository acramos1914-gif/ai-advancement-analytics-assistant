# Architecture

The app uses a deliberately small, layered design.

1. `validation.py` checks file shape and reports exceptions without mutating input.
2. `cleaning.py` standardizes fields, excludes unusable gift rows, and assigns July–June fiscal years.
3. `analytics.py` produces the trusted aggregate result object.
4. `privacy.py` allow-lists aggregate keys and recursively removes identifier-shaped fields.
5. `demo_provider.py` or `live_provider.py` interprets only that safe context.
6. `reporting.py` exports the trusted KPIs and reviewed narrative.
7. `app.py` coordinates the local Streamlit experience.

Raw records never enter provider prompts. No upload is stored in a database or log.

