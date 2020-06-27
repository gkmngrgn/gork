import typing

import numpy as np
from gork.palette import COLOR_COUNT, COLORS
from gork.structs import RGB, Color, PositionType

DEFAULT_PIXEL_SIZE = 10
DEFAULT_N_CLUSTERS = 256


def get_all_positions(
    x_start: int, x_end: int, y_start: int, y_end: int
) -> typing.Iterator[PositionType]:
    for pos_y in range(y_start, y_end):
        for pos_x in range(x_start, x_end):
            yield (pos_x, pos_y)


def get_distance(c1: RGB, c2: RGB) -> np.float64:
    """
    An alternative way of finding nearest colors:
    https://www.compuphase.com/cmetric.htm
    """
    (r1, g1, b1) = c1.as_tuple
    (r2, g2, b2) = c2.as_tuple
    r_mean = (r1 + r2) / 2
    dist_r = np.power((r1 - r2), 2)
    dist_g = np.power((g1 - g2), 2)
    dist_b = np.power((b1 - b2), 2)
    return np.sqrt(
        2 * dist_r
        + 4 * dist_g
        + 3 * dist_b
        + ((r_mean * (dist_r - dist_b)) / COLOR_COUNT)
    )


def get_nearest_color(rgb: RGB) -> Color:
    distances = np.empty(COLOR_COUNT, dtype=np.double)
    for index, color in enumerate(COLORS):
        distances[index] = get_distance(color.as_rgb, rgb)
    return COLORS[np.argmin(distances)]
