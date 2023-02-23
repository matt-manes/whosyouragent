import json
import random
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class VersionUpdater:
    def __init__(self):
        self.versions_path = Path(__file__).parent / "browserVersions.json"
        if not self.versions_path.exists():
            self.versions_path.write_text(json.dumps({}))

    def update_firefox(self):
        try:
            url = "https://www.mozilla.org/en-US/firefox/releases/"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            release_list = soup.find("ol", class_="c-release-list")
            version = release_list.ol.li.a.text
            self.firefox = version
        except Exception as e:
            print(e)
            raise Exception("Error updating firefox")

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
            print(e)
            raise Exception("Error updating chrome")

    def update_safari(self):
        try:
            url = "https://en.wikipedia.org/wiki/Safari_(web_browser)"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[2].text[: info_boxes[2].text.find("[")]
            self.safari = version
        except Exception as e:
            print(e)
            raise Exception("Error updating safari")

    def update_edge(self):
        try:
            url = "https://www.techspot.com/downloads/7158-microsoft-edge.html"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            version = soup.find("span", class_="subver").text
            self.edge = version
        except Exception as e:
            print(e)
            raise Exception("Error updating edge")

    def update_vivaldi(self):
        try:
            url = "https://en.wikipedia.org/wiki/Vivaldi_(web_browser)"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[5].text[: info_boxes[5].text.find(" ")]
            self.vivaldi = version
        except Exception as e:
            print(e)
            raise Exception("Error updating vivaldi")

    def update_opera(self) -> str:
        try:
            url = "https://en.wikipedia.org/wiki/Opera_(web_browser)"
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            info_boxes = soup.find_all("td", class_="infobox-data")
            version = info_boxes[2].div.text[: info_boxes[2].div.text.find("[")]
            self.opera = version
        except Exception as e:
            print(e)
            raise Exception("Error updating Opera")

    def update_all(self):
        updaters = [
            self.update_firefox,
            self.update_chrome,
            self.update_safari,
            self.update_edge,
            self.update_vivaldi,
            self.update_opera,
        ]
        with ThreadPoolExecutor(6) as executor:
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
            if not ((versions[version]).replace(".", "")).isnumeric()
        ]
        for popper in poppers:
            versions.pop(popper)
        previous_versions = json.loads(self.versions_path.read_text())
        versions = previous_versions | versions
        self.versions_path.write_text(json.dumps(versions))


platforms = [
    "(Windows NT 10.0; Win64; x64)",
    "(x11; Ubuntu; Linux x86_64)",
    "(Windows NT 11.0; Win64; x64)",
    "(Macintosh; Intel Mac OS X 13_0_0)",
]


def randomize_version_number(version: str) -> str:
    """Randomize a version number so that it's in between
    the previous major version and the current one."""
    parts = [int(part) for part in version.split(".")]
    parts[0] = random.randint(parts[0] - 1, parts[0])
    for i, part in enumerate(parts[1:]):
        parts[i + 1] = random.randint(0, part)
    return ".".join(str(part) for part in parts)


def get_agent() -> str:
    """Build and return a user agent string."""
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
