import operator
import sys
import typing
from collections import defaultdict

from gork.palette import SENSITIVITY, get_flat_palette, get_palette

import numpy as np
from PIL import Image


class GorkImage:
    def __init__(self, image_path: str, width: int) -> None:
        self.spectrum: typing.Dict[typing.Tuple[int, ...], str] = {}
        self.palette = get_palette()
        self.image = Image.open(image_path)
        self.src_width, self.src_height = self.image.size
        self.dst_width, self.dst_height = width, int(width / self.image.width * self.image.height)
        self.image = self.image.resize(size=(self.dst_width, self.dst_height), resample=Image.BOX)

    def dists(self, pixel: np.ndarray) -> np.ndarray:
        dists = np.empty(self.palette.shape[0], dtype=np.double)
        for i in range(self.palette.shape[0]):
            r = (self.palette[i][0] + pixel[0]) / 2
            dr = np.power(self.palette[i][0] - pixel[0], 2)
            dg = np.power(self.palette[i][1] - pixel[1], 2)
            db = np.power(self.palette[i][2] - pixel[2], 2)
            dists[i] = np.sqrt(2 * dr + 4 * dg + 3 * db + ((r * (dr - db)) / 256))
        return dists

    def export(self, output: str) -> None:
        palette_img = Image.new("P", (1, 1), 0)
        palette_img.putpalette(get_flat_palette())

        # if self.image.mode not in ["RGB", "L"]:
        #     image = self.image.convert("RGB")

        image_size = (self.dst_width * SENSITIVITY, self.dst_height * SENSITIVITY)
        image = self.image.resize(size=image_size, resample=Image.BICUBIC).quantize(palette=palette_img).convert("RGB")

        out_image = Image.new("RGB", size=(self.dst_width, self.dst_height))
        out_data = np.empty([self.dst_width, self.dst_height, 3])

        for x in range(self.dst_width):
            for y in range(self.dst_height):
                histogram: typing.Dict[int, int] = defaultdict(int)
                for x2 in range(x * SENSITIVITY, (x + 1) * SENSITIVITY):
                    for y2 in range(y * SENSITIVITY, (y + 1) * SENSITIVITY):
                        histogram[image.getpixel((x2, y2))] += 1
                if sys.version_info[0] == 3:
                    color = max(histogram.items(), key=operator.itemgetter(1))[0]
                elif sys.version_info[0] == 2:
                    color = max(histogram.iteritems(), key=operator.itemgetter(1))[0]
                out_data[x, y] = color
                out_image.putpixel((x, y), color)

        out_image = out_image.resize(size=(self.src_width, self.src_height), resample=Image.BOX)
        out_image.save(output)

    def get_pixel_color(self, x: int, y: int) -> str:
        pixel = self.image.getpixel(xy=(x, y))
        if pixel not in self.spectrum:
            dists = self.dists(np.array(pixel))
            self.spectrum[pixel] = str(np.argmin(dists))
        return self.spectrum[pixel]

    def get_spectrum(self) -> typing.Tuple[int, ...]:
        return sorted(set(self.spectrum.values()))
