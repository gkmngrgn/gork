import operator
import sys

from collections import defaultdict

import typing

from gork.palette import PALETTE, SENSITIVITY, SIZE, get_flat_palette

import numpy as np
from PIL import Image, ImageOps


class GorkImage:
    def __init__(self, image_path: str) -> None:
        self.image = Image.open(image_path)
        self.spectrum: typing.Dict[typing.Tuple[int, ...], str] = {}
        self.palette = np.empty((2 ** 8, 3), dtype=np.int64)
        for index, color in enumerate(PALETTE):
            self.palette[index] = color[::-1]

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

        if self.image.mode not in ["RGB", "L"]:
            image = self.image.convert("RGB")
        self.img_size = self.image.size

        image = (
            self.image.resize((SIZE[0] * SENSITIVITY, SIZE[1] * SENSITIVITY), Image.BICUBIC)
            .quantize(palette=palette_img)
            .convert("RGB")
        )

        self.out_image = Image.new("RGB", SIZE)
        self.out_data = np.empty([SIZE[0], SIZE[1], 3])

        for x in range(SIZE[0]):
            for y in range(SIZE[1]):
                histogram: typing.Dict[int, int] = defaultdict(int)
                for x2 in range(x * SENSITIVITY, (x + 1) * SENSITIVITY):
                    for y2 in range(y * SENSITIVITY, (y + 1) * SENSITIVITY):
                        histogram[image.getpixel((x2, y2))] += 1
                if sys.version_info[0] == 3:
                    color = max(histogram.items(), key=operator.itemgetter(1))[0]
                elif sys.version_info[0] == 2:
                    color = max(histogram.iteritems(), key=operator.itemgetter(1))[0]
                self.out_data[x, y] = color
                self.out_image.putpixel((x, y), color)

        # self.out_image = self.out_image.resize(self.img_size)
        self.out_image.save(output)

    def get_pixel_color(self, x: int, y: int) -> str:
        pixel = self.image.getpixel(xy=(x, y))
        if pixel not in self.spectrum:
            dists = self.dists(np.array(pixel))
            self.spectrum[pixel] = str(np.argmin(dists))
        return self.spectrum[pixel]

    def get_size(self) -> typing.Tuple[int, int]:
        return self.image.width, self.image.height

    def get_spectrum(self) -> ...:  # TODO
        return sorted(set(self.spectrum.values()))

    def resize(self, width: int) -> None:
        height = int(self.image.width * width / self.image.height)
        self.image = ImageOps.fit(self.image, size=(width, height))
