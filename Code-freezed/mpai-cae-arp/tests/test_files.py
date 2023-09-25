import tempfile
import pytest
from mpai_cae_arp import files


def test_open_file():
    with tempfile.NamedTemporaryFile() as tmp_file:

        tmp_file.write(b'{"test": "test"}')
        tmp_file.seek(0)

        my_file = files.File(path=tmp_file.name,
                             format=files.FileType.JSON).open(files.FileAction.READ)

        assert my_file.read() == '{"test": "test"}'


def test_failing_read():
    with pytest.raises(FileNotFoundError):
        files.File(path="test", format=files.FileType.JSON).open(files.FileAction.READ)


def test_get_content():
    with tempfile.NamedTemporaryFile() as tmp_file:

        tmp_file.write(b'{"test": "test"}')
        tmp_file.seek(0)

        my_file_content = files.File(path=tmp_file.name,
                                     format=files.FileType.JSON).get_content()

        assert my_file_content == {"test": "test"}
