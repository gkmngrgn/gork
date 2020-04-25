import collections
import operator
import typing

from gork.palette import SENSITIVITY
from gork.structs import RGB, PositionType, RGBType
from gork.utils import get_all_positions, get_color_histogram, get_nearest_color
from PIL import Image
from tqdm import tqdm


class GorkImage:
    def __init__(self, image_path: str, width: int) -> None:
        self.spectrum: typing.Dict[typing.Tuple[int, ...], RGB] = {}
        self.image = Image.open(image_path)
        self.src_width, self.src_height = self.image.size
        self.dst_width, self.dst_height = width, int(width / self.image.width * self.image.height)
        self.image = self.generate_pixelated_image()

    def export(self, output: str) -> None:
        image = self.image.resize(size=(self.src_width, self.src_height), resample=Image.BOX)
        image.save(output)

    def generate_pixelated_image(self) -> Image:
        # if self.image.mode not in ["RGB", "L"]:
        #     image = self.image.convert("RGB")

        image_size = (self.dst_width * SENSITIVITY, self.dst_height * SENSITIVITY)
        image = self.image.resize(size=image_size).convert("RGB")
        image_output = Image.new("RGB", size=(self.dst_width, self.dst_height))
        palette: typing.Dict[RGBType, typing.List[PositionType]] = collections.defaultdict(list)
        all_positions = get_all_positions(x_start=0, x_end=self.dst_width, y_start=0, y_end=self.dst_height)

        print("\npixelate...")
        for pos_x, pos_y in tqdm(
            all_positions, total=self.dst_width * self.dst_height, ncols=self.dst_width, unit="px"
        ):
            histogram = get_color_histogram(image, pos_x, pos_y)
            rgb_value = max(histogram.items(), key=operator.itemgetter(1))[0]
            palette[rgb_value].append((pos_x, pos_y))

        print("\nfind nearest colors...")
        for pixel, positions in tqdm(palette.items(), ncols=self.dst_width):
            nearest_color = get_nearest_color(RGB(*pixel))
            for position in positions:
                image_output.putpixel(position, nearest_color.as_tuple)

        return image_output

    def get_color(self, x: int, y: int) -> RGB:
        pixel = self.image.getpixel(xy=(x, y))
        if pixel not in self.spectrum:
            self.spectrum[pixel] = RGB(*pixel)
        return self.spectrum[pixel]

    def get_spectrum(self) -> typing.List[RGB]:
        return sorted(set(self.spectrum.values()))
