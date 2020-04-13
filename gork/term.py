import io
import typing

from gork.palette import PALETTE
from gork.image import GorkImage

import numpy as np
from PIL import Image

ANSI_ESC = "\x1B["
ANSI_CLR = "38;5;{fg};48;5;{bg}"
ANSI_CHR = "m▀"
ANSI_RES = "\x1b[0m"


class Terminal(object):
    def __init__(self, src: io.BufferedReader) -> None:
        self.src = src
        self.spectrum: typing.Dict[typing.Tuple[int, ...], str] = {}
        self.palette = np.empty((2 ** 8, 3), dtype=np.int64)
        for index, color in enumerate(PALETTE):
            self.palette[index] = color[::-1]
        self.width = 78

    @staticmethod
    def get_ansi_color_code(foreground: str, background: str = "") -> str:
        background = background or foreground
        code_block = [ANSI_ESC, ANSI_CLR.format(fg=foreground, bg=background), ANSI_CHR]
        return "".join(code_block)

    def get_color(self, pixel: np.array) -> str:
        pixel_tuple = tuple(pixel)
        if pixel_tuple not in self.spectrum:
            dists = self.dists(self.palette, pixel)
            self.spectrum[pixel_tuple] = str(np.argmin(dists))
        return self.spectrum[pixel_tuple]

    def dists(self, col_map: np.ndarray, pixel: np.ndarray) -> np.ndarray:
        dists = np.empty(col_map.shape[0], dtype=np.double)
        for i in range(col_map.shape[0]):
            r = (col_map[i][0] + pixel[0]) / 2
            dr = np.power(col_map[i][0] - pixel[0], 2)
            dg = np.power(col_map[i][1] - pixel[1], 2)
            db = np.power(col_map[i][2] - pixel[2], 2)
            dists[i] = np.sqrt(2 * dr + 4 * dg + 3 * db + ((r * (dr - db)) / 256))
        return dists

    def print_image(self) -> None:
        image = GorkImage(image_path=self.src.name)
        image.resize(width=self.width)
        width, height = image.get_size()

        import ipdb; ipdb.set_trace()

        # input_img = image.astype(np.int64)

        print()
        for y in range(height // 2):
            y2 = 2 * y
            for x in range(width):
                top_pxl = input_img[y2, x]
                bot_pxl = input_img[y2 + 1, x]
                top_col = self.get_color(top_pxl)
                bot_col = self.get_color(bot_pxl)
                print(self.get_ansi_color_code(top_col, bot_col), sep="", end=ANSI_RES, flush=True)
            print()

    def print_palette(self) -> None:
        print("\nColors of the image")

        counter = 0
        for color_code in sorted(set(self.spectrum.values())):
            print(self.get_ansi_color_code(color_code), sep="", end=f"{ANSI_RES} ")
            counter += 1

            if counter >= self.width / 2:
                counter = 0
                print("\n")

        print("\n")
