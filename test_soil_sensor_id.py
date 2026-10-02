"""
Unit tests for the gateway local-API soil sensor ID parsing.

Imports only the pure helpers, so it needs no running exporter.
Run directly: `python3 test_soil_sensor_id.py`
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("TEMPERATURE_UNIT", "c")

import ecowitt_exporter as ex  # noqa: E402  pylint: disable=wrong-import-position


def _entry(type_, id_):
    return {"img": "wh51", "type": str(type_), "name": "x", "id": id_}


def test_bound_channels_only():
    pages = [[_entry(14, "F9500"), _entry(15, "f9462"), _entry(16, "F94F2"),
              _entry(17, "FFFFFFFE"), _entry(18, "FFFFFFFF")]]
    assert ex.parse_soil_sensors(pages) == {
        "soilmoisture1": "F9500", "soilmoisture2": "F9462", "soilmoisture3": "F94F2"}


def test_high_channels_and_non_soil_ignored():
    pages = [[_entry(58, "ABCD1")], [{"img": "wh45", "type": "39", "id": "2E0B"}]]
    assert ex.parse_soil_sensors(pages) == {"soilmoisture9": "ABCD1"}


def test_garbage_type_skipped():
    assert not ex.parse_soil_sensors([[{"type": None, "id": "1"}, {"id": "2"}]])


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
