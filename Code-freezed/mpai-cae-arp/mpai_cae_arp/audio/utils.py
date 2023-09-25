"""
The ``utils`` module contains a set of functions which are used to perform some common tasks in the audio processing. The most important functions are:
"""

from enum import Enum
import numpy as np


class Criterion(Enum):
    """
    Represents a mathematical criterion. Some kinds of calculations can be done in different ways and often we want to have control over the way they are done. For example, when calculating the RMS of a signal, we can either take the maximum value of the RMS of each channel, or the mean value of the RMS of each channel.

    The following values are available:

    * ``max``: which value is the string ``'max'``.
    * ``min``: which value is the string ``'min'``.
    * ``mean``: which value is the string ``'mean'``.

    """

    max = 'max'
    min = 'min'
    mean = 'mean'


def db_to_pcm(db: int, bit_depth: int) -> int:
    r"""
    Convert a dB value to a float value.

    Args:
        db (int): The dB value to convert.
        bit_depth (int): The bit depth of the PCM value, this is used to calculate the maximum value of the PCM value.

    The dB value is converted to a PCM value using the following formula:

    .. math::

        \text{PCM} = \left\lfloor 2^{bit\_depth - 1} \times 10^{\frac{db}{20}}\right\rceil

    where :math:`\lfloor x \rceil` is the *round* function, which approximates the result to the nearest integer (it introduces the quantization error).
    """
    return round(10**(db / 20) * 2**(bit_depth - 1))


def pcm_to_db(pcm, bit_depth: int) -> float:
    r"""
    Convert the given signal power to a dB value.

    Args:
        pcm (int): The PCM value to convert.
        bit_depth (int): The bit depth of the PCM value, this is used to calculate the maximum value of the PCM value.

    The PCM value is converted to a dB value using the following formula:

    .. math::

        db = 20 \times log_{10}\left(\frac{\text{PCM}}{2^{bit\_depth - 1}}\right)

    .. note::

        Due to the formula the result on input ``0`` should be ``-inf``, nonetheless, as we are threating discrete quantities, we return the minimum value that can be represented by the given bit depth based on the following table:

        +---------+--------------------+
        | Bit     | Minimum value (dB) |
        +=========+====================+
        | 16      | -98                |
        +---------+--------------------+
        | 24      | -146               |
        +---------+--------------------+
        | 32      | -194               |
        +---------+--------------------+

        for a more detailed explanation see about `audio bit depth <https://en.wikipedia.org/wiki/Audio_bit_depth#Quantization>`_.
    """

    MIN_VAL = {
        "16": -98,
        "24": -146,
        "32": -194,
    }

    if pcm == 0:
        return MIN_VAL[str(bit_depth)]

    return 20 * np.log10(abs(pcm / 2**(bit_depth - 1)))


def rms(array: np.ndarray) -> float:
    r"""
    Calculate the RMS of the given array.

    The Root Mean Square (RMS) is the square root of the mean of the squares of the values in the array. It is a measure of the magnitude of a signal. It is calculated using the following formula:

    .. math::

        \text{RMS} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} x_i^2}

    where :math:`x_i` is the value of the array at index :math:`i` and :math:`n` is the length of the array.
    """

    mean_squares = np.square(array).mean()
    if mean_squares == 0:
        return 0
    return np.sqrt(mean_squares)


def get_last_index(haystack: np.ndarray, threshold) -> int | tuple | None:
    """
    Get the index of the last occurrence of a value greater than ``threshold`` in the given array

    Args:
        haystack (np.ndarray): the array to inspect
        threshold (int): the threshold to use

    Returns:
        The index of the last occurrence of a value greater than the given limit in the array, if the array is multi-dimensional it returns a tuple. If there is no match, None is returned
    """
    positions = np.where(haystack >= threshold)
    indexes = positions[0]
    if indexes.size == 0:
        return None
    if len(positions) > 1:
        return list(zip(*positions))[-1]
    return indexes[-1]
