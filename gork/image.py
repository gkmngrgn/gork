import collections
import operator
import typing

import cv2
import numpy as np
from gork.palette import COLORS, PALETTE
from gork.structs import RGB, Color, ImageType, RGBType
from gork.utils import (
    DEFAULT_N_CLUSTERS,
    DEFAULT_PIXEL_SIZE,
    get_nearest_color,
)
from sklearn.cluster import MiniBatchKMeans


class GorkImage:
    def __init__(
        self,
        image_path: str,
        pixel_size: int = DEFAULT_PIXEL_SIZE,
        save_results: bool = True,
        ignore_cache: bool = False,
    ) -> None:
        self.spectrum: typing.Dict[RGBType, int] = collections.defaultdict(int)
        self.pixel_size = pixel_size
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        self.src_height, self.src_width, _ = self.image.shape
        self.dst_width = self.src_width // pixel_size
        self.dst_height = int(self.dst_width / self.src_width * self.src_height)
        self.image = self.generate_pixelated_image()

    def export(self, output: str) -> None:
        image = cv2.resize(
            src=self.image,
            dsize=(self.src_width, self.src_height),
            interpolation=cv2.INTER_NEAREST,
        )
        cv2.imwrite(output, image)

    def generate_pixelated_image(
        self, n_clusters: int = DEFAULT_N_CLUSTERS,
    ) -> ImageType:
        image = self.image
        colorspace = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        clt = MiniBatchKMeans(n_clusters=n_clusters)
        labels = clt.fit_predict(
            colorspace.reshape((self.src_width * self.src_height, 3))
        )
        quantized_colorspace = clt.cluster_centers_.astype(np.uint8)[labels].reshape(
            (self.src_height, self.src_width, 3)
        )
        image = cv2.cvtColor(quantized_colorspace, cv2.COLOR_LAB2BGR)
        image = cv2.resize(
            image, (self.dst_width, self.dst_height), interpolation=cv2.INTER_LINEAR,
        )

        for color in np.unique(image.reshape(-1, image.shape[2]), axis=0):
            nearest_color = get_nearest_color(RGB(*color))
            image[np.where((image == color).all(axis=2))] = nearest_color.as_tuple
            self.spectrum[nearest_color.as_tuple] += 1

        image = cv2.resize(
            image, (self.src_width, self.src_height), interpolation=cv2.INTER_NEAREST
        )

        return image

    def get_color(self, pos_x: int, pos_y: int) -> np.ndarray:
        return self.image[pos_y, pos_x]

    def get_spectrum(self) -> typing.List[typing.Tuple[Color, int]]:
        spectrum = [
            (COLORS[PALETTE.index(rgb)], count)
            for rgb, count in sorted(
                self.spectrum.items(), key=operator.itemgetter(1), reverse=True
            )
        ]
        return spectrum
