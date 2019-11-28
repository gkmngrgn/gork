import argparse

from gork.effect import ImageEffect
from gork.term import Terminal


class ImageGenerator(object):
    def parse_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="My best image effect.")
        parser.add_argument("src", type=argparse.FileType("rb"), help="original image file path")
        parser.add_argument("dst", type=argparse.FileType("wb"), help="generated image file path")
        parser.add_argument("--show-palette", action="store_true", help="print color palette of image")
        return parser.parse_args()

    def run(self) -> None:
        args = self.parse_args()
        effect = ImageEffect(src=args.src)
        effect.out_image.save(args.dst.name)

        terminal = Terminal(src=args.src)
        terminal.print_image()
        terminal.print_palette()


if __name__ == "__main__":
    image_generator = ImageGenerator()
    image_generator.run()
