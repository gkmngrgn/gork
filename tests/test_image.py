import pathlib

from gork.image import GorkImage


def test_image_size():
    image_path = (
        pathlib.Path(__file__).parent / ".." / "examples" / "emoji_watermelon.png"
    )
    image = GorkImage(image_content=image_path.read_bytes())
    assert image.dst_width == 32
    assert image.dst_height == 32


def test_image_resize():
    image_path = pathlib.Path(__file__).parent / ".." / "examples" / "building.png"
    image = GorkImage(image_content=image_path.read_bytes())
    assert image.dst_width == 128
    assert image.dst_height == 96

    image = GorkImage(image_content=image_path.read_bytes(), pixel_size=20)
    assert image.dst_width == 64
    assert image.dst_height == 48
