"""
Test Access Copy Files
"""

import pytest
import os
import acoustid
import json
import shutil
import filecmp
from conftest import working_path, acf_path, files_names, oldify


@pytest.mark.parametrize("files_name", files_names)
def test_restored_audio_files(files_name: str):
    """
    Test `RestoredAudioFiles`.

    Parameters
    ----------
    files_name : str
        Name of the files to test.
    """
    # after packager run checks
    input_raf_path = working_path / "temp" / files_name / "RestoredAudioFiles"
    output_raf_path = acf_path / files_name / "RestoredAudioFiles"
    assert output_raf_path.is_dir(), "RestoredAudioFiles not found"
    assert sorted(os.listdir(input_raf_path)) == sorted(os.listdir(output_raf_path)), "RestoredAudioFiles file tree is not the same as input"
    for file in os.listdir(input_raf_path):
        input_fingerprint = acoustid.fingerprint_file(input_raf_path / file)
        output_fingerprint = acoustid.fingerprint_file(output_raf_path / file)
        assert acoustid.compare_fingerprints(input_fingerprint, output_fingerprint) > 0.7, f'RestoredAudioFiles {file} is not the same as input'

    # DS7 files equality check
    test_raf_path = oldify(acf_path) / files_name / "RestoredAudioFiles"
    for file in os.listdir(test_raf_path):
        output_fingerprint = acoustid.fingerprint_file(output_raf_path / file)
        test_fingerprint = acoustid.fingerprint_file(test_raf_path / file)
        assert acoustid.compare_fingerprints(output_fingerprint, test_fingerprint) > 0.7, f"RestoredAudioFiles {file} is not the same as test dataset's"


@pytest.mark.parametrize("files_name", files_names)
def test_editing_list(files_name: str):
    """
    Test `EditingList.json`.

    Parameters
    ----------
    files_name : str
        Name of the files to test.
    """
    # after packager run checks
    input_el_path = working_path / "temp" / files_name / "EditingList.json"
    output_el_path = acf_path / files_name / "EditingList.json"
    assert output_el_path.is_file(), "EditingList.json not found"
    with open(input_el_path, "r") as input_el_file:
        input_el_dict = json.load(input_el_file)
    with open(output_el_path, "r") as output_el_file:
        output_el_dict = json.load(output_el_file)
    assert input_el_dict == output_el_dict, "EditingList.json is not the same as input"

    # DS7 equality check
    test_el_path = oldify(acf_path) / files_name / "EditingList.json"
    with open(test_el_path, "r") as test_el_file:
        test_el_dict = json.load(test_el_file)
    assert output_el_dict == test_el_dict, "EditingList.json is not the same as test dataset's"


# noinspection DuplicatedCode
@pytest.mark.parametrize("files_name", files_names)
def test_irregularity_file(files_name: str):
    """
    Test `IrregularityFile.json`.

    Parameters
    ----------
    files_name : str
        Name of the files to test.
    """
    # after packager run checks
    input_if_path = working_path / "temp" / files_name / "TapeIrregularityClassifier_IrregularityFileOutput2.json"
    output_if_path = acf_path / files_name / "IrregularityFile.json"
    assert output_if_path.is_file(), "IrregularityFile.json not found"
    with open(input_if_path, "r") as input_if_file:
        input_if_dict = json.load(input_if_file)
    with open(output_if_path, "r") as output_if_file:
        output_if_dict = json.load(output_if_file)
    assert input_if_dict == output_if_dict, "IrregularityFile.json is not the same as input"

    # DS7 equality check
    test_if_path = oldify(acf_path) / files_name / "IrregularityFile.json"
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
        Name of the files to test.
    """
    # after packager run checks
    input_ii_path = working_path / "temp" / files_name / "IrregularityImages"
    output_ii_path = acf_path / files_name / "IrregularityImages.zip"
    assert output_ii_path.is_file(), "IrregularityImages.zip not found"
    shutil.unpack_archive(output_ii_path, tmp_path, "zip")
    shutil.move(tmp_path / "IrregularityImages", tmp_path / (files_name+"_IrregularityImages_output"))
    output_ii_path = tmp_path / (files_name+"_IrregularityImages_output")
    assert sorted(os.listdir(input_ii_path)) == sorted(os.listdir(output_ii_path)), "IrregularityImages file tree is not the same as input"
    for file in os.listdir(input_ii_path):
        assert filecmp.cmp(input_ii_path / file, output_ii_path / file), f'IrregularityImages {file} is not the same as input'

    # DS7 equality check
    test_ii_path = oldify(acf_path) / files_name / "IrregularityImages.zip"
    shutil.unpack_archive(test_ii_path, tmp_path, "zip")
    shutil.move(tmp_path / "IrregularityImages", tmp_path / (files_name+"_IrregularityImages_test"))
    test_ii_path = tmp_path / (files_name+"_IrregularityImages_test")
    assert sorted(os.listdir(test_ii_path)) == sorted(os.listdir(output_ii_path)), "IrregularityImages file tree is not the same as dataset's"
    for file in os.listdir(test_ii_path):
        assert filecmp.cmp(output_ii_path / file, test_ii_path / file), f"IrregularityImages {file} is not the same as dataset's"
