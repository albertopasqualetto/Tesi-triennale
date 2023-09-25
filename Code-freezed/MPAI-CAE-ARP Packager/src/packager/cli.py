#!./venv/bin/activate

import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from mpai_cae_arp.io import Color, Style, pprint

from packager import lib

from packager.lib import PathType_str

__copyright__ = "Copyright 2022, Audio Innova S.r.l."
__credits__ = ["Niccolò Pretto", "Nadir Dalla Pozza", "Sergio Canazza"]
__status__ = "Production"


def get_arguments() -> tuple[PathType_str, str]:
    """
    Method to obtain arguments from environment or command line.
    Defaults to environment variables, ignored if a command line argument is passed.

    Returns
    -------
    tuple[PathType_str, str]
        A tuple containing:
            1) the working path;
            2) the name of the Preservation files, which is key element to retrieve necessary files.
    """
    if len(sys.argv) > 1:
        # Read from command line
        parser = ArgumentParser(
            prog="python3 packager.py",
            formatter_class=RawTextHelpFormatter,
            description="A tool that implements MPAI CAE-ARP Packager Technical Specification.\n"
                        "By default, the configuration parameters are loaded from ./config/args.yaml file,\n"
                        "but, alternately, you can pass command line arguments to replace them."
        )
        parser.add_argument(
            "-w",
            "--working-path",
            help="Specify the Working Path, where all input files are stored",
            required=True
        )
        parser.add_argument(
            "-f",
            "--files-name",
            help="Specify the name of the Preservation files (without extension)",
            required=True
        )
        args = parser.parse_args()
        working_path = args.working_path
        files_name = args.files_name
    else:
        arg_names = ['WORKING_PATH', 'FILES_NAME']
        config = {argument: os.getenv(argument) for argument in arg_names}
        working_path, files_name = map(config.get, arg_names)

        if any(value is None for value in config.values()):
            raise ValueError("Please, set the environment variables: WORKING_PATH, FILES_NAME")

    return Path(working_path), files_name


def check_input(working_path: PathType_str, files_name: str) -> PathType_str:
    """
    Method to check that passed arguments are correct and that the environment is conformant to the standard.

    Parameters
    ----------
    working_path : PathType_str
        The path where all input files are stored.
    files_name : str
        The name of the Preservation files, which is key element to retrieve necessary files.

    Returns
    -------
    PathType_str
        The path where files to be processed are stored.
    """
    working_path = Path(working_path)

    if not working_path.exists():
        check_return_code(lib.ReturnCode.ERROR, 'The specified WORKING_PATH is non-existent!')
    # Check for temp directory existence
    temp_path = working_path / 'temp'
    if not temp_path.exists():
        check_return_code(lib.ReturnCode.ERROR, 'WORKING_PATH structure is not conformant!')
    # Check for input directory existence
    files_name_path = temp_path / files_name
    if not files_name_path.exists():
        check_return_code(lib.ReturnCode.ERROR, 'The specified FILES_NAME has no corresponding files!')
    return files_name_path


def check_return_code(return_code: lib.ReturnCode, message: str) -> None:
    """
    Check if there are problems from `return_code` and print them.
    
    Parameters
    ----------
    return_code : lib.ReturnCode
        Represents the return code of the function.
    message : str
        Represents the message to print.

    Returns
    -------
    None
    """
    match return_code:
        case lib.ReturnCode.ERROR:
            pprint(message, color=Color.RED)
            if not sys.platform.startswith(('win', 'cygwin')):
                quit(os.EX_CONFIG)  # `os.EX_CONFIG` is not compatible with the above platforms in Python 3.10
            else:
                quit()
        case lib.ReturnCode.WARNING:
            pprint(message, color=Color.YELLOW)
        case _:
            return None


def main() -> None:
    """
    Main execution method.

    Returns
    -------
    None
    """
    pprint('\nWelcome to ARP Packager!', styles=[Style.BOLD])
    print(f"You are using Python version: {sys.version}")

    # Get the input from config/args.yaml or command line
    working_path, files_name = get_arguments()
    working_path = Path(working_path)
    # Check if input is correct
    temp_path = check_input(working_path, files_name)
    temp_path = Path(temp_path)

    # Access Copy Files
    pprint('\nCreation of Access Copy Files...', styles=[Style.BOLD])

    # By default, AccessCopyFiles directory is created in the output path...
    acf_path = working_path / 'AccessCopyFiles' / files_name
    # ...however, if it already exists, the user can decide if it has to be overridden
    make_acf = lib.make_dir(acf_path)

    if make_acf:
        # Copy RestoredAudioFiles
        return_code, message = lib.copy_restored_audio_files(temp_path, acf_path)
        check_return_code(return_code, message)
        print("Restored Audio Files copied")

        # Copy Editing List
        return_code, message = lib.copy_editing_list(temp_path, acf_path)
        check_return_code(return_code, message)
        print("Editing List copied")

        # Create Irregularity Images archive
        return_code, message = lib.create_irregularity_images_archive(temp_path, acf_path)
        check_return_code(return_code, message)
        print("Irregularity Images archive created")

        # Copy Irregularity File
        return_code, message = lib.copy_irregularity_file(temp_path, acf_path)
        check_return_code(return_code, message)
        print("Irregularity File copied")

        # End Access Copy Files
        pprint('Success!', color=Color.GREEN, styles=[Style.BOLD])


    # Preservation Master Files
    pprint('\nCreation of Preservation Master Files...', styles=[Style.BOLD])

    # By default, PreservationMasterFiles directory is created in the output path...
    pmf_path = Path(working_path / 'PreservationMasterFiles' / files_name)
    # ...however, if it already exists, it is possible to skip its creation
    make_pmf = lib.make_dir(pmf_path)

    if make_pmf:
        # Copy Preservation Audio File
        return_code, message = lib.copy_preservation_audio_file(files_name, working_path, pmf_path)
        check_return_code(return_code, message)
        print("Preservation Audio File copied")

        # Create Preservation Audio-Visual File with substituted audio
        return_code, message = lib.create_preservation_audio_visual_file(files_name, working_path, temp_path, pmf_path)
        check_return_code(return_code, message)
        print("Preservation Audio-Visual File created")

        # Create Irregularity Images archive
        return_code, message = lib.create_irregularity_images_archive(temp_path, pmf_path)
        check_return_code(return_code, message)
        print("Irregularity Images archive created")

        # Copy Irregularity File
        return_code, message = lib.copy_irregularity_file(temp_path, pmf_path)
        check_return_code(return_code, message)
        print("Irregularity File copied")

        # End Preservation Master Files
        pprint('Success!\n', color=Color.GREEN, styles=[Style.BOLD])

    else:
        print("\nExit")


if __name__ == '__main__':
    main()
