"""Color structures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

ImageType = np.ndarray
RGBType = Tuple[int, int, int]
PositionType = Tuple[int, int]


@dataclass
class RGB:
    """A dataclass for keeping pixel color information."""

    red: int
    green: int
    blue: int

    def __repr__(self) -> str:
        """Return rgb codes."""
        return f"rgb({self.red}, {self.green}, {self.blue})"

    def __gt__(self, other: RGB) -> bool:
        """Check if tbis color is greater than the other."""
        return (
            self.red > other.red and self.green > other.green and self.blue > other.blue
        )

    @property
    def as_tuple(self) -> RGBType:
        """Return object as tuple."""
        return (self.red, self.green, self.blue)


class Color:
    """An object for keeping Xterm color data."""

    def __init__(self, hex_code: str, name: str) -> None:
        """Initialize color object with hex code and name."""
        # We need color names for the accessibility.
        self.hex_code = hex_code.lstrip("#")
        self.name = name
        self.red, self.green, self.blue = (
            int(self.hex_code[i : i + 2], 16) for i in (0, 2, 4)
        )

    def __repr__(self) -> str:
        """Return color name with hex code."""
        return f"{self.name} #{self.hex_code}"

    @property
    def as_rgb(self) -> RGB:
        """Return object as RGB type."""
        return RGB(red=self.red, green=self.green, blue=self.blue)

    @property
    def as_tuple(self) -> Tuple[int, int, int]:
        """Return object as tuple."""
        return self.as_rgb.as_tuple
