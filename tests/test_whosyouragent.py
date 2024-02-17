import json
import random
from pathlib import Path


import whosyouragent

updater = whosyouragent.VersionUpdater()
updater.update_all()


def test__whosyouragent__update_firefox():
    assert all(ch.isnumeric() or ch == "." for ch in updater.firefox)


def test__whosyouragent__update_chrome():
    assert all(ch.isnumeric() or ch == "." for ch in updater.chrome)


def test__whosyouragent__update_safari():
    assert all(ch.isnumeric() or ch == "." for ch in updater.safari)


def test__whosyouragent__update_edge():
    assert all(ch.isnumeric() or ch == "." for ch in updater.edge)


def test__whosyouragent__update_vivaldi():
    assert all(ch.isnumeric() or ch == "." for ch in updater.vivaldi)


def test__whosyouragent__update_opera():
    assert all(ch.isnumeric() or ch == "." for ch in updater.opera)


def test__whosyouragent__update_all():
    assert all(ch.isnumeric() or ch == "." for ch in updater.firefox)
    assert all(ch.isnumeric() or ch == "." for ch in updater.chrome)
    assert all(ch.isnumeric() or ch == "." for ch in updater.safari)
    assert all(ch.isnumeric() or ch == "." for ch in updater.edge)
    assert all(ch.isnumeric() or ch == "." for ch in updater.vivaldi)
    assert all(ch.isnumeric() or ch == "." for ch in updater.opera)
    assert (
        Path(__file__).parent.parent / "src" / "whosyouragent" / "browserVersions.json"
    ).exists()


def test__whosyouragent__get_agent():
    agent = whosyouragent.get_agent()
    assert type(agent) == str
    assert agent.startswith("Mozilla/5.0 ")
    agent = whosyouragent.get_agent(as_dict=True)
    assert type(agent) == dict
    assert list(agent.keys()) == ["User-Agent"]
    assert agent["User-Agent"].startswith("Mozilla/5.0 ")


def test__whosyouragent__randomize_version_number():
    versions = json.loads(
        (
            Path(__file__).parent.parent
            / "src"
            / "whosyouragent"
            / "browserVersions.json"
        ).read_text()
    )

    def checksum(version: str) -> int:
        return sum(int(part) for part in version.split("."))

    def get_random_browser() -> str:
        return versions[random.choice(list(versions.keys()))]

    for _ in range(100000):
        original = get_random_browser()
        original_sum = checksum(original)
        new = whosyouragent.whosyouragent.randomize_version_number(original)
        assert all(ch.isnumeric() or ch == "." for ch in new)
        assert original_sum >= checksum(new)


def test__get_header():
    headers = whosyouragent.whosyouragent.get_header()
    assert isinstance(headers, dict)
    assert "User-Agent" in headers
    assert isinstance(headers["User-Agent"], str)
    assert headers["User-Agent"] != ""
