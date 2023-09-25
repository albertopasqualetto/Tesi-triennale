import os
import tempfile
import uuid
import numpy as np

from mpai_cae_arp.audio import AudioWave
from mpai_cae_arp.types.irregularity import Irregularity, IrregularityFile, Source

import audio_analyzer.segment_finder as sf


def test_calculate_offset():    # FIXME this does not work because calculate_offset() takes only audio parts after 15 seconds
    audio = AudioWave(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 24, 1, 8000)
    video = AudioWave(np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 24, 1, 8000)
    offset = sf.calculate_offset(audio, video)
    assert offset == 0.0


def test_get_irregularities_from_audio():
    audio = AudioWave(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 24, 1, 8000)
    irregularities = sf.get_irregularities_from_audio(audio)
    assert irregularities == []


def test_merge_irreg_files():
    file1 = IrregularityFile(
        irregularities=[
            Irregularity(
                id=uuid.uuid4(),
                source=Source.AUDIO,
                time_label="00:10:00.000"
                )],
        offset=0.0)
    file2 = IrregularityFile(
        irregularities=[
            Irregularity(
                id=uuid.uuid4(),
                source=Source.AUDIO,
                time_label="00:00:00.000")],
        offset=1.0)
    new_file = sf.merge_irreg_files(file1, file2)
    assert new_file.offset == 1.0
    assert len(new_file.irregularities) == 2


def test_extract_audio_irregularities():
    audio = AudioWave(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), 24, 1, 8000)
    irregularities = sf.get_irregularities_from_audio(audio)
    irreg_file = IrregularityFile(irregularities=irregularities, offset=0.0)

    sf.extract_audio_irregularities(audio, irreg_file, tempfile.gettempdir())

    for irreg in irreg_file.irregularities:
        if irreg.source == Source.AUDIO:
            assert os.path.exists(f"{tempfile.gettempdir()}/AudioBlocks/{irreg.id}.wav")
