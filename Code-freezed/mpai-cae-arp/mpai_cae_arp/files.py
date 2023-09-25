from io import TextIOWrapper
from enum import Enum
import json
import yaml
import codecs
from pydantic import BaseModel, field_validator


class FileAction(str, Enum):
    READ = "r"
    WRITE = "w"
    APPEND = "a"


class FileType(str, Enum):
    YAML = "yaml"
    JSON = "json"


class File(BaseModel):
    encoding: str = "utf-8"
    format: FileType
    path: str

    @field_validator('encoding')
    def encoding_validator(cls, v: str):
        try:
            codecs.lookup(v)
        except LookupError:
            raise ValueError(f"Encoding {v} not supported")
        return v

    def open(self, action: FileAction) -> TextIOWrapper:
        """
        Open the file with the given action        

        Parameters
        ----------
        action : FileAction
            the action to perform on the file at opening

        Returns
        -------
        TextIOWrapper
            the file descriptor
        """
        return open(self.path, action.value, encoding=self.encoding)

    def get_content(self) -> dict:
        """
        Return the file content

        Raises
        ------
        ValueError
            if the format is not supported
        
        Returns
        -------
        dict
            the parsed content of the file
        """
        with self.open(FileAction.READ) as fd:
            if self.format == FileType.YAML:
                content = yaml.safe_load(fd)
                return content
            if self.format == FileType.JSON:
                content = json.load(fd)
            else:
                raise ValueError("Format not supported")

        return content

    def write_content(self, content: dict | str) -> None:
        """
        Write the given content in the file

        Parameters
        ----------
        content : dict | str
            the content to write in the file
            if content is a string, it will be parsed as a JSON string
        """

        if isinstance(content, str):
            try:
                content = json.loads(json.loads(content))
            except json.decoder.JSONDecodeError:
                raise ValueError("Content str is not a valid JSON string")

        with self.open(FileAction.WRITE) as fd:
            if self.format == FileType.YAML:
                yaml.safe_dump(content, fd)
            elif self.format == FileType.JSON:
                json.dump(content, fd, indent=4)
            else:
                raise ValueError("Format not supported")
