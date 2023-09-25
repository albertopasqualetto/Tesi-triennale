"""
Unit tests for the packager module - lib.py.
"""

import pytest
from packager import lib

from pathlib import Path
import os

PathType = str | os.PathLike | Path


def test_make_dir(tmp_path, monkeypatch, capfd):
    working_path = Path(tmp_path)
    test_path = working_path / 'test'
    # Directory does not exist
    out = lib.make_dir(test_path)
    assert out is True, "make_dir does not return True (directory created)" 
    out, err = capfd.readouterr()
    assert 'created' in out, "Directory not created"
    assert test_path.exists(), "Directory not created"

    # Directory already exists
    monkeypatch.setattr('builtins.input', lambda _: "y")    # input "y" to overwrite
    out = lib.make_dir(test_path)
    assert out is True, "make_dir does not return True (directory already exists and want to overwrite)"
    out, err = capfd.readouterr()
    assert 'overwritten' in out, "Directory not overwritten"

    monkeypatch.setattr('builtins.input', lambda _: "n")  # input "n" to overwrite
    out = lib.make_dir(test_path)
    assert out is False, "make_dir does not return False (directory already exists and do NOT want to overwrite)"

    monkeypatch.setattr('builtins.input', lambda _: "not_y_nor_n")  # input unknown to overwrite
    with pytest.raises(SystemExit) as e:
        lib.make_dir(test_path)
    assert e.type == SystemExit, "make_dir does not quit (unknown input to overwrite)"

# Other tests are, in fact, the conformance tests
