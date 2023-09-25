from dataclasses import dataclass
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from mpai_cae_arp.audio.standards import EqualizationStandard, SpeedStandard
from ._constants import INVERSE_CLASSIFICATION_MAPPING


@dataclass
class ClassificationResult:
    """
    A class to represent the result of a classification.

    Since the classification recognizes 4 informations, those are stored in a container class to have the possibility to find all informations in the same place, but, when necessary, use only the part that is needed.

    Informations are:

    - the reading speed of the tape,
    - the writing speed,
    - the reading post-emphasis equalization curve
    - the writing pre-emphasis equalization curve
    """

    writing_speed: SpeedStandard
    reading_speed: SpeedStandard
    writing_equalization: EqualizationStandard
    reading_equalization: EqualizationStandard


_MAP_CLASS_TO_RESULT = {
    '3N_3N':
    ClassificationResult(SpeedStandard.III, SpeedStandard.III,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '3N_7C':
    ClassificationResult(SpeedStandard.III, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '3N_7N':
    ClassificationResult(SpeedStandard.III, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '3N_15C':
    ClassificationResult(SpeedStandard.III, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '3N_15N':
    ClassificationResult(SpeedStandard.III, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '7C_3N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.III,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '7C_7C':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.IV,
                         EqualizationStandard.CCIR, EqualizationStandard.CCIR),
    '7C_7N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.IV,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '7C_15C':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.V,
                         EqualizationStandard.CCIR, EqualizationStandard.CCIR),
    '7C_15N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.V,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '7N_3N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.III,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '7N_7C':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '7N_7N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '7N_15C':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '7N_15N':
    ClassificationResult(SpeedStandard.IV, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '15C_3N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.III,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '15C_7C':
    ClassificationResult(SpeedStandard.V, SpeedStandard.IV,
                         EqualizationStandard.CCIR, EqualizationStandard.CCIR),
    '15C_7N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.IV,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '15C_15C':
    ClassificationResult(SpeedStandard.V, SpeedStandard.V,
                         EqualizationStandard.CCIR, EqualizationStandard.CCIR),
    '15C_15N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.V,
                         EqualizationStandard.CCIR, EqualizationStandard.NAB),
    '15N_3N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.III,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '15N_7C':
    ClassificationResult(SpeedStandard.V, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '15N_7N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.IV,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
    '15N_15C':
    ClassificationResult(SpeedStandard.V, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.CCIR),
    '15N_15N':
    ClassificationResult(SpeedStandard.V, SpeedStandard.V,
                         EqualizationStandard.NAB, EqualizationStandard.NAB),
}


class Classifier:

    model: RandomForestClassifier | DecisionTreeClassifier | KNeighborsClassifier

    def __init__(self, model):
        self.model = model

    def predict(self, x: pd.DataFrame) -> pd.DataFrame:
        prediction = self.model.predict(x)
        prediction = pd.DataFrame(prediction, columns=['classification'])

        prediction = prediction.replace(INVERSE_CLASSIFICATION_MAPPING)

        prediction = prediction.replace(_MAP_CLASS_TO_RESULT)

        return prediction

    def get_model_description(self) -> str:
        return str(self.model)
