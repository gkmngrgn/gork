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
        image_content: bytes,
        pixel_size: int = DEFAULT_PIXEL_SIZE,
        save_results: bool = True,
        ignore_cache: bool = False,
    ) -> None:
        self.spectrum: typing.Dict[RGBType, int] = collections.defaultdict(int)
        self.pixel_size = pixel_size

        image_content = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(image_content, cv2.IMREAD_COLOR)
        self.__src_height, self.__src_width, _ = image.shape
        self.width = self.__src_width // pixel_size
        self.height = int(self.width / self.__src_width * self.__src_height)
        self.image = self.generate_pixelated_image(image)

    def export(self, output: str) -> None:
        image = cv2.resize(
            src=self.image,
            dsize=(self.__src_width, self.__src_height),
            interpolation=cv2.INTER_NEAREST,
        )
        cv2.imwrite(output, image)

    def generate_pixelated_image(
        self, image: np.ndarray, n_clusters: int = DEFAULT_N_CLUSTERS,
    ) -> ImageType:
        colorspace = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        clt = MiniBatchKMeans(n_clusters=n_clusters)
        labels = clt.fit_predict(
            colorspace.reshape((self.__src_width * self.__src_height, 3))
        )
        quantized_colorspace = clt.cluster_centers_.astype(np.uint8)[labels].reshape(
            (self.__src_height, self.__src_width, 3)
        )
        image = cv2.cvtColor(quantized_colorspace, cv2.COLOR_LAB2BGR)
        image = cv2.resize(
            image, (self.width, self.height), interpolation=cv2.INTER_LINEAR,
        )

        for color in np.unique(image.reshape(-1, image.shape[2]), axis=0):
            nearest_color = get_nearest_color(RGB(*color))
            image[np.where((image == color).all(axis=2))] = nearest_color
            self.spectrum[nearest_color] += 1

        image = cv2.resize(
            image,
            (self.__src_width, self.__src_height),
            interpolation=cv2.INTER_NEAREST,
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
