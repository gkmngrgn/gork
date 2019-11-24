import argparse

from effect import ImageEffect


class ImageGenerator(object):
    def parse_args(self):
        parser = argparse.ArgumentParser(description="My best image effect.")
        parser.add_argument("src", type=argparse.FileType("rb"), help="original image file path")
        parser.add_argument("dst", type=argparse.FileType("wb"), help="generated image file path")
        return parser.parse_args()

    def run(self):
        args = self.parse_args()
        effect = ImageEffect(src=args.src)
        effect.out_image.save(args.dst.name)


if __name__ == "__main__":
    image_generator = ImageGenerator()
    image_generator.run()
