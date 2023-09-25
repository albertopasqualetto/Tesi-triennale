"""
Test Preservation Master Files
"""

import pytest
import subprocess
import acoustid
import json
import os
import shutil
import filecmp
from conftest import working_path, pmf_path, files_names, oldify, AUDIO_THRESHOLD, VIDEO_THRESHOLD


@pytest.mark.parametrize("files_name", files_names)
def test_preservation_audio_file(files_name: str):
    """
    Test `PreservationAudioFile.wav`.

    Parameters
    ----------
    files_name : str
        The name of the files to test.
    """
    # after packager run checks
    input_paf_path = working_path / "PreservationAudioFile" / (files_name+".wav")
    output_paf_path = pmf_path / files_name / "PreservationAudioFile.wav"
    assert output_paf_path.is_file(), "PreservationAudioFile.wav not found"
    input_fingerprint = acoustid.fingerprint_file(input_paf_path)
    output_fingerprint = acoustid.fingerprint_file(output_paf_path)
    assert acoustid.compare_fingerprints(input_fingerprint, output_fingerprint) > AUDIO_THRESHOLD, "PreservationAudioFile.wav is not the same as input"

    # DS8 files equality check
    test_paf_path = oldify(pmf_path) / files_name / "PreservationAudioFile.wav"
    test_fingerprint = acoustid.fingerprint_file(test_paf_path)
    assert acoustid.compare_fingerprints(output_fingerprint, test_fingerprint) > AUDIO_THRESHOLD, "PreservationAudioFile.wav is not the same as test dataset's"


@pytest.mark.parametrize("files_name", files_names)
def test_preservation_audio_visual_file(files_name: str, tmp_path):
    """
    Test `PreservationAudioVisualFile.mov`.

    Parameters
    ----------
    files_name : str
        The name of the files to test.
    """
    # after packager run checks
    input_pvf_path = working_path / "PreservationAudioVisualFile" / (files_name+".mov")
    output_pvf_path = pmf_path / files_name / "PreservationAudioVisualFile.mov"
    assert output_pvf_path.is_file(), "PreservationAudioVisualFile.mov not found"
    subprocess.run(["ffmpeg", "-i", output_pvf_path, "-vn", "-c:a", "copy", tmp_path / (files_name+"_PreservationAudioVisualFile_output_audio.wav")])
    subprocess.run(["ffmpeg", "-i", output_pvf_path, "-an", "-c:v", "copy", tmp_path / (files_name+"_PreservationAudioVisualFile_output_video.mov")])
    input_paf_path = working_path / "PreservationAudioFile" / (files_name+".wav")
    input_fingerprint = acoustid.fingerprint_file(input_paf_path)
    output_fingerprint = acoustid.fingerprint_file(tmp_path / (files_name+"_PreservationAudioVisualFile_output_audio.wav"))  # audio
    audio_similarity = acoustid.compare_fingerprints(input_fingerprint, output_fingerprint)
    print("audio_similarity=", audio_similarity)
    assert audio_similarity > AUDIO_THRESHOLD, "PreservationAudioVisualFile.mov audio is not the same as PreservationAudioFile.wav"
    psnr_out = subprocess.run(["ffmpeg",    # video
                               "-i", input_pvf_path,
                               "-i", tmp_path / (files_name+"_PreservationAudioVisualFile_output_video.mov"),
                               "-filter_complex", "psnr",
                               "-f", "null",
                               "-"],
                              capture_output=True)
    psnr_out = psnr_out.stderr.decode("utf-8")
    psnr = psnr_out[psnr_out.find('average:') + 8:psnr_out.find(' ', psnr_out.find('average:'))]
    print("psnr_out=", psnr)
    assert psnr == 'inf' or float(psnr) > VIDEO_THRESHOLD, "PreservationAudioVisualFile.mov is not the same as input"   # psnr is calculated over PreservationAudioVisualFile.mov which is not exactly the same as input since the video can be shifted by the offset in order to sync with the audio, for this reason we allow a psnr < inf and also not always really high
    
    # DS8 files equality check
    test_pvf_path = oldify(pmf_path) / files_name / "PreservationAudioVisualFile.mov"
    subprocess.run(["ffmpeg", "-i", test_pvf_path, "-vn", "-c:a", "copy", tmp_path / (files_name+"_PreservationAudioVisualFile_test_audio.wav")])
    subprocess.run(["ffmpeg", "-i", test_pvf_path, "-an", "-c:v", "copy", tmp_path / (files_name+"_PreservationAudioVisualFile_test_video.mov")])
    test_fingerprint = acoustid.fingerprint_file(tmp_path / (files_name+"_PreservationAudioVisualFile_test_audio.wav"))  # audio
    audio_similarity = acoustid.compare_fingerprints(output_fingerprint, test_fingerprint)
    print("audio_similarity_test=", audio_similarity)
    assert audio_similarity > AUDIO_THRESHOLD, "PreservationAudioVisualFile.mov audio is not the same as test dataset's"
    psnr_out = subprocess.run(["ffmpeg",    # video
                               "-i", tmp_path / (files_name+"_PreservationAudioVisualFile_output_video.mov"),
                               "-i", tmp_path / (files_name+"_PreservationAudioVisualFile_test_video.mov"),
                               "-filter_complex", "psnr",
                               "-f", "null",
                               "-"],
                              capture_output=True)
    psnr_out = psnr_out.stderr.decode("utf-8")
    psnr = psnr_out[psnr_out.find('average:') + 8:psnr_out.find(' ', psnr_out.find('average:'))]
    print("psnr_test=", psnr)
    assert psnr == 'inf' or float(psnr) > VIDEO_THRESHOLD, "PreservationAudioVisualFile.mov is not the same as test dataset's"


