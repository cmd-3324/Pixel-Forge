# Pixel-Forge

[![PyPI](https://img.shields.io/pypi/v/pixel-forge)](https://pypi.org/project/pixel-forge/)
[![Python](https://img.shields.io/pypi/pyversions/pixel-forge)](https://pypi.org/project/pixel-forge/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Convert images between formats from the command line. Fast, cross-platform, and safe by default.

```console
$ convertme photo.png --to webp
OK photo.png -> /home/me/photo.webp (1.2 MB -> 340.5 KB, -72%)
```

## Installation

```console
uv tool install pixel-forge
```

or with pip / pipx:

```console
pipx install pixel-forge
```

Requires Python 3.10+.

## Usage

```console
convertme SOURCE --to FORMAT [OPTIONS]
```

| Option | Description |
|---|---|
| `-t`, `--to FORMAT` | Target format (required). |
| `-d`, `--dest DIR` | Folder to save into. Created if missing. Default: current directory. |
| `-q`, `--quality 1-100` | Quality for JPEG and WebP output. |
| `-f`, `--force` | Overwrite the output file if it exists. |
| `-V`, `--version` | Show the version and exit. |
| `-h`, `--help` | Show help and exit. |

### Examples

```console
convertme photo.png --to webp
convertme photo.png -t jpg -d ./out
convertme photo.png -t webp -q 80
convertme logo.png -t ico
```

### Supported formats

`png`, `jpg`, `jpeg`, `webp`, `gif`, `bmp`, `tiff`, `ico`

## Behavior

- **Transparency:** converting to JPEG flattens transparent areas onto a white background.
- **Orientation:** camera (EXIF) rotation is applied, so photos don't end up sideways.
- **Animation:** animated GIF and WebP files keep all their frames when converted between those two formats.
- **Safe writes:** existing files are never overwritten without `--force`, and a failed conversion never leaves a half-written file.

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Conversion failed |
| 2 | Invalid usage |

## Development

```console
git clone https://github.com/YOUR-USERNAME/pixel-forge
cd pixel-forge
uv sync
uv run pytest
uv run ruff check .
```

Run the tool from source:

```console
uv run convertme --help
```

## Contributing

Issues and pull requests are welcome. Please run the tests and linter before submitting.

## License

[MIT](LICENSE)
