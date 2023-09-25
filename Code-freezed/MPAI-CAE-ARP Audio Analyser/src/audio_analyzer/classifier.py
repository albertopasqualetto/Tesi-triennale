from pandas import DataFrame

from mpai_cae_arp.audio import AudioWave
from mpai_cae_arp.types.irregularity import Irregularity, IrregularityProperties
from ml import classification as mlc


def classification_to_irreg_properties(classification: mlc.ClassificationResult) -> IrregularityProperties:
    return IrregularityProperties(
        reading_equalisation=classification.reading_equalization,
        reading_speed=classification.reading_speed,
        writing_speed=classification.writing_speed,
        writing_equalisation=classification.writing_equalization,
    )


def classify(audio_blocks: DataFrame) -> list[IrregularityProperties]:

    audio_blocks_classification = []

    # classify the audioBlocks
    eq_classifier = mlc.load_model("pretto_and_berio_nono_classifier")
    prediction = eq_classifier.predict(audio_blocks)

    for i in range(len(prediction)):
        classification = classification_to_irreg_properties(prediction.iloc[i].classification)
        audio_blocks_classification.append(classification)

    return audio_blocks_classification


def extract_features(audio_blocks: list[Irregularity]) -> DataFrame:

    features = {f'mfcc{i}': [] for i in range(1, 14)}

    for audio_block in audio_blocks:
        audio = AudioWave.from_file(audio_block.audio_block_URI)
        audio_mfcc = audio.get_mfcc()
        for i, key in enumerate(features.keys()):
            features[key].append(audio_mfcc[i])

    return DataFrame(features)
