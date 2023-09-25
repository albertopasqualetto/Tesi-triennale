"""
n of each DS
Inputs:
    - DS1: Preservation Audio File
    - DS2: Preservation Audio-Visual File
    - DS3: Irregularity File

Outputs:
    - DS4: Irregularity File (IrregularityFileOutput_1)
    - DS4: Irregularity File (IrregularityFileOutput_2) 


WILL TEST ALL FILES IN 'PreservationAudioFile' FOLDER
AN AIM IS ACCEPTED AVERAGE RECALL AND PRECISION ARE ABOVE 0.9
A REASONABLE n FOR TESTING IS 5<n<=10, since each file generates multiple irregularities to classify

one tape is 'files_name'

psnr is used for video comparison
hashing algorithms, filecmp.cmp and wave does not work in audio comparison
"""

import pytest
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from mpai_cae_arp.io import pprint, Color
import json
import tempfile


if os.getenv('WORKING_PATH') is None:
    os.environ['WORKING_PATH'] = "../data"
working_path = Path(os.getenv('WORKING_PATH'))
temp_path = working_path / "temp"
files_names = [file.split(".")[0] for file in os.listdir(working_path / "PreservationAudioFile")]

ACCEPTANCE_THRESHOLD = 0.9


def check_n(n_files=files_names, start=5, end=10):
    if not 0 < start < end:
        raise ValueError("start must be less than end and greater than 0")
    if not start < len(n_files) < end:
        pprint(f"WARNING: n={len(n_files)} is not a reasonable number of files to test, they should be between {start} and {end}; continuing anyway", color=Color.YELLOW)


def pytest_sessionstart(session):
    """Setup that occurs only once here"""
    if not hasattr(session.config, "workerinput"):  # if master node
        setup()


def pytest_sessionfinish(session, exitstatus):
    """Teardown that occurs only once here"""
    if not hasattr(session.config, "workerinput"):  # if master node
        teardown()


def setup():
    check_n(files_names)

    cli_path = Path(__file__).parent.parent.joinpath("src", "audio_analyzer", "cli.py")
    
    for files_name in files_names:
        aa_if1_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json"
        aa_if2_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json"
        ab_path = temp_path / files_name / "AudioBlocks"

        # rename Irregularity files and AudioBlocks folder
        try:
            os.remove(oldify(aa_if1_path))
        except FileNotFoundError:
            pass
        try:
            os.remove(oldify(aa_if2_path))
        except FileNotFoundError:
            pass
        shutil.rmtree(oldify(ab_path), ignore_errors=True)

        try:
            shutil.move(aa_if1_path, oldify(aa_if1_path))
            shutil.move(aa_if2_path, oldify(aa_if2_path))
        except FileNotFoundError:
            teardown()
            pytest.exit("ERROR: DS4 and DS5 (Irregularity files) not found", pytest.ExitCode.INTERNAL_ERROR)
        try:
            shutil.move(ab_path, oldify(ab_path))
        except FileNotFoundError:
            print(f"Passing {files_name} AudioBlocks folder renaming to old because non-old folder not found")

        # run packager for each tape in PreservationAudioFile folder
        subprocess.run([sys.executable, str(cli_path), "-w", working_path, "-f", files_name])


def teardown():
    for files_name in files_names:
        aa_if1_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json"
        aa_if2_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json"
        ab_path = temp_path / files_name / "AudioBlocks"
        # delete AccessCopyFiles and PreservationMasterFiles folders
        try:
            os.remove(aa_if1_path)
            os.remove(aa_if2_path)
            shutil.rmtree(ab_path)
        except FileNotFoundError:
            print(f"passing {files_name} folders created by the packager deletion because it failed to run")
        shutil.move(oldify(aa_if1_path), aa_if1_path)
        shutil.move(oldify(aa_if2_path), aa_if2_path)
        shutil.move(oldify(ab_path), ab_path)


