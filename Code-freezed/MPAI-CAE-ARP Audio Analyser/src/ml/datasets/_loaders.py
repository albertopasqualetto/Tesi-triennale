import itertools
from importlib import resources
import pandas as pd

_DATA_MODULE = 'ml.datasets'

def _filter_dataset(data: pd.DataFrame,
                    labels: list | None = None,
                    noise_type: str | None = None,
                    combination: bool = False):
    df = data
    if labels is not None:
        if combination:
            df = data[data['label'].isin(
                ['_'.join(l) for l in itertools.product(labels, labels)])]
        else:
            df = data[data['label'].isin(labels)]
    if noise_type is not None:
        df = df[df.noise_type == noise_type]

    return df


def load_pretto(filters: dict = None, return_X_y: bool = False):
    """Load and return the Pretto dataset (classification).

    =================   ============================
    Classes                                       25
    Samples per noise   2075 (A), 5050 (B), 1933 (C)
    Samples total                               9058
    Dimensionality                                15
    Features                           string, float
    =================   ============================

    Read more in the :ref:`Datasets <pretto>`.

    Examples
    --------

    .. doctest::

        >>> from ml.datasets import load_pretto
        >>> data = load_pretto(filters={'labels': ['7C', '7N'], 'noise_type': None, 'combination': True})
        >>> data.noise_type.unique()
        array(['A', 'B', 'C'], dtype=object)
        >>> data.label.unique()
        array(['7C_7C', '7C_7N', '7N_7C', '7N_7N'], dtype=object)

    """
    data = pd.read_csv(resources.files(_DATA_MODULE).joinpath('data/train.csv'))

    if filters is not None:
        data = _filter_dataset(data, filters.get('labels'),
                               filters.get('noise_type'),
                               filters.get('combination'))

    if return_X_y:
        return data.drop("label", axis=1), data["label"]

    return data


def load_berio_nono(filters: dict = None, return_X_y: bool = False):
    """Load and return the Berio-Nono dataset (classification).

    =================   ============================
    Classes                                        4
    Samples per noise   1231 (A), 1796 (B), 9175 (C)
    Samples total                              12202
    Dimensionality                                15
    Features                           string, float
    =================   ============================

    Read more in the :ref:`Datasets <berio-nono>`.

    Examples
    --------

    .. doctest::

        >>> from ml.datasets import load_berio_nono
        >>> data = load_berio_nono(filters={'labels': ['7C', '7N'], 'noise_type': None, 'combination': True})
        >>> data.noise_type.unique()
        array(['A', 'B', 'C'], dtype=object)
        >>> data.label.unique()
        array(['7C_7C', '7N_7N'], dtype=object)

    """
    data = pd.read_csv(resources.files(_DATA_MODULE).joinpath('data/test.csv'))

    if filters is not None:
        data = _filter_dataset(data, filters.get('labels'),
                               filters.get('noise_type'),
                               filters.get('combination'))

    if return_X_y:
        return data.drop("label", axis=1), data["label"]

    return data
