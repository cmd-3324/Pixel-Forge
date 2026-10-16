"""Supported output formats.

Deliberately free of Pillow imports so ``--help`` and ``--version`` stay fast.
"""

from enum import Enum


class OutputFormat(str, Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    webp = "webp"
    gif = "gif"
    bmp = "bmp"
    tiff = "tiff"
    ico = "ico"


# Maps the user-facing name to Pillow's format identifier.
PILLOW_NAME: dict[OutputFormat, str] = {
    OutputFormat.png: "PNG",
    OutputFormat.jpg: "JPEG",
    OutputFormat.jpeg: "JPEG",
    OutputFormat.webp: "WEBP",
    OutputFormat.gif: "GIF",
    OutputFormat.bmp: "BMP",
    OutputFormat.tiff: "TIFF",
    OutputFormat.ico: "ICO",
}
