"""
MPAI CAE-ARP Packager.

Implements MPAI CAE-ARP Packager Technical Specification, providing:
- Access Copy Files:Images
  1. Restored Audio Files.
  2. Editing List.
  3. Set of Irregularity Images in a .zip file.
  4. Irregularity File.
- Preservation Master Files:
  1. Preservation Audio File.
  2. Preservation Audio-Visual File where the audio has been replaced with the Audio of the Preservation Audio File
     fully synchronised with the video.
  3. Set of Irregularity Images in a .zip file.
  4. Irregularity File.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from enum import Enum
from mpai_cae_arp.io import Color, pprint

PathType_str = str | os.PathLike[str] | Path

__copyright__ = "Copyright 2022, Audio Innova S.r.l."
__credits__ = ["Niccolò Pretto", "Nadir Dalla Pozza", "Sergio Canazza"]
__status__ = "Production"


class ReturnCode(Enum):
    """
    Return codes
    """
    SUCCESS = 0
    WARNING = 1
    ERROR = 2


def make_dir(dir_path: PathType_str) -> bool:
    """
    Decide if the given directory has to be created or should be overridden.

    Parameters
    ----------
    dir_path : PathType_str
        The path of the directory to be created.

    Returns
    -------
    bool
        True if the directory has to be created, False otherwise.
    """
    dir_path = Path(dir_path)
    if not dir_path.exists():
        # Create directory
        dir_path.mkdir(parents=True)
        print("Directory '% s' created" % dir_path)
        return True
    else:
        pprint(f"Directory '{dir_path}' already exists!", color=Color.YELLOW)
        overwrite = input('Do you want to overwrite it? [y/n]: ')
        if overwrite.casefold() == 'y':
            # Overwrite directory
            shutil.rmtree(dir_path)
            dir_path.mkdir(parents=True)
            print('%s overwritten' % dir_path)
            return True
        elif overwrite.casefold() != 'n':
            pprint('Unknown command, exiting', color=Color.RED)
            if not sys.platform.startswith(('win', 'cygwin')):
                quit(os.EX_CONFIG)  # `os.EX_CONFIG` is not compatible with the above platforms in Python 3.10
            else:
                quit()
    return False


def copy_restored_audio_files(temp_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Copy RestoredAudioFiles directory from temp_path to acf_path / 'RestoredAudioFiles'.

    Parameters
    ----------
    temp_path : PathType_str
        The path of the 'temp' directory.
    dest_path : PathType_str
        The path of the AccessCopyFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    return_code = ReturnCode.SUCCESS
    message = "Restored Audio Files copied"
    
    temp_path = Path(temp_path)
    dest_path = Path(dest_path)
    raf_path = temp_path / 'RestoredAudioFiles'
    if not raf_path.exists():
        return ReturnCode.ERROR, f"Restored Audio Files directory '{raf_path}' not found!"
    restored_audio_files = os.listdir(raf_path)
    if len(restored_audio_files) == 1:
        return_code = ReturnCode.WARNING
        message = f"Restored Audio Files directory '{raf_path}' is empty!"
    shutil.copytree(raf_path, dest_path / 'RestoredAudioFiles')
    return return_code, message


def copy_editing_list(temp_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Copy EditingList.json file from temp_path to acf_path.

    Parameters
    ----------
    temp_path : PathType_str
        The path of the 'temp' directory.
    dest_path : PathType_str
        The path of the AccessCopyFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    temp_path = Path(temp_path)
    dest_path = Path(dest_path)
    
    el_path = temp_path / 'EditingList.json'
    try:
        shutil.copy2(el_path, dest_path)
    except FileNotFoundError:
        return ReturnCode.ERROR, f"Editing List file '{el_path}' not found!"
    return ReturnCode.SUCCESS, "Editing List copied"


def create_irregularity_images_archive(temp_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Create IrregularityImages.zip archive in acf_path from temp_path IrregularityImages directory.

    Parameters
    ----------
    temp_path : PathType_str
        The path of the 'temp' directory.
    dest_path : PathType_str
        The path of the AccessCopyFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    return_code = ReturnCode.SUCCESS
    message = "Restored Audio Files copied"
    
    temp_path = Path(temp_path)
    dest_path = Path(dest_path)

    ii_path = temp_path / 'IrregularityImages'
    if not ii_path.exists():
        return ReturnCode.ERROR, f"Irregularity Images directory '{ii_path}' not found!"
    irregularity_images = os.listdir(ii_path)
    if len(irregularity_images) == 1:
        return_code = ReturnCode.WARNING
        message = f"Irregularity Images directory '{ii_path}' is empty!"
    shutil.make_archive(str(dest_path / 'IrregularityImages'), 'zip', temp_path, 'IrregularityImages')
    return return_code, message


def copy_irregularity_file(temp_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Copy TapeIrregularityClassifier_IrregularityFileOutput2.json file from temp_path to acf_path / 'IrregularityFile.json'.

    Parameters
    ----------
    temp_path : PathType_str
        The path of the 'temp' directory.
    dest_path : PathType_str
        The path of the AccessCopyFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    temp_path = Path(temp_path)
    dest_path = Path(dest_path)

    if_path = temp_path / 'TapeIrregularityClassifier_IrregularityFileOutput2.json'
    try:
        shutil.copy2(if_path, dest_path / 'IrregularityFile.json')
    except FileNotFoundError:
        return ReturnCode.ERROR, f"Irregularity File file '{if_path}' not found!"
    return ReturnCode.SUCCESS, "Irregularity File copied"


def copy_preservation_audio_file(files_name: str, working_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Copy PreservationAudioFile.wav file from temp_path to pmf_path.

    Parameters
    ----------
    files_name : str
        The name of the files (tape).
    working_path : PathType_str
        The path of the working directory.
    dest_path : PathType_str
        The path of the PreservationMasterFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    working_path = Path(working_path)
    dest_path = Path(dest_path)

    audio_file = files_name + '.wav'
    paf_path = working_path / 'PreservationAudioFile' / audio_file
    try:
        shutil.copy2(paf_path, dest_path / 'PreservationAudioFile.wav')
    except FileNotFoundError:
        return ReturnCode.ERROR, f"Preservation Audio File file '{paf_path}' not found!"
    return ReturnCode.SUCCESS, "Preservation Audio File copied"


def create_preservation_audio_visual_file(files_name: str, working_path: PathType_str, temp_path: PathType_str, dest_path: PathType_str) -> tuple[ReturnCode, str]:
    """
    Create PreservationAudioVisualFile.mov file in pmf_path from PreservationAudioFile.wav and VideoFile.mov.

    Parameters
    ----------
    files_name : str
        The name of the files (tape).
    working_path : PathType_str
        The path of the working directory.
    temp_path : PathType_str
        The path of the 'temp' directory.
    dest_path : PathType_str
        The path of the PreservationMasterFiles directory.

    Returns
    -------
    tuple[ReturnCode, str]
        A tuple consisting of: 1) ReturnCode; 2) str representing the message to print.
    """
    working_path = Path(working_path)
    temp_path = Path(temp_path)
    dest_path = Path(dest_path)

    audio_file = files_name + '.wav'
    paf_path = working_path / 'PreservationAudioFile' / audio_file
    video_file = files_name + '.mov'
    pvf_path = working_path / 'PreservationAudioVisualFile' / video_file
    
    if not paf_path.exists():
        return ReturnCode.ERROR, f"Preservation Audio File file '{paf_path}' not found!"
    if not pvf_path.exists():
        return ReturnCode.ERROR, f"Preservation Audio-Visual File file '{pvf_path}' not found!"
    try:
        # Open Irregularity File to get offset
        irregularity_file_json = open(temp_path / 'TapeIrregularityClassifier_IrregularityFileOutput2.json')
    except OSError:
        return ReturnCode.ERROR, f"Irregularity File not found!"

    irregularity_file = json.load(irregularity_file_json)
    offset = irregularity_file['Offset']
    command_to_run = ['ffmpeg',
                      '-y', '-hide_banner', '-loglevel', 'error']
    # If offset is positive, the audio is anticipated, otherwise video is anticipated (through seek)
    if offset > 0:
        command_to_run = command_to_run + ['-i', pvf_path,
                                           '-ss', str(offset) + 'ms', '-i', paf_path]
    else:
        command_to_run = command_to_run + ['-ss', str(offset * -1) + 'ms', '-i', pvf_path,
                                           '-i', paf_path]
    command_to_run = command_to_run + ['-c:v', 'mpeg4', '-c:a', 'copy',
                                       '-map', '0:v', '-map', '1:a',
                                       '-b:v', '3M', '-maxrate', '4M', '-bufsize', '4M',
                                       str(dest_path / 'PreservationAudioVisualFile.mov')]
    subprocess.run(command_to_run)
    return ReturnCode.SUCCESS, "Preservation Audio-Visual File created"
