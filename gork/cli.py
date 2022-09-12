"""GORK command line interface."""
import argparse

from gork.image import GorkImage
from gork.palette import DEFAULT_WIDTH, PALETTE
from gork.structs import RGBType

ANSI_ESC = "\x1B["
ANSI_CLR = "38;5;{fg};48;5;{bg}"
ANSI_CHR = "m▀"
ANSI_RES = "\x1b[0m"


class ImageGenerator:
    """Pixelated image generator."""

    @staticmethod
    def get_ansi_color_code(
        top_color: RGBType, bottom_color: RGBType, repeat: int = 1
    ) -> str:
        """Get ANSI color code."""

        def ccode(rgb: RGBType) -> int:
            return PALETTE.index(tuple(rgb))

        code_block = [
            "".join(
                [
                    ANSI_ESC,
                    ANSI_CLR.format(fg=ccode(top_color), bg=ccode(bottom_color)),
                    ANSI_CHR,
                    ANSI_RES,
                ]
            )
            for _ in range(repeat)
        ]
        return "".join(code_block)

    def parse_args(self) -> argparse.Namespace:
        """Parse CLI arguments."""
        parser = argparse.ArgumentParser(description="My best image effect.")
        parser.add_argument(
            dest="src", type=argparse.FileType("rb"), help="original image file path"
        )
        parser.add_argument(
            "-o",
            "--output",
            dest="output",
            type=argparse.FileType("wb"),
            help="export image to a file",
        )
        parser.add_argument(
            "-p",
            "--show-palette",
            dest="palette",
            action="store_true",
            help="print color palette of image",
        )
        parser.add_argument(
            "-w",
            "--width",
            dest="width",
            type=int,
            default=DEFAULT_WIDTH,
            help="set width of the image as character length",
        )
        return parser.parse_args()

    def print_image(self, image: GorkImage) -> None:
        """Print pixelated image preview in terminal."""
        print("\npreview...")

        lines = []
        for half_y in range(image.dst_height // 2):
            pos_y = 2 * half_y
            line = [
                self.get_ansi_color_code(
                    top_color=image.get_color(pos_x, pos_y),
                    bottom_color=image.get_color(pos_x, pos_y + 1),
                )
                for pos_x in range(image.dst_width)
            ]
            lines.append("".join(line))

        print("\n".join(lines), flush=True)

    def print_palette(self, image: GorkImage) -> None:
        """Print pixelated image colors."""
        print("\ncolors...")

        output = []
        for color, count in image.get_spectrum()[:10]:
            color_code = self.get_ansi_color_code(
                color.as_tuple, color.as_tuple, repeat=2
            )
            output.append(f"{color_code} {color.name}, {count} pixels\n\n")

        print("".join(output))

    def run(self) -> None:
        """Run CLI app for the parsed arguments."""
        args = self.parse_args()
        image = GorkImage(image_path=args.src.name, width=args.width)

        self.print_image(image=image)

        if args.palette is True:
            self.print_palette(image=image)

        if args.output:
            image.export(output=args.output.name)


def run_cli() -> None:
    """Run image generator."""
    image_generator = ImageGenerator()
    image_generator.run()
