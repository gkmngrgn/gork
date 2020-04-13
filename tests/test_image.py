import pathlib
from gork.image import GorkImage


def test_image_size():
    image_path = pathlib.Path(__file__).parent / "assets" / "cats.png"
    image = GorkImage(image_path=image_path)
    assert image.get_size() == (500, 500)


def test_image_resize():
    image_path = pathlib.Path(__file__).parent / "assets" / "cats.png"
    image = GorkImage(image_path=image_path)
    image.resize(width=78)
    assert image.get_size() == (78, 78)
