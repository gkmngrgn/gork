from gork.palette import COLOR_TREE, PALETTE
from gork.structs import RGB, Color

DEFAULT_PIXEL_SIZE = 10
DEFAULT_N_CLUSTERS = 256


def get_nearest_color(rgb: RGB) -> Color:
    distance, result = COLOR_TREE.query(rgb.as_tuple)
    return PALETTE[result]
