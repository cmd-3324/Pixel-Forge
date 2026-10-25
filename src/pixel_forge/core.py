"""Core image-conversion logic. No CLI or Rich dependencies, so it is reusable."""

from __future__ import annotations

from contextlib import suppress
from pathlib import Path
from typing import Any

from PIL import Image, ImageOps

# Extension -> Pillow format name. Add new formats here.
FORMATS: dict[str, str] = {
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "webp": "WEBP",
    "gif": "GIF",
    "bmp": "BMP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "ico": "ICO",
    "icns": "ICNS",
    "pdf": "PDF",
    "ppm": "PPM",
    "tga": "TGA",
    "jp2": "JPEG2000",
}

NO_ALPHA = {"JPEG", "PDF", "PPM"}  # formats that need a flattened background
ICON = {"ICO", "ICNS"}
EXOTIC_MODES = {"CMYK", "YCbCr", "LAB", "HSV"}
PLAIN_MODES = {"RGB", "L"}


class ConvertError(Exception):
    """Expected, user-facing conversion failure."""


def normalize_format(name: str) -> str:
    """Return the lowercase extension for `name`, or raise ConvertError."""
    key = name.lower().lstrip(".")
    if key not in FORMATS:
        raise ConvertError(f"unsupported format '{name}'")
    return key


def _has_alpha(img: Image.Image) -> bool:
    return img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info


def _prepare(img: Image.Image, kind: str) -> Image.Image:
    """Adapt the image mode to what the target format can store."""
    if img.mode in EXOTIC_MODES and kind != "TIFF":
        img = img.convert("RGB")
    if kind in NO_ALPHA:
        if _has_alpha(img):
            rgba = img.convert("RGBA")
            base = Image.new("RGBA", rgba.size, "white")
            base.alpha_composite(rgba)
            return base.convert("RGB")
        if img.mode not in PLAIN_MODES:
            return img.convert("RGB")
        return img
    if kind in ICON:
        return img.convert("RGBA")
    return img


def convert(
    source: str | Path,
    fmt: str,
    dest: str | Path | None = None,
    **options: Any,
) -> Path:
    """Convert `source` to `fmt` and return the output path.

    `options` are forwarded to Pillow's `Image.save` (e.g. quality=85).
    Raises ConvertError on any expected failure.
    """
    source = Path(source)
    if not source.is_file():
        raise ConvertError(f"{source} is not a file")

    key = normalize_format(fmt)
    kind = FORMATS[key]
    folder = Path(dest) if dest else Path.cwd()
    output = folder / f"{source.stem}.{key}"

    if output.exists():
        if output.samefile(source):
            raise ConvertError(f"{source.name} is already a .{key} file")
        raise ConvertError(f"{output} already exists (not overwriting)")

    try:
        with Image.open(source) as img:
            img.load()  # validate the image before touching the disk
            img = ImageOps.exif_transpose(img)  # fix rotated phone photos
            img = _prepare(img, kind)
            folder.mkdir(parents=True, exist_ok=True)
            img.save(output, format=kind, **options)
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError) as exc:
        with suppress(OSError):
            output.unlink(missing_ok=True)  # never leave a partial file
        raise ConvertError(f"could not convert {source.name}: {exc}") from exc

    return output
