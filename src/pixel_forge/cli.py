# """convertme: convert an image to another format."""

# from pathlib import Path
# from typing import Annotated, Optional

# import typer
# from rich.console import Console



# app = typer.Typer(
#     add_completion=False,
#     no_args_is_help=True,
#     help="Convert an image to another format.",
#     context_settings={"help_option_names": ["-h", "--help"]},
# )
# console = Console()
# err = Console(stderr=True)

# FORMATS = {
#     "png": "PNG",
#     "jpg": "JPEG",
#     "jpeg": "JPEG",
#     "webp": "WEBP",
#     "gif": "GIF",
#     "bmp": "BMP",
#     "tiff": "TIFF",
#     "tif": "TIFF",
#     "ico": "ICO",
#     "icns": "ICNS",
#     "pdf": "PDF",
#     "ppm": "PPM",
#     "tga": "TGA",
#     "jp2": "JPEG2000",
# }
# NO_ALPHA = {"JPEG", "PDF", "PPM"}

# @app.command()
# def main(
#     source: Annotated[
#         Path,
#         typer.Argument(
#             exists=True, dir_okay=False, readable=True, help="Image to convert."
#         ),
#     ],
#     to: Annotated[
#         str,
#         typer.Option("--to", "-t", help="Target format: " + ", ".join(FORMATS) + "."),
#     ],
#     dest: Annotated[
#         Optional[Path],
#         typer.Option(
#             "--dest",
#             "-d",
#             file_okay=False,
#             help="Folder to save into (default: current folder).",
#         ),
#     ] = None,
# ) -> None:
#     """Convert SOURCE to another format.

#     Example: convertme photo.png --to webp
#     """
#     from PIL import Image  # imported here so --help stays instant

#     fmt = to.lower().lstrip(".")
#     if fmt not in FORMATS:
#         err.print(f"[red]error:[/red] unsupported format '{to}'.")
#         raise typer.Exit(2)

#     folder = dest or Path.cwd()
#     folder.mkdir(parents=True, exist_ok=True)
#     output = folder / f"{source.stem}.{fmt}"
#     if output.exists():
#         err.print(f"[red]error:[/red] {output} already exists.")
#         raise typer.Exit(1)

#     try:


#         with Image.open(source) as img:
#             kind = FORMATS[fmt]
#             if kind in NO_ALPHA and img.mode != "RGB":
#                 rgba = img.convert("RGBA")
#                 img = Image.new("RGB", rgba.size, "white")
#                 img.paste(rgba, mask=rgba.getchannel("A"))
#             elif kind in ("ICO", "ICNS"):
#                 img = img.convert("RGBA")
#             img.save(output, format=kind)
#     except OSError as exc:
#         output.unlink(missing_ok=True)
#         err.print(f"[red]error:[/red] could not convert {source.name}: {exc}")
#         raise typer.Exit(1) from exc

#     console.print(f"[green]Saved[/green] {output}")



# if __name__ == "__main__":
#     app()



"""convertme: convert an image to another format."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.markup import escape

from .core import FORMATS, ConvertError, convert

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Convert an image to another format.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()
err = Console(stderr=True)


@app.command()
def main(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True, dir_okay=False, readable=True, help="Image to convert."
        ),
    ],
    to: Annotated[
        str,
        typer.Option("--to", "-t", help="Target format: " + ", ".join(FORMATS) + "."),
    ],
    dest: Annotated[
        Optional[Path],
        typer.Option(
            "--dest",
            "-d",
            file_okay=False,
            help="Folder to save into (default: current folder).",
        ),
    ] = None,
) -> None:
    """Convert SOURCE to another format.

    Example: convertme photo.png --to webp
    """
    try:
        output = convert(source, to, dest)
    except ConvertError as exc:
        err.print(f"[red]error:[/red] {escape(str(exc))}")
        raise typer.Exit(1) from exc

    console.print(f"[green]Saved[/green] {escape(str(output))}")


if __name__ == "__main__":
    app()
