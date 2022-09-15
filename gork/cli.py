"""GORK command line interface."""
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, FileType

from gork.image import GorkImage


def run_cli() -> None:
    """Run image generator for parameters."""
    parser = ArgumentParser(
        prog="gork",
        description="Pixelate an image and recognize the objects.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    sub_parsers = parser.add_subparsers(
        dest="sub_cmd",
        title="subcommands",
        description="valid subcommands",
        help="additional help",
    )
    sub_cmd_analyzer = sub_parsers.add_parser(
        "analyze", formatter_class=ArgumentDefaultsHelpFormatter
    )
    add_common_arguments(sub_cmd_analyzer)
    sub_cmd_analyzer.add_argument("--export")

    sub_cmd_export = sub_parsers.add_parser(
        "export", formatter_class=ArgumentDefaultsHelpFormatter
    )
    add_common_arguments(sub_cmd_export)
    sub_cmd_export.add_argument("destination")
    sub_cmd_export.add_argument(
        "--pixel-size",
        type=int,
        default=10,
        help="set width of the image as character length",
    )

    sub_cmd_print = sub_parsers.add_parser(
        "print", formatter_class=ArgumentDefaultsHelpFormatter
    )
    add_common_arguments(sub_cmd_print)
    sub_cmd_print.add_argument(
        "--width",
        type=int,
        required=True,
        help="set width of the image as character length",
    )

    args = parser.parse_args()
    if args.sub_cmd is None:
        parser.print_help()
        return

    image = GorkImage(
        image_content=args.source.read(),
        # save_results=True,
        # ignore_cache=args.ignore_cache,
    )

    if hasattr(args, "width"):
        image.pixel_size = image.src_width // args.width
    else:
        image.pixel_size = args.pixel_size

    # SUBCOMMANDS
    if args.sub_cmd == "analyze":
        run_analyze(image)

    if args.sub_cmd == "export":
        run_export(image, args.destination)

    if args.sub_cmd == "print":
        run_print(image)


def add_common_arguments(parser: ArgumentParser) -> None:
    """Add common arguments for each sub commands."""
    parser.add_argument(
        "source",
        type=FileType("rb"),
        help="original image file path",
    )
    parser.add_argument("--ignore-cache")


def run_analyze(_: GorkImage) -> None:
    """Generate report about the pixelated image."""
    print("not ready yet.")


def run_export(image: GorkImage, destination: str) -> None:
    """Save output as an image file."""
    image.export(output=destination)


def run_print(_: GorkImage) -> None:
    """Print pixelated image to terminal."""
    print("not ready yet.")