# noinspection DuplicatedCode
@pytest.mark.parametrize("files_name", files_names)
def test_irregularity_file(files_name: str):
    """
    Test `IrregularityFile.json`.

    Parameters
    ----------
    files_name : str
        The name of the files to test.
    """
    # after packager run checks
    input_if_path = working_path / "temp" / files_name / "TapeIrregularityClassifier_IrregularityFileOutput2.json"
    output_if_path = pmf_path / files_name / "IrregularityFile.json"
    assert output_if_path.is_file(), "IrregularityFile.json not found"
    with open(input_if_path, "r") as input_if_file:
        input_if_dict = json.load(input_if_file)
    with open(output_if_path, "r") as output_if_file:
        output_if_dict = json.load(output_if_file)
    assert input_if_dict == output_if_dict, "IrregularityFile.json is not the same as input"

    # DS8 files equality check
    test_if_path = oldify(pmf_path) / files_name / "IrregularityFile.json"
    with open(test_if_path, "r") as test_if_file:
        test_if_dict = json.load(test_if_file)
    assert output_if_dict == test_if_dict, "IrregularityFile.json is not the same as test dataset's"


# noinspection DuplicatedCode
@pytest.mark.parametrize("files_name", files_names)
def test_irregularity_images(files_name: str, tmp_path):
    """
    Test `IrregularityImages.zip`.
    
    Parameters
    ----------
    files_name : str
        The name of the files to test.
    """
    # after packager run checks
    input_ii_path = working_path / "temp" / files_name / "IrregularityImages"
    output_ii_path = pmf_path / files_name / "IrregularityImages.zip"
    assert output_ii_path.is_file(), "IrregularityImages.zip not found"
    shutil.unpack_archive(output_ii_path, tmp_path, "zip")
    shutil.move(tmp_path / "IrregularityImages", tmp_path / (files_name+"_IrregularityImages_output"))
    output_ii_path = tmp_path / (files_name+"_IrregularityImages_output")
    assert sorted(os.listdir(input_ii_path)) == sorted(os.listdir(output_ii_path)), "IrregularityImages file tree is not the same as input"
    for file in os.listdir(input_ii_path):
        assert filecmp.cmp(input_ii_path / file, output_ii_path / file), f'IrregularityImages {file} is not the same as input'

    # DS8 files equality check
    test_ii_path = oldify(pmf_path) / files_name / "IrregularityImages.zip"
    shutil.unpack_archive(test_ii_path, tmp_path, "zip")
    shutil.move(tmp_path / "IrregularityImages", tmp_path / (files_name + "_IrregularityImages_ds7"))
    test_ii_path = tmp_path / (files_name + "_IrregularityImages_ds7")
    assert sorted(os.listdir(test_ii_path)) == sorted(os.listdir(output_ii_path)), "IrregularityImages file tree is not the same as dataset's"
    for file in os.listdir(test_ii_path):
        assert filecmp.cmp(output_ii_path / file, test_ii_path / file), f"IrregularityImages {file} is not the same as dataset's"
