import collections
import math
import typing

from PIL import Image

from gork.palette import COLORS, SENSITIVITY
from gork.structs import RGB, RGBType, PositionType, Color


def get_all_positions(x_start: int, x_end: int, y_start: int, y_end: int) -> typing.Iterator[PositionType]:
    for pos_y in range(y_start, y_end):
        for pos_x in range(x_start, x_end):
            yield (pos_x, pos_y)


def get_color_histogram(image: Image, pos_x: int, pos_y: int) -> typing.Dict[RGBType, int]:
    histogram: typing.Dict[RGBType, int] = collections.defaultdict(int)

    for pos_x2, pos_y2 in get_all_positions(
        x_start=pos_x * SENSITIVITY,
        x_end=(pos_x + 1) * SENSITIVITY,
        y_start=pos_y * SENSITIVITY,
        y_end=(pos_y + 1) * SENSITIVITY,
    ):
        rgb = RGB(*image.getpixel((pos_x2, pos_y2)))
        histogram[rgb.as_tuple] += 1

    return histogram


def get_distance(c1: RGB, c2: RGB) -> float:
    (r1, g1, b1) = c1.as_tuple
    (r2, g2, b2) = c2.as_tuple
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def get_nearest_color(rgb: RGB) -> Color:
    return min(COLORS, key=lambda color: get_distance(color.as_rgb, rgb))
