import pytest

from iolink_utils.exceptions import InvalidVersionStringFormat
from iolink_utils.utils.version import Version


def test_utils_version():
    ver = Version()

    assert str(ver) == "Version(V0.0.0.0)"
    assert ver < Version("1.0")
    assert ver < Version("V0.1.2.3")

    assert str(Version("1.2.1")) == "Version(V1.2.1)"

    assert Version("1") < Version("V2")

    assert Version("1.2.0") == Version("1.2")
    assert Version("1.2.0.0") == Version("1.2")
    assert Version("1.2") < Version("1.2.1")
    assert Version("1.2.1") > Version('1.2')
    assert Version("1.2.3") > Version("1.2.0")


def test_utils_version_invalid():
    with pytest.raises(InvalidVersionStringFormat):
        Version('1.a')
    with pytest.raises(InvalidVersionStringFormat):
        Version('abc')

    assert Version('1').__eq__(1) == NotImplemented
    assert Version('1').__lt__(2) == NotImplemented
