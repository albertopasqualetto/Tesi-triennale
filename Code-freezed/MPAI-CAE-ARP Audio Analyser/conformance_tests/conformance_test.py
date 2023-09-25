import pytest
from conftest import files_names, working_path, temp_path, ACCEPTANCE_THRESHOLD, oldify

from pathlib import Path
import json
from jsonschema import validate, ValidationError, SchemaError
import subprocess
import math
import filetype
import tempfile

# JSON schema from MPAI-CAE Technical Specification v2 paragraph 6.4.14.1
if_json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Irregularity File",
    "type": "object",
    "properties": {
        "Offset": {
            "type": "integer"
        },
        "Irregularities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "IrregularityID": {
                        "type": "string",
                        "format": "uuid"
                    },
                    "Source": {
                        "enum": ["a", "v", "b"]
                    },
                    "TimeLabel": {
                        "type": "string",
                        "pattern": "[0-9]{2}:[0-5][0-9]:[0-5][0-9]\\.[0-9]{3}"
                    },
                    "IrregularityType": {
                        "enum": ["sp", "b", "sot", "eot", "da", "di", "m", "s", "wf", "pps", "ssv", "esv", "sb"]
                    },
                    "IrregularityProperties": {
                        "type": "object",
                        "properties": {
                            "ReadingSpeedStandard": {
                                "enum": [0.9375, 1.875, 3.75, 7.5, 15, 30]
                            },
                            "ReadingEqualisationStandard": {
                                "enum": ["IEC", "IEC1", "IEC2"]
                            },
                            "WritingSpeedStandard": {
                                "enum": [0.9375, 1.875, 3.75, 7.5, 15, 30]
                            },
                            "WritingEqualisationStandard": {
                                "enum": ["IEC", "IEC1", "IEC2"]
                            },
                        }
                    },
                    "ImageURI": {
                        "type": "string",
                        "format": "uri"
                    },
                    "AudioFileURI": {
                        "type": "string",
                        "format": "uri"
                    }
                }
            },
            "minItems": 1,
            "uniqueItems": True,
            "required": ["IrregularityID", "Source", "TimeLabel"]
        }
    },
    "required": ["Irregularities"]
}


@pytest.mark.parametrize("files_name", files_names)
def test_irregularity_files_schema(files_name: str):
    """Conformance testing specification point a.

    Test if the irregularity files are syntactically correct and conforming to the JSON schema.
    """
    output_if1_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json"
    output_if2_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json"
    assert output_if1_path.is_file(), "AudioAnalyser_IrregularityFileOutput1.json not found"
    assert output_if2_path.is_file(), "AudioAnalyser_IrregularityFileOutput2.json not found"
    try:
        validate(instance=json.load(output_if1_path.open()), schema=if_json_schema)
    except SchemaError as e:
        pytest.fail(f"AudioAnalyser_IrregularityFileOutput1.json schema is not valid: {e}")
    except ValidationError as e:
        pytest.fail(f"AudioAnalyser_IrregularityFileOutput1.json is not valid: {e}")
    try:    # TODO fails because of video analyser wrong output (":" as ms separator)
        validate(instance=json.load(output_if2_path.open()), schema=if_json_schema)
    except SchemaError as e:
        pytest.fail(f"AudioAnalyser_IrregularityFileOutput2.json schema is not valid: {e}")
    except ValidationError as e:
        pytest.fail(f"AudioAnalyser_IrregularityFileOutput2.json is not valid: {e}")


