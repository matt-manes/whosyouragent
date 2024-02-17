import json
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class VersionUpdater:
    def __init__(self):
        self.versions_path = Path(__file__).parent / "browserVersions.json"
        self.firefox: str = ""
        self.chrome: str = ""
        self.safari: str = ""
        self.edge: str = ""
        self.vivaldi: str = ""
        self.opera: str = ""
        if not self.versions_path.exists():
            self.versions_path.write_text(
                json.dumps(
                    {
                        "Firefox": "122.0.1",
                        "Chrome": "109.0.5414.165",
                        "Edg": "121.0.2277.128",
                        "Vivaldi": "6.5.3206.63",
                        "OPR": "107.0.5045.21",
                        "Safari": "17.2",
                    }
                )
            )

    def update_firefox(self):
        try:
            url = "https://www.mozilla.org/en-US/firefox/releases/"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            release_list = soup.find("ol", class_="c-release-list")
            version = release_list.find("ol").find("li").find("a").text  # type: ignore
            self.firefox = version
        except Exception as e:
            pass

    def update_chrome(self):
        try:
            url = "https://en.wikipedia.org/wiki/Google_Chrome"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[8].text[
                : min([info_boxes[8].text.find("["), info_boxes[8].text.find("/")])
            ]
            self.chrome = version
        except Exception as e:
            pass

    def update_safari(self):
        try:
            url = "https://en.wikipedia.org/wiki/Safari_(web_browser)"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[2].text[: info_boxes[2].text.find("[")]
            self.safari = version
        except Exception as e:
            pass

    def update_edge(self):
        try:
            url = "https://www.techspot.com/downloads/7158-microsoft-edge.html"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            version = soup.find("div", class_="subver").text  # type: ignore
            self.edge = version
        except Exception as e:
            pass

    def update_vivaldi(self):
        try:
            url = "https://vivaldi.com/blog/"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            text = soup.find("div", class_="download-vivaldi-sidebar").text  # type: ignore
            text = text.split(" - ")[1]
            text = text.replace(" (", ".")
            version = text[: text.find(")")]
            self.vivaldi = version
        except Exception as e:
            pass

    def update_opera(self):
        try:
            url = "https://en.wikipedia.org/wiki/Opera_(web_browser)"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[2].div.text[: info_boxes[2].div.text.find("[")]
            self.opera = version
        except Exception as e:
            pass

    def update_all(self):
        updaters = [
            self.update_firefox,
            self.update_chrome,
            self.update_safari,
            self.update_edge,
            self.update_vivaldi,
            self.update_opera,
        ]
        with ThreadPoolExecutor() as executor:
            for updater in updaters:
                executor.submit(updater)
        versions = {
            "Firefox": self.firefox,
            "Chrome": self.chrome,
            "Edg": self.edge,
            "Vivaldi": self.vivaldi,
            "OPR": self.opera,
            "Safari": self.safari,
        }
        # Remove any keys that failed to update and keep previous version number
        poppers = [
            version
            for version in versions
            if versions[version]
            and not ((versions[version]).replace(".", "")).isnumeric()
        ]
        for popper in poppers:
            versions.pop(popper)
        previous_versions = json.loads(self.versions_path.read_text())
        versions = previous_versions | versions
        self.versions_path.write_text(json.dumps(versions))


def randomize_version_number(version: str) -> str:
    """Randomize a version number so that it's in between
    the previous major version and the current one."""
    parts = [int(part) for part in version.split(".")]
    parts[0] = random.randint(parts[0] - 1, parts[0])
    for i, part in enumerate(parts[1:]):
        parts[i + 1] = random.randint(0, part)
    return ".".join(str(part) for part in parts)


def get_agent() -> str:
    """Build and return a user agent string.

    :param as_dict: If True, return {"User-Agent": useragent} instead of just the useragent string.
    Note: Leaving this parameter in place to maintain backwards compatibility,
    but it's advised to use the `get_header()` function instead."""
    platforms = [
        "(Windows NT 10.0; Win64; x64)",
        "(x11; Ubuntu; Linux x86_64)",
        "(Windows NT 11.0; Win64; x64)",
        "(Macintosh; Intel Mac OS X 13_0_0)",
    ]
    browsers = json.loads((Path(__file__).parent / "browserVersions.json").read_text())
    for browser in browsers:
        browsers[browser] = randomize_version_number(browsers[browser])
    browser = random.choice(list(browsers.keys()))
    if browser == "Safari":
        platform = platforms[-1]
        useragent = f'Mozilla/5.0 {platform} AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{browsers["Safari"]} Safari/605.1.15'
    else:
        platform = random.choice(platforms)
        if browser == "Firefox":
            platform = platform[: platform.rfind(")")] + f"; rv:{browsers[browser]})"
            useragent = (
                f"Mozilla/5.0 {platform} Gecko/20100101 Firefox/{browsers[browser]}"
            )
        else:
            useragent = f'Mozilla/5.0 {platform} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{browsers["Chrome"]} Safari/537.36'
            if browser == "Edg":
                useragent += f' Edg/{browsers["Edg"]}'
            elif browser == "OPR":
                useragent += f' OPR/{browsers["OPR"]}'
            elif browser == "Vivaldi":
                useragent += f' Vivaldi/{browsers["Vivaldi"]}'
    return useragent


def get_header() -> dict[str, str]:
    """Returns a dictionary `{'User-Agent': <random user agent string>}` for convenience.
    >>> response = requests.get(url, headers=get_header())"""
    return {"User-Agent": get_agent()}
