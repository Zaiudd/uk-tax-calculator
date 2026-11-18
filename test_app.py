"""Checks that the web page loads and shows the right answer."""

from streamlit.testing.v1 import AppTest


def test_app_runs_without_errors():
    app = AppTest.from_file("app.py").run()
    assert not app.exception


def test_app_shows_take_home_for_default_salary():
    app = AppTest.from_file("app.py").run()
    assert app.metric[0].value == "£25,119.60"
