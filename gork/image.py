import typing
from PIL import Image, ImageOps


class GorkImage:
    def __init__(self, image_path: str) -> None:
        self.image = Image.open(image_path)

    def get_size(self) -> typing.Tuple[int, int]:
        return self.image.width, self.image.height

    def resize(self, width: int) -> None:
        height = int(self.image.width * width / self.image.height)
        self.image = ImageOps.fit(self.image, size=(width, height))
