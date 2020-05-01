from __future__ import annotations

import typing

import numpy as np

ImageType = np.ndarray
RGBType = typing.Tuple[int, int, int]
PositionType = typing.Tuple[int, int]


class RGB:
    def __init__(self, red: int, green: int, blue: int) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self) -> str:
        return f"rgb({self.red}, {self.green}, {self.blue})"

    def __gt__(self, other: RGB) -> bool:
        return self.red > other.red and self.green > other.green and self.blue > other.blue

    @property
    def as_tuple(self) -> RGBType:
        return (self.red, self.green, self.blue)


class Color:
    """
    An object for keeping Xterm color data. We will need color names for the accessibility.
    """

    def __init__(self, hex_code: str, name: str) -> None:
        self.hex_code = hex_code.lstrip("#")
        self.name = name
        self.red, self.green, self.blue = (int(self.hex_code[i : i + 2], 16) for i in (0, 2, 4))

    def __repr__(self) -> str:
        return f"{self.name} #{self.hex_code}"

    @property
    def as_rgb(self) -> RGB:
        return RGB(red=self.red, green=self.green, blue=self.blue)

    @property
    def as_tuple(self) -> typing.Tuple[int, int, int]:
        return self.as_rgb.as_tuple
