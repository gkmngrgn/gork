"""RGB to ANSI color tool."""
from gork.structs import RGBType


def round_color(color_value: int) -> int:
    """Round color code."""
    quot = 255 / 5
    return round(color_value / quot)


def ansi(rgb: RGBType) -> int:
    """Get ansi value of rgb."""
    red, green, blue = map(round_color, rgb)
    return 16 + 36 * red + 6 * green + blue


def color(character: str, foreground: RGBType, background: RGBType) -> str:
    """Get ansi code of color with the specific character."""
    return f"\x1b[38;5;{ansi(foreground)};48;5;{ansi(background)}m{character}\x1b[0m"


def get_ansi_color_code(
    top_color: RGBType,
    bottom_color: RGBType,
    repeat: int = 1,
) -> str:
    """Get ansi color code to print preview in terminal."""
    code_block = [color("▀", top_color, bottom_color) for _ in range(repeat)]
    return "".join(code_block)
