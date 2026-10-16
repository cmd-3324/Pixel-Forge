from pathlib import Path

import pytest
from PIL import Image
from typer.testing import CliRunner

from pixel_forge.cli import app

runner = CliRunner()


@pytest.fixture
def png(tmp_path: Path) -> Path:
    path = tmp_path / "pic.png"
    Image.new("RGBA", (32, 32), (255, 0, 0, 128)).save(path)
    return path


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert result.output.startswith("convertme ")


def test_png_with_alpha_to_jpg(png: Path, tmp_path: Path) -> None:
    out = tmp_path / "out"
    result = runner.invoke(app, [str(png), "--to", "jpg", "-d", str(out)])
    assert result.exit_code == 0, result.output
    with Image.open(out / "pic.jpg") as img:
        assert img.format == "JPEG"


def test_refuses_overwrite_without_force(png: Path, tmp_path: Path) -> None:
    args = [str(png), "--to", "webp", "-d", str(tmp_path)]
    assert runner.invoke(app, args).exit_code == 0
    assert runner.invoke(app, args).exit_code == 1
    assert runner.invoke(app, [*args, "--force"]).exit_code == 0


def test_same_file_is_rejected(png: Path) -> None:
    assert runner.invoke(app, [str(png), "--to", "png"]).exit_code == 1


def test_not_an_image(tmp_path: Path) -> None:
    bad = tmp_path / "x.txt"
    bad.write_text("hello")
    assert runner.invoke(app, [str(bad), "--to", "png"]).exit_code == 1


def test_unknown_format(png: Path) -> None:
    assert runner.invoke(app, [str(png), "--to", "xyz"]).exit_code == 2
