from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_main_pages_render_with_sample():
    app = AppTest.from_file(str(Path(__file__).parents[1] / "app.py"), default_timeout=20)
    app.run()
    assert not app.exception
    app.button[0].click().run()
    assert not app.exception
    assert any(metric.label == "Total giving" for metric in app.metric)
    assert len(app.tabs) == 6
