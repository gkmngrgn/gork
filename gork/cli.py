"""GORK command line interface."""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType, Namespace
from pathlib import Path

from gork.ansi_color import get_ansi_color_code
from gork.image import GorkImage


class CLI:
    """CLI for GORK."""

    def __init__(self) -> None:
        """Initialize cli instance with argument parser."""
        self.config_parser()

    def __add_command(self, name: str) -> ArgumentParser:
        """Add sub command with common parameters."""
        sub_parser = self.sub_parsers.add_parser(
            name, formatter_class=ArgumentDefaultsHelpFormatter
        )
        sub_parser.add_argument(
            "source",
            type=FileType("rb"),
            help="original image file path",
        )
        sub_parser.add_argument(
            "--pixel-size",
            type=int,
            default=10,
            help="set width of the image as character length",
        )
        return sub_parser

    def config_parser(self) -> None:
        """Configure argument parser."""
        self.parser = ArgumentParser(
            prog="gork",
            description="Pixelate an image and recognize the objects.",
            formatter_class=ArgumentDefaultsHelpFormatter,
        )
        self.sub_parsers = self.parser.add_subparsers(
            dest="sub_cmd",
            title="subcommands",
            description="valid subcommands",
            help="additional help",
        )
        sub_cmd_analyze = self.__add_command("analyze")
        sub_cmd_analyze.add_argument("--export")

        sub_cmd_export = self.__add_command("export")
        sub_cmd_export.add_argument(
            "destination",
            type=Path,
            help="destination path for the output image",
        )

        self.__add_command("print")

    def run_analyze(self, args: Namespace, image: GorkImage) -> None:
        """Generate report about the pixelated image."""
        print(args)
        print(image)
        print("not ready yet.")

    def run_export(self, args: Namespace, image: GorkImage) -> None:
        """Save output as an image file."""
        image.export(output=str(args.destination))

    def run_print(self, args: Namespace, image: GorkImage) -> None:
        """Print pixelated image to terminal."""
        print(args)
        print("\npreview...")

        lines = []
        for half_y in range(image.dst_height // 2):
            pos_y = 2 * half_y
            line = [
                get_ansi_color_code(
                    image.get_color(pos_x, pos_y),
                    image.get_color(pos_x, pos_y + 1),
                )
                for pos_x in range(image.dst_width)
            ]
            lines.append("".join(line))

        print("\n".join(lines), flush=True)

    def run_cli(self) -> None:
        """Run image generator for parameters."""
        args = self.parser.parse_args()

        if args.sub_cmd is None:
            self.parser.print_help()
            return

        image = GorkImage(
            image_content=args.source.read(),
            pixel_size=args.pixel_size,
        )
        getattr(self, f"run_{args.sub_cmd}")(args, image)
