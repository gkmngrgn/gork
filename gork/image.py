import collections
import operator
import typing

import cv2
import numpy as np
from gork.palette import SENSITIVITY
from gork.structs import RGB, ImageType, PositionType, RGBType
from gork.utils import get_all_positions, get_color_histogram, get_nearest_color
from tqdm import tqdm


class GorkImage:
    def __init__(self, image_path: str, width: int) -> None:
        self.spectrum: typing.Dict[typing.Tuple[int, ...], RGB] = {}
        self.image = cv2.imread(image_path)
        self.src_height, self.src_width, _ = self.image.shape
        self.dst_height, self.dst_width = int(width / self.src_width * self.src_height), width
        self.image = self.generate_pixelated_image()

    def export(self, output: str) -> None:
        image = cv2.resize(src=self.image, dsize=(self.src_width, self.src_height), interpolation=cv2.INTER_NEAREST)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output, image)

    def generate_pixelated_image(self) -> ImageType:
        source_image = cv2.resize(
            src=self.image,
            dsize=(self.dst_width * SENSITIVITY, self.dst_height * SENSITIVITY),
            interpolation=cv2.INTER_NEAREST,
        )
        pixelated_image = np.empty(shape=[self.dst_height, self.dst_width, 3], dtype=np.uint8)
        palette: typing.Dict[RGBType, typing.List[PositionType]] = collections.defaultdict(list)
        all_positions = get_all_positions(x_start=0, x_end=self.dst_width, y_start=0, y_end=self.dst_height)

        print("\npixelate...")
        for pos_x, pos_y in tqdm(
            all_positions, total=self.dst_width * self.dst_height, ncols=self.dst_width, unit="px"
        ):
            histogram = get_color_histogram(source_image, pos_x, pos_y)
            rgb_value, _ = max(histogram.items(), key=operator.itemgetter(1))
            palette[rgb_value].append((pos_x, pos_y))

        print("\nfind nearest colors...")
        for pixel, positions in tqdm(palette.items(), ncols=self.dst_width):
            nearest_color = get_nearest_color(RGB(*pixel))
            for pos_x, pos_y in positions:
                pixelated_image[pos_y, pos_x] = nearest_color.as_tuple

        pixelated_image = cv2.cvtColor(pixelated_image, cv2.COLOR_BGR2RGB)
        return pixelated_image

    def get_color(self, pos_x: int, pos_y: int) -> RGB:
        pixel = tuple(self.image[pos_y, pos_x])
        if pixel not in self.spectrum:
            self.spectrum[pixel] = RGB(*pixel)
        return self.spectrum[pixel]

    def get_spectrum(self) -> typing.List[RGB]:
        return sorted(set(self.spectrum.values()))
