"""
n of each DS
Inputs:
    - DS1: Preservation Audio File
    - DS2: Preservation Audio-Visual File
    - DS3: Restored Audio Files 
    - DS4: Editing List 
    - DS5: Irregularity File
    - DS6: Irregularity Images

Outputs:
    - DS7: Access Copy Files
    - DS8: Preservation Master Files 


inputs -> datasets folder
outputs -> packager output folder

WILL TEST ALL FILES IN 'PreservationAudioFile' FOLDER

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
from collections import defaultdict

if os.getenv('WORKING_PATH') is None:
    os.environ['WORKING_PATH'] = "../data"
working_path = Path(os.getenv('WORKING_PATH'))
acf_path = working_path / "AccessCopyFiles"
pmf_path = working_path / "PreservationMasterFiles"

files_names = [file.split(".")[0] for file in os.listdir(working_path / "PreservationAudioFile")]

AUDIO_THRESHOLD = 0.7
VIDEO_THRESHOLD = 25


def pytest_sessionstart(session):
    """Setup that occurs only once here"""
    if not hasattr(session.config, "workerinput"):  # if master node
        setup()


def pytest_sessionfinish(session, exitstatus):
    """Teardown that occurs only once here"""
    if not hasattr(session.config, "workerinput"):  # if master node
        teardown()


def setup():
    # rename AccessCopyFiles and PreservationMasterFiles folders
    shutil.rmtree(oldify(acf_path), ignore_errors=True)
    shutil.rmtree(oldify(pmf_path), ignore_errors=True)
    try:
        shutil.move(acf_path, oldify(acf_path))
        shutil.move(pmf_path, oldify(pmf_path))
    except FileNotFoundError:
        teardown()
        pytest.exit("ERROR: DS7 (Access Copy Files) and DS8 (Preservation Master Files) not found", pytest.ExitCode.INTERNAL_ERROR)

    # run packager for each tape in PreservationAudioFile folder
    cli_path = Path(__file__).parent.parent.joinpath("src", "packager", "cli.py")
    for file in files_names:
        subprocess.run([sys.executable, str(cli_path), "-w", working_path, "-f", file])


def teardown():
    # delete AccessCopyFiles and PreservationMasterFiles folders
    try:
        shutil.rmtree(acf_path)
        shutil.rmtree(pmf_path)
    except FileNotFoundError:
        print("passing folders created by the packager deletion because it failed to run")
    shutil.move(oldify(acf_path), acf_path)
    shutil.move(oldify(pmf_path), pmf_path)


@pytest.hookimpl(optionalhook=True)
def pytest_json_modifyreport(json_report):
    json_report['conformance_tester_id'] = ''
    json_report['standard_usecaseid_version'] = 'CAE:ARP:1.0'
    json_report['name_of_aim'] = 'Packager'
    json_report['implementer_id'] = ''
    json_report['neural_network_version'] = ''
    json_report['identifier_of_conformance_testing_dataset'] = ''
    json_report['test_id'] = ''  # TODO ?

    """
    format of actual_output:
    actual_output = {"BERIO100":
                         {"access_copy_files":
                              {"restored_audio_files": True,
                               "editing_list": True,
                               "irregularity_file": True,
                               "irregularity_images": True},
                          "preservation_master_files":
                              {"preservation_audio_file": True,
                               "preservation_audio_visual_file": True,
                               "irregularity_file": True,
                               "irregularity_images": True},
                          "final_assertion": True},
                     "BERIO052":
                         {"access_copy_files":
                              {"restored_audio_files": True,
                               "editing_list": True,
                               "irregularity_file": True,
                               "irregularity_images": True},
                          "preservation_master_files":
                              {"preservation_audio_file": True,
                               "preservation_audio_visual_file": True,
                               "irregularity_file": True,
                               "irregularity_images": True},
                          "final_assertion": True}
                     }
    """

    actual_output = defaultdict(lambda: defaultdict(dict))
    for node in json_report['tests']:
        output = (((node['nodeid'].split("::")[0]).split('/')[-1]).split('test_')[1]).split('.py')[0]
        test_name = ((node['nodeid'].split("::")[1]).split('[')[0]).split('test_')[1]
        files_name = node['nodeid'].split("[")[1].split(']')[0]
        assertion = node['outcome'] == 'passed'

        actual_output[files_name][output][test_name] = assertion

    # noinspection PyTypeChecker
    actual_output['final_assertion'] = json_report['summary']['passed'] == json_report['summary']['total']

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
