from dataclasses import dataclass
from datetime import date
from typing import Optional

from .iodd_version import Version

@dataclass
class DocumentInfo:
    version: Version = Version("V0.0")
    releaseDate: Optional[date] = None
    copyright: str = ""
