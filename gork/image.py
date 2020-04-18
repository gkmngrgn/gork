import operator
import sys
import typing
from collections import defaultdict

from gork.palette import SENSITIVITY, get_flat_palette, get_palette
from gork.structs import RGB
from PIL import Image


class GorkImage:
    def __init__(self, image_path: str, width: int) -> None:
        self.spectrum: typing.Dict[typing.Tuple[int, ...], RGB] = {}
        self.palette = get_palette()
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
        image = self.image.resize(size=image_size, resample=Image.BOX).quantize(palette=palette).convert("RGB")
        image_output = Image.new("RGB", size=(self.dst_width, self.dst_height))

        for x in range(self.dst_width):
            for y in range(self.dst_height):
                histogram: typing.Dict[int, int] = defaultdict(int)
                for x2 in range(x * SENSITIVITY, (x + 1) * SENSITIVITY):
                    for y2 in range(y * SENSITIVITY, (y + 1) * SENSITIVITY):
                        histogram[image.getpixel((x2, y2))] += 1
                if sys.version_info[0] == 3:
                    pixel = max(histogram.items(), key=operator.itemgetter(1))[0]
                elif sys.version_info[0] == 2:
                    pixel = max(histogram.iteritems(), key=operator.itemgetter(1))[0]

                image_output.putpixel((x, y), pixel)

        return image_output

    def get_color(self, x: int, y: int) -> RGB:
        pixel = self.image.getpixel(xy=(x, y))
        if pixel not in self.spectrum:
            self.spectrum[pixel] = RGB(*pixel)
        return self.spectrum[pixel]

    def get_spectrum(self) -> typing.List[RGB]:
        return sorted(set(self.spectrum.values()))
