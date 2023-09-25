"""
This module contains functions to convert time formats. The agreed time format is hh:mm:ss.msc as a string in MPAI standards.
"""
import datetime


def seconds_to_string(seconds: float) -> str:
    """Converts seconds to a human-readable time format (hh:mm:ss.msc).

    Parameters
    ----------
    seconds : float
        The number of seconds to convert

    Returns
    -------
    str
        A human-readable time format
    """

    seconds = float(seconds)

    # convert seconds in the format hh:mm:ss.msc
    time = str(datetime.timedelta(seconds=seconds))

    if seconds.is_integer():
        time = time + ".000"

    # convert days to hours
    if "day" in time:
        split_time = time.split(", ")
        days = int(split_time[0].split(" ")[0])
        hours = int(split_time[1].split(":")[0])
        time = f'{days * 24 + hours}:{":".join(split_time[1].split(":")[1::])}'

    time = ':'.join([x.zfill(2) for x in time.split(":")])  # add leading zeros
    split_time = time.split(".")
    time = split_time[0] + "." + split_time[1][:3]  # msc precision is 3

    return time


def time_to_seconds(time: str) -> float:
    """
    Converts a time string in the format hh:mm:ss.msc in seconds.

    Parameters
    ----------
    time : str
        The time string to convert

    Raises
    ------
    ValueError
        If the time string is not in the correct format

    Returns
    -------
    float
        The number of seconds

    """

    if not time.replace(":", "").replace(".", "").isdigit():
        raise ValueError("The time string is not in the correct format")

    split_time = time.split(":")
    hours = int(split_time[0])
    minutes = int(split_time[1])
    seconds = float(split_time[2])

    return hours * 3600 + minutes * 60 + seconds


def frames_to_seconds(frames: int, fps: int) -> float:
    """
    Converts a number of frames in seconds.

    Parameters
    ----------
    frames : int
        The number of frames
    fps : int
        The number of frames per second

    Raises
    ------
    ValueError
        If the number of frames per second is less than or equal to 0 or if the number of frames is less than 0

    Returns
    -------
    float
        The number of seconds

    """

    if fps <= 0:
        raise ValueError("The number of frames per second must be greater than 0")
    if frames < 0:
        raise ValueError("The number of frames must be greater than or equal to 0")

    return frames / fps


def seconds_to_frames(seconds: float, fps: int) -> int:
    """
    Converts a number of seconds in frames.

    Parameters
    ----------
    seconds : float
        The number of seconds
    fps : int
        The number of frames per second

    Raises
    ------
    ValueError
        If the number of frames per second is less than or equal to 0 or if the number of seconds is less than 0

    Returns
    -------
    int
        The number of frames

    """

    if fps <= 0:
        raise ValueError("The number of frames per second must be greater than 0")
    if seconds < 0:
        raise ValueError("The number of seconds must be greater than or equal to 0")

    return int(seconds * fps)
