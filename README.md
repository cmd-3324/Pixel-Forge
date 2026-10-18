# Pixel-Forge

Convert images between formats from the terminal.

```console
$ convertme photo.png --to webp
Saved /home/me/photo.webp
```

## Installation

```console
uv tool install pixel-forge
```

or with pipx:

```console
pipx install pixel-forge
```
## OR

```console
gh repo clone cmd-3324/Pixel-Forge
```
Then:
```console
cd Pixel-Forge
```
Finally:

```console
pipx install . 
```

_or Just Download & click .exe file in releases._


Requires Python 3.10+.

## Usage

```console
convertme SOURCE --to FORMAT [--dest FOLDER]
```

| Option | Description |
|---|---|
| `-t`, `--to FORMAT` | Target format (required). |
| `-d`, `--dest FOLDER` | Folder to save into. Created if missing. Default: current folder. |
| `-h`, `--help` | Show help. |

### Examples

```console
convertme photo.png --to webp
convertme photo.png -t jpg -d ./out
```

### Supported formats

`png`, `jpg`, `jpeg`, `webp`, `gif`, `bmp`, `tiff`, `tif`, `ico`, `icns`, `pdf`, `ppm`, `tga`, `jp2`

## Behavior

- Existing files are never overwritten.
- Formats without transparency (JPEG, PDF, PPM) get a white background where the image is transparent.

## Development

```console
git clone https://github.com/cmd-3324/pixel-forge
cd pixel-forge
uv sync
uv run convertme --help
```

## License

[MIT](LICENSE)