def calculate_avg_recall_precision() -> tuple[float, float]:
    """
    Calculate average recall and precision from `aa_measures.json` file in temp folder.

    Returns
    -------
    tuple[float, float]
        Tuple of 1) average recall and 2) average precision.
    """
    root_tmp_dir = Path(tempfile.gettempdir()) / "mpai"
    with open(root_tmp_dir / "aa_measures.json", "r") as measures_file:
        measures_dict = json.load(measures_file)
    avg_recall = sum([measure["recall"] for measure in measures_dict]) / len(measures_dict)
    avg_precision = sum([measure["precision"] for measure in measures_dict]) / len(measures_dict)
    return avg_recall, avg_precision


def get_all_files_measures_merged() -> dict:
    """
    Merge all `*_measures.json` files in temp folder.

    Returns
    -------
    dict
        Merged dictionary of all measures.
    """
    root_tmp_dir = Path(tempfile.gettempdir()) / "mpai" / "aa_conformance_test"
    merged_dict = {}
    for file in os.listdir(root_tmp_dir):
        if file.endswith("measures.json") and file != "merged_measures.json":
            with open(root_tmp_dir / file, "r") as measures_file:
                measures_dict = json.load(measures_file)
            file_name = file.rsplit("_", maxsplit=1)[0]
            merged_dict.update({file_name: measures_dict})
    # also save merged json
    with open(root_tmp_dir / "merged_measures.json", "w") as merged_measures_file:
        json.dump(merged_dict, merged_measures_file)
    return merged_dict


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    json_report['conformance_tester_id'] = ''
    json_report['standard_usecaseid_version'] = 'CAE:ARP:1.0'
    json_report['name_of_aim'] = 'Audio Analyser'
    json_report['implementer_id'] = ''
    json_report['neural_network_version'] = ''
    json_report['identifier_of_conformance_testing_dataset'] = ''
    json_report['test_id'] = ''  # TODO ?

    """
    format of actual_output:
    actual_output = {"BERIO100":
                         {"recall": 0.9,
                            "precision": 0.9},
                     "BERIO052":
                         {"recall": 0.9,
                            "precision": 0.9}
                     }
    """

    actual_output = get_all_files_measures_merged()
    recalls = [float(files_name["recall"]) for files_name in actual_output.values()]
    precisions = [float(files_name["precision"]) for files_name in actual_output.values()]
    avg_recall = sum(recalls) / len(recalls)
    avg_precision = sum(precisions) / len(precisions)
    pprint(f"Average Recall={avg_recall} - it is {'above' if avg_recall > ACCEPTANCE_THRESHOLD else 'below'} the acceptance threshold", color=Color.GREEN if avg_recall > ACCEPTANCE_THRESHOLD else Color.RED)
    pprint(f"Average Precision={avg_precision} - it is {'above' if avg_precision > ACCEPTANCE_THRESHOLD else 'below'} the acceptance threshold", color=Color.GREEN if avg_precision > ACCEPTANCE_THRESHOLD else Color.RED)

    json_report['actual_output'] = actual_output

    json_report['execution_time'] = json_report['duration']
    json_report['test_comment'] = ''
    json_report['test_date'] = str(datetime.fromtimestamp(json_report['created']).strftime("%Y/%m/%d"))

    del json_report['created']
    del json_report['duration']
    del json_report['exitcode']
    del json_report['root']
    del json_report['environment']
    del json_report['summary']
    if 'collectors' in json_report.keys():
        del json_report['collectors']
    if 'tests' in json_report.keys():
        del json_report['tests']
    if 'warnings' in json_report.keys():
        del json_report['warnings']


def oldify(path: str | os.PathLike | Path) -> Path:
    """
    Rename a file or folder to its "old" version.

    Parameters
    ----------
    path : str | os.PathLike | Path
        Path to file or folder.

    Returns
    -------
    Path
        Path to "old" file or folder.
    """
    if path.is_file():
        return Path(str(path) + ".old")
    elif path.is_dir():
        return Path(str(path) + "_old")
    else:
        if path.suffix.startswith('.'):
            return Path(str(path) + ".old")
        elif path.suffix == '':
            return Path(str(path) + "_old")
