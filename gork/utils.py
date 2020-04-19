import math
import typing

from gork.palette import COLORS
from gork.structs import RGB, Color


def get_all_positions(
    x_start: int, x_end: int, y_start: int, y_end: int
) -> typing.Iterator[typing.Tuple[int, int]]:
    for pos_y in range(y_start, y_end):
        for pos_x in range(x_start, x_end):
            yield (pos_x, pos_y)


def get_nearest_color(rgb: RGB) -> Color:
    """
    We find the nearest color calculating the Euclidian distance. But here, there's a bit different implementation:
    https://www.compuphase.com/cmetric.htm
    """
    def distance(c1, c2):
        (r1, g1, b1) = c1.as_tuple
        (r2, g2, b2) = c2.as_tuple
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    closest_colors = sorted(COLORS, key=lambda color: distance(color.as_rgb, rgb))
    return closest_colors[0]
