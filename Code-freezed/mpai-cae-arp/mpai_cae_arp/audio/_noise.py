from dataclasses import dataclass


@dataclass
class Noise:
    """
    A class to represent a noise, which is a signal that resides in a certain range of decibels, like a sort of filter.

    Args:
        label (str): a label which describes this noise
        db_max (int): the maximum value of this noise in decibels (must be less than or equal to 0)
        db_min (int): the minimum value of this noise in decibels (must be less than or equal to 0)

    Raises:
        ValueError: if ``db_max`` is less than ``db_min``, or if ``db_min`` or ``db_max`` are greater than 0

    .. topic:: More about noise classes

        Noise classes of interest are defined in :cite:`10.1162/comj_a_00487`, where we can find three main notable classes:

        1. type A, from :math:`-50dB` to :math:`-63dB`, which is noise in the middle of a recording, i.e., silence between spoken words;
        2. type B, from :math:`-63dB` to :math:`-69dB`, which is noise of the recording head without any specific input signal;
        3. type C, from :math:`-69dB` to :math:`-72dB`, which is noise coming from sections of pristine tape.
    """
    _label: str
    _db_max: int
    _db_min: int

    def __init__(self, label, db_max, db_min) -> None:
        if db_max < db_min:
            raise ValueError("db_max must be greater than db_min")
        if db_min > 0 or db_max > 0:
            raise ValueError("db_min and db_max must be negative or zero")

        self._label = label
        self._db_max = db_max
        self._db_min = db_min

    @property
    def label(self):
        return self._label

    @property
    def db_range(self):
        """Get the range of this noise."""
        return self.db_max - self.db_min

    @property
    def db_max(self):
        return self._db_max

    @property
    def db_min(self):
        return self._db_min

    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, Noise):
            raise TypeError("Cannot compare Noise with not Noise")
        return self.db_min < __o.db_min

    def __gt__(self, __o: object) -> bool:
        if not isinstance(__o, Noise):
            raise TypeError("Cannot compare Noise with not Noise")
        return self.db_max > __o.db_max

    def __le__(self, __o: object) -> bool:
        if not isinstance(__o, Noise):
            raise TypeError("Cannot compare Noise with not Noise")
        return self < __o or self == __o

    def __repr__(self):
        return f"<Noise({self.label}, {self.db_min}dB, {self.db_max}dB)>"
