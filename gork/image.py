import collections
import operator
import typing

import cv2
import numpy as np
from gork.palette import COLORS, PALETTE, SENSITIVITY
from gork.structs import RGB, Color, ImageType, PositionType, RGBType
from gork.utils import (
    DEFAULT_N_CLUSTERS,
    DEFAULT_PIXEL_SIZE,
    get_all_positions,
    get_color_histogram,
    get_nearest_color,
    merge_mean_color,
    weight_mean_color,
)
from skimage import color as sk_color
from skimage import segmentation as sk_segmentation
from skimage.future import graph as sk_graph
from sklearn.cluster import MiniBatchKMeans
from tqdm import tqdm


class GorkImage:
    def __init__(
        self,
        image_path: str,
        pixel_size: int = DEFAULT_PIXEL_SIZE,
        save_results: bool = True,
        ignore_cache: bool = False,
    ) -> None:
        self.spectrum: typing.Dict[RGBType, int] = collections.defaultdict(int)
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
        image = cv2.resize(
            image, (self.src_width, self.src_height), interpolation=cv2.INTER_NEAREST
        )
        return image

    def generate_pixelated_image_obsolete(self) -> ImageType:
        source_image = cv2.resize(
            src=self.image,
            dsize=(self.dst_width * SENSITIVITY, self.dst_height * SENSITIVITY),
            interpolation=cv2.INTER_NEAREST,
        )
        source_image = cv2.cvtColor(source_image, cv2.COLOR_BGR2RGB)
        pixelated_image = np.empty(
            shape=[self.dst_height, self.dst_width, 3], dtype=np.uint8
        )
        all_positions = get_all_positions(
            x_start=0, x_end=self.dst_width, y_start=0, y_end=self.dst_height
        )

        # STEP 1: decrease colors with skimage
        print("\nmerge colors using Region Adjacency Graph (RAG)...")
        labels_1 = sk_segmentation.slic(source_image, compactness=10, n_segments=500)
        graph = sk_graph.rag_mean_color(source_image, labels_1)
        labels_2 = sk_graph.merge_hierarchical(
            labels_1,
            graph,
            thresh=0.08,
            rag_copy=False,
            in_place_merge=True,
            merge_func=merge_mean_color,
            weight_func=weight_mean_color,
        )
        source_image = sk_color.label2rgb(labels_2, source_image, kind="avg")

        # STEP 2: pixelate image
        palette: typing.Dict[
            RGBType, typing.List[PositionType]
        ] = collections.defaultdict(list)

        print("\npixelate...")
        for pos_x, pos_y in tqdm(
            all_positions,
            total=self.dst_width * self.dst_height,
            ncols=self.dst_width,
            unit="px",
        ):
            histogram = get_color_histogram(source_image, pos_x, pos_y)
            rgb_value, _ = max(histogram.items(), key=operator.itemgetter(1))
            palette[rgb_value].append((pos_x, pos_y))

        print("\nfind nearest colors...")
        for pixel, positions in tqdm(palette.items(), ncols=self.dst_width):
            nearest_color = get_nearest_color(RGB(*pixel))
            self.spectrum[nearest_color.as_tuple] += 1
            for pos_x, pos_y in positions:
                pixelated_image[pos_y, pos_x] = nearest_color.as_tuple

        return pixelated_image

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
