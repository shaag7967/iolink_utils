from typing import Optional
from datetime import date, datetime
import re
from .iodd_version import Version


class IoddFilename:
    # <vendor name>-<device name>-<release date>-IODD<schema version>.xml
    def __init__(self, filename: Optional[str]):
        self.value = filename
        self.date: Optional[date] = None
        self.schemaVersion: Version = Version()

        if filename is not None:
            match = re.search(r"-(\d{8})-IODD(\d+(?:\.\d+)*)(?:-[a-z]{2})?\.xml", filename)
            if match:
                self.date = datetime.strptime(match.group(1), "%Y%m%d").date()
                self.schemaVersion = Version(match.group(2))
