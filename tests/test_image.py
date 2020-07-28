import pathlib

from gork.image import GorkImage


def test_image_size():
    image_path = pathlib.Path(__file__).parent / "assets" / "cats.png"
    image = GorkImage(image_content=image_path.read_bytes())
    assert image.width == 50
    assert image.height == 50


def test_image_resize():
    image_path = pathlib.Path(__file__).parent / "assets" / "cats.png"
    image = GorkImage(image_content=image_path.read_bytes(), pixel_size=20)
    image.resize(width=78)
    assert image.width == 78
    assert image.height == 78
