from gork.palette import PALETTE

import cv2
import numpy as np


class Terminal(object):
    def __init__(self, src):
        self.src = src
        self.spectrum = {}
        self.palette = np.empty((2 ** 8, 3), dtype=np.int64)
        for index, color in enumerate(PALETTE):
            self.palette[index] = color[::-1]
        self.width = 78

    def get_size(self, width, image):
        r = width / float(image.shape[1])
        return width, int(image.shape[0] * r)

    def get_color(self, pixel):
        pixel_tuple = tuple(pixel)  # why?
        if pixel_tuple not in self.spectrum:
            dists = self.dists(self.palette, pixel)
            self.spectrum[pixel_tuple] = str(np.argmin(dists))
        return self.spectrum[pixel_tuple]

    def dists(self, col_map, pixel):
        dists = np.empty(col_map.shape[0], dtype=np.double)
        for i in range(col_map.shape[0]):
            r = (col_map[i][0] + pixel[0]) / 2
            dr = np.power(col_map[i][0] - pixel[0], 2)
            dg = np.power(col_map[i][1] - pixel[1], 2)
            db = np.power(col_map[i][2] - pixel[2], 2)
            dists[i] = np.sqrt(2 * dr + 4 * dg + 3 * db + ((r * (dr - db)) / 256))
        return dists

    def print_image(self):
        image = cv2.imread(self.src.name)
        width, height = self.get_size(self.width, image)
        image = cv2.resize(src=image, dsize=(width, height))

        out = []
        input_img = image.astype(np.int64)
        for y in range(height // 2):
            y2 = 2 * y
            for x in range(width):
                top_pxl = input_img[y2, x]
                bot_pxl = input_img[y2 + 1, x]
                top_col = self.get_color(top_pxl)
                bot_col = self.get_color(bot_pxl)
                out.append("".join(("\x1B[38;5;", top_col, ";48;5;", bot_col, "m▀")))
            out.append("\n")

        print("".join(out), "\x1b[0m", sep="")

    def print_palette(self):
        print()
        print("Colors of the image")

        counter = 0
        for color_code in sorted(set(self.spectrum.values())):
            print("".join(("\x1B[38;5;", color_code, ";48;5;", "m█")), end=" ")
            counter += 1

            if counter >= self.width / 2:
                counter = 0
                print("\n")
