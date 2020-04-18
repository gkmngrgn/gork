import typing


class RGB:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self) -> str:
        return f"({self.red}, {self.green}, {self.blue})"

    def __gt__(self, other) -> bool:
        return self.red > other.red and self.green > other.green and self.blue > other.blue

    @property
    def as_tuple(self):
        return (self.red, self.green, self.blue)


class Color:
    """
    An object for keeping Xterm color data. We will need color names for the accessibility.
    """

    def __init__(self, hex_code: str, name: str) -> None:
        self.hex_code = hex_code

    @property
    def as_rgb(self) -> typing.Tuple[int, int, int]:
        h = self.hex_code.lstrip("#")
        return tuple(int(h[i: i + 2], 16) for i in (0, 2, 4))
