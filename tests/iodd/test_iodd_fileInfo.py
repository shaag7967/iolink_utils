from pathlib import Path
from datetime import date

from iolink_utils.iodd.iodd import IoddFileInfo
from iolink_utils.utils.version import Version


def test_iodd_BasicDevice():
    test_dir = Path(__file__).parent
    info = IoddFileInfo(str(test_dir.joinpath('IODDViewer1.4_Examples/IO-Link-01-BasicDevice-20211215-IODD1.1.xml')))

    assert info.fileExists
    assert info.filename == 'IO-Link-01-BasicDevice-20211215-IODD1.1.xml'
    assert info.sizeInBytes > 10000
    assert info.schemaVersion == Version('1.1')
    assert info.dirPath.endswith('IODDViewer1.4_Examples')
    assert info.date == date(2021, 12, 15)
