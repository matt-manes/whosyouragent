import json
import os
import time
from pathlib import Path

from .whosyouragent import VersionUpdater, get_agent

browsers_path = Path(__file__).parent / "browserVersions.json"
if (
    not browsers_path.exists()
    or time.time() - os.stat(str(browsers_path)).st_mtime > 604800  # 1 week
):
    print("Updating whosyouragent browser versions...")
    updater = VersionUpdater()
    updater.update_all()
