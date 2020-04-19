import operator
import typing
from collections import defaultdict

from gork.palette import SENSITIVITY, get_flat_palette
from gork.structs import RGB
from gork.utils import get_all_positions, get_nearest_color

from PIL import Image


class GorkImage:
    def __init__(self, image_path: str, width: int) -> None:
        self.spectrum: typing.Dict[typing.Tuple[int, ...], RGB] = {}
        self.image = Image.open(image_path)
        self.src_width, self.src_height = self.image.size
        self.dst_width, self.dst_height = width, int(width / self.image.width * self.image.height)
        self.image = self.generate_pixelated_image()

    def export(self, output: str) -> None:
        image = self.image.resize(size=(self.src_width, self.src_height), resample=Image.BOX)
        image.save(output)

    def generate_pixelated_image(self) -> Image:
        palette = Image.new("P", (1, 1), 0)
        palette.putpalette(get_flat_palette())

        # if self.image.mode not in ["RGB", "L"]:
        #     image = self.image.convert("RGB")

        image_size = (self.dst_width * SENSITIVITY, self.dst_height * SENSITIVITY)
        image = self.image.resize(size=image_size).quantize(palette=palette).convert("RGB")
        image_output = Image.new("RGB", size=(self.dst_width, self.dst_height))

        for pos_x, pos_y in get_all_positions(x_start=0, x_end=self.dst_width, y_start=0, y_end=self.dst_height):
            histogram: typing.Dict[int, int] = defaultdict(int)

            for pos_x2, pos_y2 in get_all_positions(
                x_start=pos_x * SENSITIVITY,
                x_end=(pos_x + 1) * SENSITIVITY,
                y_start=pos_y * SENSITIVITY,
                y_end=(pos_y + 1) * SENSITIVITY,
            ):
                rgb = RGB(*image.getpixel((pos_x2, pos_y2)))
                histogram[rgb] += 1

            rgb = max(histogram.items(), key=operator.itemgetter(1))[0]
            color = get_nearest_color(rgb)
            image_output.putpixel((pos_x, pos_y), color.as_tuple)

        return image_output

    def get_color(self, x: int, y: int) -> RGB:
        pixel = self.image.getpixel(xy=(x, y))
        if pixel not in self.spectrum:
            self.spectrum[pixel] = RGB(*pixel)
        return self.spectrum[pixel]

    def get_spectrum(self) -> typing.List[RGB]:
        return sorted(set(self.spectrum.values()))
