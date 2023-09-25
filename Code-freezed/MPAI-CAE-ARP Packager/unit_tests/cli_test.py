"""
Unit tests for the packager module - cli.py.
"""

import pytest
from packager import (lib, cli)

import sys
from pathlib import Path
import os

PathType = str | os.PathLike | Path


def test_get_arguments(monkeypatch):
    cli_path = Path(__file__).parent.parent.joinpath("src", "packager", "cli.py")
    # Normal cli behaviour
    monkeypatch.setattr(sys, 'argv', [str(cli_path), '-w', '../data', '-f', 'BERIO100'])
    working_path, files_name = cli.get_arguments()
    assert isinstance(working_path, PathType), "Normal cli behaviour - working path is not a path"
    assert isinstance(files_name, str), "Normal cli behaviour - files name is not a str"

    # Only one argument cli
    monkeypatch.setattr(sys, 'argv', [str(cli_path), '-w', '../data'])  # missing files name
    with pytest.raises(SystemExit) as e:
        cli.get_arguments()
    assert e.type == SystemExit, "Only one argument cli - missing files name not reported"
    monkeypatch.setattr(sys, 'argv', [str(cli_path), '-f', 'BERIO100'])     # missing working path
    with pytest.raises(SystemExit) as e:
        cli.get_arguments()
    assert e.type == SystemExit, "Only one argument cli - missing working path not reported"

    # No arguments cli
    monkeypatch.setattr(sys, 'argv', [str(cli_path)])
    monkeypatch.delenv('WORKING_PATH', raising=False)
    monkeypatch.delenv('FILES_NAME', raising=False)
    with pytest.raises(ValueError) as e:    # missing both arguments in env
        cli.get_arguments()
    assert e.type == ValueError, "No arguments cli - missing both arguments in env not reported"

    monkeypatch.setenv('WORKING_PATH', '../data')   # missing files name in env
    with pytest.raises(ValueError) as e:
        cli.get_arguments()
    assert e.type == ValueError, "No arguments cli - missing files name in env not reported"

    monkeypatch.delenv('WORKING_PATH', raising=False)   # missing working path in env
    monkeypatch.setenv('FILES_NAME', 'BERIO100')
    with pytest.raises(ValueError) as e:
        cli.get_arguments()
    assert e.type == ValueError, "No arguments cli - missing working path in env not reported"

    monkeypatch.setenv('WORKING_PATH', '../data')   # both arguments in env
    monkeypatch.setenv('FILES_NAME', 'BERIO100')
    working_path, files_name = cli.get_arguments()
    assert isinstance(working_path, PathType), "No arguments cli - working path is not a path (from env)"
    assert isinstance(files_name, str), "No arguments cli - files name is not a str (from env)"


def test_check_input(tmp_path):
    working_path = Path(tmp_path)
    files_name = 'BERIO100'
    temp_path = working_path / 'temp'
    files_path = temp_path / files_name

    # No working path
    with pytest.raises(SystemExit) as e:
        cli.check_input(files_path, files_name)
    assert e.type == SystemExit, "No working path not reported"
    
    # No temp_path in working path
    with pytest.raises(SystemExit) as e:
        cli.check_input(working_path, files_name)
    assert e.type == SystemExit, "No temp_path not reported"

    # No files path in working path
    temp_path.mkdir()
    with pytest.raises(SystemExit) as e:
        cli.check_input(working_path, files_name)
    assert e.type == SystemExit, "No files_name not reported"

    # All ok
    files_path.mkdir()
    try:
        out_path = cli.check_input(working_path, files_name)
    except SystemExit:
        pytest.fail("Exception when everything ok")
    assert out_path == files_path, "Wrong output path"


def test_check_return_code(capfd):
    message = "test message"
    with pytest.raises(SystemExit) as e:
        cli.check_return_code(lib.ReturnCode.ERROR, message)
        out, err = capfd.readouterr()
        assert message in out, "Wrong message on error"
    assert e.type == SystemExit, "Not exiting on error"
    
    try:
        cli.check_return_code(lib.ReturnCode.WARNING, message)
        out, err = capfd.readouterr()
        assert message in out, "Wrong message on warning"
    except SystemExit:
        pytest.fail("Exception on warning")

    try:
        cli.check_return_code(lib.ReturnCode.SUCCESS, message)
    except SystemExit:
        pytest.fail("Exception when everything ok")
