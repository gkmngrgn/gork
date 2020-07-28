import pathlib

from gork.image import GorkImage


def test_image_size():
    image_path = pathlib.Path(__file__).parent / ".." / "examples" / "emoji_watermelon.png"
    image = GorkImage(image_content=image_path.read_bytes())
    assert image.width == 32
    assert image.height == 32


def test_image_resize():
    image_path = pathlib.Path(__file__).parent / ".." / "examples" / "building.png"
    image = GorkImage(image_content=image_path.read_bytes())
    assert image.width == 128
    assert image.height == 96

    image = GorkImage(image_content=image_path.read_bytes(), pixel_size=20)
    assert image.width == 64
    assert image.height == 48
