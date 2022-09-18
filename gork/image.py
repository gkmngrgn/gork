"""GORK image module."""
import collections
import operator
from typing import Dict, List, Tuple

import cv2
import numpy as np
from sklearn.cluster import MiniBatchKMeans

from gork.palette import COLOR_TREE, COLORS, PALETTE
from gork.structs import RGB, Color, ImageType, RGBType


def get_nearest_color(rgb: RGB) -> RGBType:
    """Return nearest color for rgb value."""
    result: int = COLOR_TREE.query(rgb.as_tuple)[1]
    return PALETTE[result]


class GorkImage:  # pylint: disable=too-many-instance-attributes
    """Gork image processor."""

    def __init__(self, image_content: bytes, pixel_size: int) -> None:
        """Initialize a new processor to generate pixelated image."""
        self.__spectrum: Dict[RGBType, int] = collections.defaultdict(int)
        self.__src_image = cv2.imdecode(
            np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR
        )

        # public attributes
        self.src_height, self.src_width, _ = self.__src_image.shape
        self.n_clusters = 256
        self.dst_width = self.src_width // pixel_size
        self.dst_height = int(self.dst_width / self.src_width * self.src_height)
        self.image = self.__create_image()

    def __create_image(self) -> ImageType:
        colorspace = cv2.cvtColor(self.__src_image, cv2.COLOR_BGR2LAB)
        clt = MiniBatchKMeans(n_clusters=self.n_clusters)
        labels = clt.fit_predict(
            colorspace.reshape((self.src_width * self.src_height, 3))
        )
        quantized_colorspace = clt.cluster_centers_.astype(np.uint8)[labels].reshape(
            (self.src_height, self.src_width, 3)
        )
        image = cv2.cvtColor(quantized_colorspace, cv2.COLOR_LAB2BGR)
        image = cv2.resize(
            image,
            (self.dst_width, self.dst_height),
            interpolation=cv2.INTER_LINEAR,
        )

        for color in np.unique(image.reshape(-1, image.shape[2]), axis=0):
            nearest_color = get_nearest_color(RGB(*color))
            image[np.where((image == color).all(axis=2))] = nearest_color
            self.__spectrum[nearest_color] += 1

        # return cv2.resize(
        #     image,
        #     (self.src_width, self.src_height),
        #     interpolation=cv2.INTER_NEAREST,
        # )

        return image

    @property
    def spectrum(self) -> List[Tuple[Color, int]]:
        """Return color list of the pixelated image."""
        spectrum = [
            (COLORS[PALETTE.index(rgb)], count)
            for rgb, count in sorted(
                self.__spectrum.items(), key=operator.itemgetter(1), reverse=True
            )
        ]
        return spectrum

    def get_color(self, pos_x: int, pos_y: int) -> RGBType:
        """Return color of a position on the pixelated image."""
        color = self.image[pos_y, pos_x]
        rgb: RGBType = (color[0], color[1], color[2])
        return rgb

    def export(self, output: str) -> None:
        """Save image output."""
        image = cv2.resize(
            src=self.image,
            dsize=(self.src_width, self.src_height),
            interpolation=cv2.INTER_NEAREST,
        )
        cv2.imwrite(output, image)
