import argparse

from gork.image import GorkImage
from gork.palette import DEFAULT_WIDTH, PALETTE
from gork.structs import RGB

ANSI_ESC = "\x1B["
ANSI_CLR = "38;5;{fg};48;5;{bg}"
ANSI_CHR = "m▀"
ANSI_RES = "\x1b[0m"


class ImageGenerator:
    @staticmethod
    def get_ansi_color_code(foreground: RGB, background: RGB) -> str:
        def ccode(rgb: RGB) -> int:
            return PALETTE.index(rgb.as_tuple)

        background = background or foreground
        code_block = [ANSI_ESC, ANSI_CLR.format(fg=ccode(foreground), bg=ccode(background)), ANSI_CHR]
        return "".join(code_block)

    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="My best image effect.")
        parser.add_argument(dest="src", type=argparse.FileType("rb"), help="original image file path")
        parser.add_argument(
            "-o", "--output", dest="output", type=argparse.FileType("wb"), help="export image to a file"
        )
        parser.add_argument(
            "-p", "--show-palette", dest="palette", action="store_true", help="print color palette of image"
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
        print()

        for y in range(image.dst_height // 2):
            y2 = 2 * y

            for x in range(image.dst_width):
                top_color = image.get_color(x=x, y=y2)
                bottom_color = image.get_color(x, y=y2 + 1)
                print(self.get_ansi_color_code(top_color, bottom_color), sep="", end=ANSI_RES, flush=True)

            print()

    def print_palette(self, image: GorkImage) -> None:
        print("\nColors of the image")

        counter = 0

        for rgb in image.get_spectrum():
            print(self.get_ansi_color_code(rgb, rgb), sep="", end=f"{ANSI_RES} ")
            counter += 1

            if counter >= image.dst_width / 2:
                counter = 0
                print("\n")

        print("\n")

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