@pytest.mark.parametrize("files_name", files_names)
def test_irregularities_present(files_name: str):
    """Conformance testing specification point  b.

    Test if all irregularities in DS3 are present in the DS5.
    """
    input_va_if1_path = temp_path / files_name / "VideoAnalyser_IrregularityFileOutput1.json"
    test_aa_if2_path = oldify(temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json")
    assert test_aa_if2_path.is_file(), "AudioAnalyser_IrregularityFileOutput2.json not found"
    with open(input_va_if1_path, "r") as input_if_file:
        input_if_dict = json.load(input_if_file)
    with open(test_aa_if2_path, "r") as output_if_file:
        output_if_dict = json.load(output_if_file)
    output_irr_ids = [irr["IrregularityID"] for irr in output_if_dict["Irregularities"]]
    for irr in input_if_dict["Irregularities"]:
        assert irr['IrregularityID'] in output_irr_ids, f"Irregularity {irr['IrregularityID']} not found in AudioAnalyser_IrregularityFileOutput2.json"


@pytest.mark.parametrize("files_name", files_names)
def test_offset_difference(files_name: str):
    """Conformance testing specification point c.

    Test if the offset difference between Audio Analyser and DS5 real offset is small.
    """
    aa_if1_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json"
    test_if2_path = oldify(temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json")
    assert aa_if1_path.is_file(), "AudioAnalyser_IrregularityFileOutput1.json not found"
    with open(aa_if1_path, "r") as aa_if_file:
        aa_if_dict = json.load(aa_if_file)
    with open(test_if2_path, "r") as test_if_file:
        test_if_dict = json.load(test_if_file)
    aa_offset = int(aa_if_dict["Offset"])
    real_offset = int(test_if_dict["Offset"])

    out = subprocess.run(["ffprobe", "-v", "0", "-of", "csv=p=0", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", str(working_path / "PreservationAudioVisualFile" / (files_name+".mov"))], capture_output=True)
    rate = out.stdout.decode("utf-8").split('/')
    fps = int(rate[0]) / int(rate[1])
    
    assert abs(aa_offset - real_offset) < 3 * math.ceil(1000 / fps), f"Offset difference is too big: {abs(aa_offset - real_offset)}ms"


@pytest.mark.parametrize("files_name", files_names)
def test_rf64(files_name: str):
    """Conformance testing specification point d.

    Test if all output audio files are conforming to RF64 file format = test if .wav files.
    """
    pass
    af_path = temp_path / files_name / "AudioBlocks"
    total_files_n = 0
    wav_conforming_files = 0
    for file in af_path.iterdir():
        total_files_n += 1
        mime = filetype.guess_mime(str(file))
        if mime == "audio/x-wav":
            wav_conforming_files += 1
    assert total_files_n == wav_conforming_files, f"AudioBlocks folder contains {total_files_n-wav_conforming_files} non-wav files out of {total_files_n}"


@pytest.mark.parametrize("files_name", files_names)
def test_audio_extraction(files_name: str):
    """Conformance testing specification point e.

    Test if audio files are extracted from the Preservation Audio File at the time labels indicated in the DS5.
    """
    output_if2_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json"
    test_if2_path = oldify(temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json")
    assert output_if2_path.is_file(), "AudioAnalyser_IrregularityFileOutput2.json not found"
    with open(output_if2_path, "r") as output_if2_file:
        output_if2_dict = json.load(output_if2_file)
    with open(test_if2_path, "r") as test_if2_file:
        test_if2_dict = json.load(test_if2_file)

    _, _, extra_in_out, extra_in_test = check_classification_results(output_if2_dict, test_if2_dict)

    assert not extra_in_out and not extra_in_test, f"Irregularities not at the same timelabels as DS5: there are {extra_in_out} extra irregularities in output file and {extra_in_test} extra irregularities in test file"

    for out_irr in output_if2_dict["Irregularities"]:
        assert Path(out_irr["AudioBlockURI"]).is_file(), f"Audio file of irregularity {out_irr['IrregularityID']} not found"


@pytest.mark.parametrize("files_name", files_names)
def test_audio_classification(files_name: str):
    """Not needed by conformance testing specification.

    Test if `AudioAnalyser_IrregularityFileOutput2.json` classification results are exactly equal to test dataset DS5.
    """
    output_if2_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json"
    test_if2_path = oldify(temp_path / files_name / "AudioAnalyser_IrregularityFileOutput2.json")
    assert output_if2_path.is_file(), "AudioAnalyser_IrregularityFileOutput2.json not found"
    with open(output_if2_path, "r") as output_if2_file:
        output_if2_dict = json.load(output_if2_file)
    with open(test_if2_path, "r") as test_if2_file:
        test_if2_dict = json.load(test_if2_file)

    exact_equality, found_n, extra_in_out, extra_in_test = check_classification_results(output_if2_dict, test_if2_dict, print_differences=True)

    print("Exact equality?", exact_equality)
    print("N of elements in common:", found_n)
    print("N of extra elements in output file:", extra_in_out)
    print("N of extra elements in test file:", extra_in_test)

    assert exact_equality, "Classification results are not exactly equal to DS5"


@pytest.mark.parametrize("files_name", files_names)
def test_if1(files_name):
    """Conformance testing specification point 2.

    Test `AudioAnalyser_IrregularityFileOutput1.json` Precision and Recall with respect to the provided ground truth (DS4).

    Recall = The ratio between the number of True Positives and the total number of True Positives plus False Negatives.
    Precision = The ratio between the number of True Positives and the total number of True Positives plus False Positives.
    positive -> there is an irregularity.
    """
    output_if1_path = temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json"
    test_if1_path = oldify(temp_path / files_name / "AudioAnalyser_IrregularityFileOutput1.json")
    try:
        with open(output_if1_path, "r") as output_if1_file:
            output_if1_dict = json.load(output_if1_file)
    except FileNotFoundError:
        output_if1_dict = {"Irregularities": []}
    with open(test_if1_path, "r") as test_if1_file:
        test_if1_dict = json.load(test_if1_file)

    _, true_positives, false_positives, false_negatives = check_classification_results(output_if1_dict, test_if1_dict)

    recall = true_positives / (true_positives + false_negatives)
    precision = true_positives / (true_positives + false_positives)

    # save to file
    root_tmp_dir = Path(tempfile.gettempdir()) / "mpai" / "aa_conformance_test"
    json_file_path = root_tmp_dir / (files_name+"_measures.json")
    json_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_file_path, "w") as measures_file:
        measures_dict = {"recall": recall, "precision": precision}
        json.dump(measures_dict, measures_file)

    assert recall > ACCEPTANCE_THRESHOLD, f"Recall is too low: {recall}"    # not necessary
    assert precision > ACCEPTANCE_THRESHOLD, f"Precision is too low: {precision}"   # not necessary


def check_classification_results(if_dict_1: dict, if_dict_2: dict, print_differences: bool = False) -> (bool, int, int, int):
    """
    Check if the irregularity files' classification results in `if_dict_1` are exactly equal to `if_dict_2`.

    Parameters
    ----------
    if_dict_1 : dict
        First irregularity file dictionary (first file to compare).
    if_dict_2 : dict
        Second irregularity file dictionary (second file to compare).
    print_differences : bool, optional
        If True, print the differences between the two files, by default False.

    Returns
    -------
    tuple[bool, int, int, int]
        Tuple of:
            1) if the two files are exactly equal;
            2) number of elements in common;
            3) number of extra elements in the first file;
            4) number of extra elements in the second file.
    """
    def check_all_combinations(list1: list[dict], idxs1: list[int], list2: list[dict], idxs2: list[int]) -> (int | None, int | None):
        """
        Check if any combination of 2 elements with specified indexes in two different lists is equal and return the indexes of the first equal elements found.

        Parameters
        ----------
        list1 : list[dict]
            First list of dictionaries to compare.
        idxs1 : list[int]
            Indexes of the first list to compare.
        list2 : list[dict]
            Second list of dictionaries to compare.
        idxs2 : list[int]
            Indexes of the second list to compare.

        Returns
        -------
        tuple[int | None, int | None]
            If a couple is found, return the indexes of the first equal elements found, otherwise return None, None.
        """
        def filtered_dict(dict_obj: dict, filter: list) -> dict:
            """
            Remove specified keys from a dictionary.

            Parameters
            ----------
            dict_obj : dict
                Dictionary to filter.
            filter : list
                List of keys to remove.

            Returns
            -------
            dict
                Filtered dictionary.
            """
            return {key: value for key, value in dict_obj.items() if key not in filter}

        keys_to_remove = ["IrregularityID", "AudioBlockURI"]
        for idx1 in idxs1:
            for idx2 in idxs2:
                filtered_list1 = list(map(lambda x: filtered_dict(x, keys_to_remove), list1))
                filtered_list2 = list(map(lambda x: filtered_dict(x, keys_to_remove), list2))
                if filtered_list1[idx1] == filtered_list2[idx2]:
                    return idx1, idx2
        return None, None

    exact_equality = True
    found_n = 0
    extra_in_1 = 0
    extra_in_2 = 0
    irrs_1 = if_dict_1["Irregularities"]
    irrs_1.sort(key=lambda irr: int(irr["TimeLabel"].replace(":", "").replace(".", "")))  # FIXME workaround for ":" timelabel problem from video analyser
    irrs_2 = if_dict_2["Irregularities"]
    irrs_2.sort(key=lambda irr: int(irr["TimeLabel"].replace(":", "").replace(".", "")))

    timelabels_1 = [irr["TimeLabel"] for irr in irrs_2]
    for timelabel in list(dict.fromkeys(timelabels_1)):     # remove duplicates
        irrs_1_idxs = get_irr_idxs_by_timelabel(irrs_1, timelabel)
        irrs_2_idxs = get_irr_idxs_by_timelabel(irrs_2, timelabel)

        while True:
            irr_1_idx, irr_2_idx = check_all_combinations(irrs_1, irrs_1_idxs, irrs_2, irrs_2_idxs)
            if irr_1_idx or irr_2_idx:  # first check exact equality
                pass
            else:  # then the others remained as couples (equal length already checked)
                if not len(irrs_1_idxs) or not len(irrs_2_idxs):
                    break
                exact_equality = False
                irr_1_idx = irrs_1_idxs[0]
                irr_2_idx = irrs_2_idxs[0]
                if print_differences:
                    print("Irregularity", irrs_1[irr_1_idx], "\n\tnot exactly equal to\n\t", irrs_2[irr_2_idx])
            found_n += 1
            del irrs_1[irr_1_idx]
            del irrs_2[irr_2_idx]
            irrs_1_idxs.remove(irr_1_idx)
            irrs_2_idxs.remove(irr_2_idx)
            irrs_1_idxs = [idx - 1 if idx > irr_1_idx else idx for idx in irrs_1_idxs]
            irrs_2_idxs = [idx - 1 if idx > irr_2_idx else idx for idx in irrs_2_idxs]
        if len(irrs_2_idxs):
            extra_in_2 += len(irrs_2_idxs)

    extra_in_1 += len(irrs_1)

    return exact_equality, found_n, extra_in_1, extra_in_2


def get_irr_idxs_by_timelabel(irr_list: list, timelabel: str) -> list[int]:
    """
    Return the indexes of the irregularities in the list with the specified timelabel.

    Parameters
    ----------
    irr_list : list
        List of irregularities.
    timelabel : str
        Timelabel to search.

    Returns
    -------
    list[int]
        List of indexes of the irregularities with the specified timelabel (eventually empty).
    """
    found = []
    for idx, irr in enumerate(irr_list):
        if irr["TimeLabel"] == timelabel:
            found.append(idx)
    return found
