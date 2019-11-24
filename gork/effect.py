import operator
import sys
from collections import defaultdict

from palette import SENSITIVITY, SIZE, get_flat_palette

import numpy as np
from PIL import Image


class ImageEffect(object):
    def __init__(self, src):
        palette_img = Image.new("P", (1, 1), 0)
        palette_img.putpalette(get_flat_palette())

        input = Image.open(src)
        self.img_size = input.size

        input = (
            input.resize((SIZE[0] * SENSITIVITY, SIZE[1] * SENSITIVITY), Image.BICUBIC)
            .quantize(palette=palette_img)
            .convert("RGB")
        )

        self.out_image = Image.new("RGB", SIZE)
        self.out_data = np.empty([SIZE[0], SIZE[1], 3])

        for x in range(SIZE[0]):
            for y in range(SIZE[1]):
                histogram = defaultdict(int)
                for x2 in range(x * SENSITIVITY, (x + 1) * SENSITIVITY):
                    for y2 in range(y * SENSITIVITY, (y + 1) * SENSITIVITY):
                        histogram[input.getpixel((x2, y2))] += 1
                if sys.version_info[0] == 3:
                    color = max(histogram.items(), key=operator.itemgetter(1))[0]
                elif sys.version_info[0] == 2:
                    color = max(histogram.iteritems(), key=operator.itemgetter(1))[0]
                self.out_data[x, y] = color
                self.out_image.putpixel((x, y), color)

        self.out_image = self.out_image.resize(self.img_size)
