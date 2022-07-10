import argparse

from gork.image import GorkImage
from gork.palette import DEFAULT_WIDTH, PALETTE
from gork.structs import RGBType

ANSI_ESC = "\x1B["
ANSI_CLR = "38;5;{fg};48;5;{bg}"
ANSI_CHR = "m▀"
ANSI_RES = "\x1b[0m"


class ImageGenerator:
    @staticmethod
    def get_ansi_color_code(
        top_color: RGBType, bottom_color: RGBType, repeat: int = 1
    ) -> str:
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
        print("\npreview...")

        lines = []
        for half_y in range(image.dst_height // 2):
            y = 2 * half_y
            line = [
                self.get_ansi_color_code(
                    top_color=image.get_color(x, y),
                    bottom_color=image.get_color(x, y + 1),
                )
                for x in range(image.dst_width)
            ]
            lines.append("".join(line))

        print("\n".join(lines), flush=True)

    def print_palette(self, image: GorkImage) -> None:
        print("\ncolors...")

        output = []
        for index, (color, count) in enumerate(image.get_spectrum()[:10], start=1):
            output.append(
                f"{self.get_ansi_color_code(color.as_tuple, color.as_tuple, repeat=2)} {color.name}, {count} pixels\n\n"
            )

        print("".join(output))

    def run(self) -> None:
        args = self.parse_args()
        image = GorkImage(image_path=args.src.name, width=args.width)

        self.print_image(image=image)

        if args.palette is True:
            self.print_palette(image=image)

        if args.output:
            image.export(output=args.output.name)


def run_cli() -> None:
    image_generator = ImageGenerator()
    image_generator.run()
