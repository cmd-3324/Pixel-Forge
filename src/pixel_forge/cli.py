"""Command-line interface for Pixel-Forge (``convertme``)."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.markup import escape

from pixel_forge.formats import OutputFormat

app = typer.Typer(
    name="convertme",
    help="Convert an image to another format.",
    epilog="Exit status: 0 = success, 1 = conversion failed, 2 = bad usage.",
    no_args_is_help=True,
    add_completion=False,
    context_settings={"help_option_names": ["-h", "--help"]},
)

console = Console()
err_console = Console(stderr=True)


def _version_callback(value: bool) -> None:
    if value:
        from importlib.metadata import version  # lazy: only needed here

        typer.echo(f"convertme {version('pixel-forge')}")
        raise typer.Exit()


def _human_size(num: int) -> str:
    size = float(num)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{num} B"  # unreachable; keeps type-checkers happy


@app.command()
def main(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            metavar="SOURCE",
            help="Image file to convert.",
        ),
    ],
    fmt: Annotated[
        OutputFormat,
        typer.Option(
            "--to",
            "-t",
            case_sensitive=False,
            help="Target format.",
        ),
    ],
    dest: Annotated[
        Optional[Path],
        typer.Option(
            "--dest",
            "-d",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Folder to save into (created if missing). [default: current dir]",
            show_default=False,
        ),
    ] = None,
    quality: Annotated[
        Optional[int],
        typer.Option(
            "--quality",
            "-q",
            min=1,
            max=100,
            help="Quality for JPEG/WEBP output (1-100).",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Overwrite the output file if it exists."),
    ] = False,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-V",
            callback=_version_callback,
            is_eager=True,
            help="Show the version and exit.",
        ),
    ] = None,
) -> None:
    """Convert SOURCE to another image format.

    Examples:  convertme photo.png --to webp   |   convertme a.jpg -t png -d ./out
    """
    # Lazy import: Pillow is the slow part, so --help/--version never pay for it.
    from pixel_forge.core import ConversionError, convert

    dest_dir = dest if dest is not None else Path.cwd()

    try:
        with console.status("Converting..."):
            result = convert(source, dest_dir, fmt, quality=quality, force=force)
    except ConversionError as exc:
        err_console.print(f"[red]error:[/red] {escape(str(exc))}")
        raise typer.Exit(1) from exc

    change = ""
    if result.source_size:
        pct = (result.output_size - result.source_size) / result.source_size * 100
        change = f", {pct:+.0f}%"
    console.print(
        f"[green]OK[/green] {escape(result.source.name)} -> "
        f"[bold]{escape(str(result.output))}[/bold] "
        f"[dim]({_human_size(result.source_size)} -> "
        f"{_human_size(result.output_size)}{change})[/dim]"
    )
