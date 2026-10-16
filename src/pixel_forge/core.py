"""Image conversion logic. No CLI / rich imports, so it is easy to test."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

from pixel_forge.formats import PILLOW_NAME, OutputFormat

_NO_ALPHA = {"JPEG"}  # formats that cannot store transparency
_ANIMATED = {"GIF", "WEBP"}  # formats where we keep every frame
_HAS_QUALITY = {"JPEG", "WEBP"}


class ConversionError(Exception):
    """A user-facing conversion failure."""


@dataclass(frozen=True, slots=True)
class Result:
    source: Path
    output: Path
    source_size: int
    output_size: int


def output_path(source: Path, dest_dir: Path, fmt: OutputFormat) -> Path:
    return dest_dir / f"{source.stem}.{fmt.value}"


def _flatten_alpha(img: Image.Image) -> Image.Image:
    """Return an RGB image, compositing any transparency onto white."""
    has_alpha = img.mode in ("RGBA", "LA", "PA") or (
        img.mode == "P" and "transparency" in img.info
    )
    if not has_alpha:
        return img if img.mode in ("RGB", "L", "CMYK") else img.convert("RGB")
    rgba = img.convert("RGBA")
    background = Image.new("RGB", rgba.size, (255, 255, 255))
    background.paste(rgba, mask=rgba.getchannel("A"))
    return background


def _explain(exc: Exception) -> str:
    if isinstance(exc, UnidentifiedImageError):
        return "Not a recognised image file."
    if isinstance(exc, Image.DecompressionBombError):
        return "Image is extremely large (possible decompression bomb); refusing."
    return str(exc)


def convert(
    source: Path,
    dest_dir: Path,
    fmt: OutputFormat,
    *,
    quality: int | None = None,
    force: bool = False,
) -> Result:
    """Convert *source* to *fmt* inside *dest_dir*."""
    pil_format = PILLOW_NAME[fmt]
    dest = output_path(source, dest_dir, fmt)

    if dest.resolve() == source.resolve():
        raise ConversionError(
            "Output would overwrite the source file; choose another --dest."
        )
    if dest.exists() and not force:
        raise ConversionError(f"{dest} already exists (use --force to overwrite).")

    # Write to a temp file first so a failure never leaves a half-written output
    # (or destroys an existing file when --force is used).
    tmp = dest.with_name(dest.name + ".tmp")
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        options: dict[str, int] = {}
        if quality is not None and pil_format in _HAS_QUALITY:
            options["quality"] = quality

        with Image.open(source) as img:
            if getattr(img, "is_animated", False) and pil_format in _ANIMATED:
                img.save(tmp, format=pil_format, save_all=True, **options)
            else:
                out = ImageOps.exif_transpose(img)  # honour camera rotation
                if pil_format in _NO_ALPHA:
                    out = _flatten_alpha(out)
                elif pil_format == "ICO":
                    out = out.convert("RGBA")
                out.save(tmp, format=pil_format, **options)
        tmp.replace(dest)
    except (OSError, ValueError, Image.DecompressionBombError) as exc:
        tmp.unlink(missing_ok=True)
        raise ConversionError(_explain(exc)) from exc

    return Result(
        source=source,
        output=dest,
        source_size=source.stat().st_size,
        output_size=dest.stat().st_size,
    )
