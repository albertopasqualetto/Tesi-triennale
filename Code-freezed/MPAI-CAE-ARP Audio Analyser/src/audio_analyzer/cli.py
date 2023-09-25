import argparse
import os
import sys
from rich.console import Console

from mpai_cae_arp.types.irregularity import IrregularityFile, Source
from mpai_cae_arp.files import File, FileType
from mpai_cae_arp.io import prettify, Style

import audio_analyzer.segment_finder as sf
import audio_analyzer.classifier as cl


def get_args() -> tuple[str | None, str | None]:
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            prog="audio-analyzer",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=f"A tool that implements {prettify('MPAI CAE-ARP Audio Analyser', styles=[Style.BOLD])} Technical Specification.",
            epilog="For support, please contact Matteo Spanio <dev2@audioinnova.com>.\n"
                 "This software is licensed under the GNU General Public License v3.0."
        )
        parser.add_argument("--working-directory", "-w", help="The path were the AIW will find and save the files")
        parser.add_argument("--files-name", "-f", help=f"The name of the files to be analyzed {prettify('without extension', styles=[Style.UNDERLINE])}")
        args = parser.parse_args()
        return args.working_directory, args.files_name
    else:
        return os.getenv("WORKING_DIRECTORY"), os.getenv("FILES_NAME")


def exit_with_error(error_message: str, console) -> None:
    console.print(f"[red bold]Error: {error_message}")
    if not sys.platform.startswith(('win', 'cygwin')):
        quit(os.EX_USAGE)  # `os.EX_USAGE` is not compatible with the above platforms in Python 3.10
    else:
        quit()


def main() -> None:
    console = Console()
    console.print("[bold]Welcome to ARP Audio Analyser!")

    working_directory, files_name = get_args()
    if any(map(lambda x: x is None, [working_directory, files_name])):
        exit_with_error("{}\n{}".format(
            "Working directory or files name not specified!",
            "Try -h/--help to know more about Audio Analyser usage"), console)

    try:
        os.makedirs(os.path.join(working_directory, "temp", files_name), exist_ok=True)
    except:
        exit_with_error("Unable to create temporary directory, output path already exists", console)
    
    with console.status("[purple]Reading input files", spinner="dots"):
        audio_src = os.path.join(working_directory, "PreservationAudioFile", f"{files_name}.wav")
        video_src = os.path.join(working_directory, "PreservationAudioVisualFile", f"{files_name}.mov")

        audio_exists = os.path.exists(audio_src)
        video_exists = os.path.exists(video_src)

        match audio_exists, video_exists:
            case True, True:
                console.print("[green]Input files found!")
            case False, True:
                exit_with_error("Audio file not found! :loud_sound:", console)
            case True, False:
                exit_with_error("Video file not found! :vhs:", console)
            case False, False:
                exit_with_error("Input files not found! :t-rex:", console)

    # create irregularity file 1
    with console.status("[purple]Creating irregularity file 1", spinner="dots"):
        irreg1 = sf.create_irreg_file(audio_src, video_src)
        console.log(f"Found {len(irreg1.irregularities)} irregularities from Audio source")
        File(path=f"{working_directory}/temp/{files_name}/AudioAnalyser_IrregularityFileOutput1.json", format=FileType.JSON).write_content(irreg1.to_json())
        console.log("[green]Irregularity file 1 created")

    # create irregularity file 2
    with console.status("[purple]Creating irregularity file 2", spinner="dots"):
        try:
            video_irreg_1 = File(path=f"{working_directory}/temp/{files_name}/VideoAnalyser_IrregularityFileOutput1.json", format=FileType.JSON).get_content()
        except:
            exit_with_error("Video irregularity file 1 not found", console)
        console.log("Video irregularity file 1 found")
        irreg2 = sf.merge_irreg_files(irreg1, IrregularityFile.from_json(video_irreg_1))
        console.log("[green]Irregularity file 2 created")

    with console.status("[cyan]Extracting audio irregularities", spinner="dots"):
        irreg2 = sf.extract_audio_irregularities(audio_src, irreg2, working_directory + "/temp/" + files_name)
        console.log("[green]Audio irregularities extracted")

    # classify audio irregularities
    with console.status("[cyan bold]Classifying audio irregularities", spinner="monkey"):
        irregularities_features = cl.extract_features(irreg2.irregularities)
        console.log("[green]Audio irregularities features extracted")
        classification_results = cl.classify(irregularities_features)
        console.log("[green]Audio irregularities classified")

    with console.status("[purple]Updating irregularity file 2", spinner="dots"):
        for irreg, classification_result in zip(irreg2.irregularities, classification_results):
            if irreg.source == Source.AUDIO:
                irreg.type = classification_result.get_irregularity_type()
                irreg.properties = classification_result if classification_result.get_irregularity_type() is not None else None

    File(path=f"{working_directory}/temp/{files_name}/AudioAnalyser_IrregularityFileOutput2.json", format=FileType.JSON).write_content(irreg2.to_json())

    console.print("[green bold]Success! :tada:")
    quit(os.EX_OK)  # `os.EX_OK` is not compatible with Windows in Python 3.10, it will be in 3.11


if __name__ == "__main__":
    main()
