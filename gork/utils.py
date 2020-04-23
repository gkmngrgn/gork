import math
import typing

from gork.palette import COLORS
from gork.structs import RGB, Color


def get_all_positions(x_start: int, x_end: int, y_start: int, y_end: int) -> typing.Iterator[typing.Tuple[int, int]]:
    for pos_y in range(y_start, y_end):
        for pos_x in range(x_start, x_end):
            yield (pos_x, pos_y)


def get_nearest_color(rgb: RGB) -> Color:
    def distance(c1: RGB, c2: RGB) -> float:
        if c1 == c2:
            return 0

        (r1, g1, b1) = c1.as_tuple
        (r2, g2, b2) = c2.as_tuple
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    closest_colors = sorted(COLORS, key=lambda color: distance(color.as_rgb, rgb))
    return closest_colors[0]
