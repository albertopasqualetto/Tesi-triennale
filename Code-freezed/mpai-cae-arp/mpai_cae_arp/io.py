"""
This module contains functions to print and format text in the console. Consider it as deprecated, use instead rich library.
"""
from enum import Enum

END = '\033[0m'


class Style(Enum):
    """
    Styles for console output
    """
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Color(Enum):
    """
    Colors for console output
    """
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


def prettify(text: str, color: Color = None, styles: list[Style] = None) -> str:
    """
    Formats a string with some styles

    Parameters
    ----------
    text : str
        string to format
    color : Color, optional
        color to use
    styles : list[Style], optional
        styles to use
    
    Returns
    -------
    str
        formatted string
    """

    prepend = ''

    if color:
        prepend += color.value
    if styles:
        for style in styles:
            prepend += style.value

    return prepend + text + END


def pprint(text: str, color: Color = None, styles: list[Style] = None) -> None:
    """
    Formats a string with some styles and prints it

    Parameters
    ----------
    text : str
        string to format
    color : Color, optional
        color to use
    styles : list[Style], optional
        styles to use
    """

    print(prettify(text, color, styles))
