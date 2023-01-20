from pathlib import Path

import pytest

import whosyouragent

updater = whosyouragent.VersionUpdater()
updater.update_all()


def test_whosyouragent_update_firefox():
    assert all(ch.isnumeric() or ch == "." for ch in updater.firefox)


def test_whosyouragent_update_chrome():
    assert all(ch.isnumeric() or ch == "." for ch in updater.chrome)


def test_whosyouragent_update_safari():
    assert all(ch.isnumeric() or ch == "." for ch in updater.safari)


def test_whosyouragent_update_edge():
    assert all(ch.isnumeric() or ch == "." for ch in updater.edge)


def test_whosyouragent_update_vivaldi():
    assert all(ch.isnumeric() or ch == "." for ch in updater.vivaldi)


def test_whosyouragent_update_opera():
    assert all(ch.isnumeric() or ch == "." for ch in updater.opera)


def test_whosyouragent_update_all():
    assert all(ch.isnumeric() or ch == "." for ch in updater.firefox)
    assert all(ch.isnumeric() or ch == "." for ch in updater.chrome)
    assert all(ch.isnumeric() or ch == "." for ch in updater.safari)
    assert all(ch.isnumeric() or ch == "." for ch in updater.edge)
    assert all(ch.isnumeric() or ch == "." for ch in updater.vivaldi)
    assert all(ch.isnumeric() or ch == "." for ch in updater.opera)
    assert (
        Path(__file__).parent.parent / "src" / "whosyouragent" / "browserVersions.json"
    ).exists()


def test_whosyouragent_get_agent():
    agent = whosyouragent.get_agent()
    assert type(agent) == str
    assert agent.startswith("Mozilla/5.0 ")
