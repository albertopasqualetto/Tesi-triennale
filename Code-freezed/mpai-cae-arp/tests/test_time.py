import pytest
from mpai_cae_arp import time


def test_seconds_to_time():
    assert time.seconds_to_string(0) == "00:00:00.000"
    assert time.seconds_to_string(123.456) == "00:02:03.456"
    assert time.seconds_to_string(123456.789) == "34:17:36.789"
    assert time.seconds_to_string(123) == "00:02:03.000"


def test_time_to_seconds():
    assert time.time_to_seconds("00:00:00.000") == 0
    assert time.time_to_seconds("00:02:03.456") == 123.456
    assert time.time_to_seconds("34:17:36.789") == 123456.789

    with pytest.raises(ValueError):
        time.time_to_seconds("00:02:03.456.789")

    with pytest.raises(ValueError):
        time.time_to_seconds("days 1, 00:02:05.123")


def test_frames_to_seconds():
    assert time.frames_to_seconds(0, 44100) == 0
    assert time.frames_to_seconds(44100, 44100) == 1
    assert time.frames_to_seconds(88200, 44100) == 2
    assert time.frames_to_seconds(44100, 48000) == 0.91875

    with pytest.raises(ValueError):
        time.frames_to_seconds(0, 0)

    with pytest.raises(ValueError):
        time.frames_to_seconds(0, -1)

    with pytest.raises(ValueError):
        time.frames_to_seconds(-1, 44100)


def test_seconds_to_frames():
    assert time.seconds_to_frames(0, 44100) == 0
    assert time.seconds_to_frames(1, 44100) == 44100
    assert time.seconds_to_frames(2, 44100) == 88200
    assert time.seconds_to_frames(0.91875, 48000) == 44100

    with pytest.raises(ValueError):
        time.seconds_to_frames(0, 0)

    with pytest.raises(ValueError):
        time.seconds_to_frames(0, -1)

    with pytest.raises(ValueError):
        time.seconds_to_frames(-1, 44100)
