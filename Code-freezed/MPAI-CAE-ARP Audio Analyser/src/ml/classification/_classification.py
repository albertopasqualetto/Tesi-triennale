import pickle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

from ml.datasets import load_berio_nono, load_pretto
from ._data_structures import Classifier
from ._constants import CLASSIFICATION_MAPPING, MODELS_PATH

def load_model(model_name: str) -> Classifier:
    """Load a trained classifier from disk.
    Aviable models are:

    - pretto_and_berio_nono_classifier

    Parameters
    ----------
    model_name: str
        the path of the model to be loaded

    Raises
    ------
    ValueError
        if the model name is not valid

    Returns
    -------
    Classifier
        the classifier loaded from disk

    """

    models = {
        "pretto_classifier":
        MODELS_PATH.joinpath('pretto_classifier.pkl'),
        "pretto_and_berio_nono_classifier":
        MODELS_PATH.joinpath('pretto_and_berio_nono_classifier.pkl')
    }

    try:
        with open(models[model_name], 'rb') as f:
            return Classifier(pickle.load(f))
    except FileNotFoundError:
        generate_classifier(models[model_name])
        return load_model(model_name)


def generate_classifier(dest_path):
    data1 = load_pretto()
    data2 = load_berio_nono()

    data = pd.concat([data1, data2])
    data = data.replace(CLASSIFICATION_MAPPING)

    X = data.drop(columns=['noise_type', 'label'], axis=1)
    y = data.label

    rfc = RandomForestClassifier(n_estimators=111,
                                 criterion="log_loss",
                                 max_features="log2",
                                 min_samples_leaf=1,
                                 n_jobs=-1)

    rfc.fit(X, y)

    with open(dest_path, 'wb') as f:
        pickle.dump(rfc, f)
