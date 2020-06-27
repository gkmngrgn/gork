import argparse

from gork.image import GorkImage
from gork.utils import DEFAULT_PIXEL_SIZE


def run_cli() -> None:
    parser = argparse.ArgumentParser(
        prog="gork",
        description="Pixelate an image and recognize the objects.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    sub_parsers = parser.add_subparsers(
        dest="sub_cmd",
        title="subcommands",
        description="valid subcommands",
        help="additional help",
    )
    sub_cmd_analyzer = add_sub_command(sub_parsers, "analyze")
    add_common_arguments(sub_cmd_analyzer)
    sub_cmd_analyzer.add_argument("--export")

    sub_cmd_export = add_sub_command(sub_parsers, "export")
    add_common_arguments(sub_cmd_export)
    sub_cmd_export.add_argument("destination")
    sub_cmd_export.add_argument(
        "--pixel-size",
        type=int,
        default=DEFAULT_PIXEL_SIZE,
        help="set width of the image as character length",
    )

    sub_cmd_print = add_sub_command(sub_parsers, "print")
    add_common_arguments(sub_cmd_print)
    sub_cmd_print.add_argument("--width")

    args = parser.parse_args()
    if args.sub_cmd is None:
        parser.print_help()
        return

    image = GorkImage(
        image_path=args.source.name,
        pixel_size=args.pixel_size,
        save_results=True,
        ignore_cache=args.ignore_cache,
    )

    if args.sub_cmd == "analyze":
        print_report(image)

    if args.sub_cmd == "export":
        image.export(output=args.destination)

    if args.sub_cmd == "print":
        print_image(image)


def add_sub_command(
    sub_parsers: argparse.Action, cmd_name: str
) -> argparse.ArgumentParser:
    sub_command = sub_parsers.add_parser(
        cmd_name, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    return sub_command


def add_common_arguments(parser) -> None:
    parser.add_argument(
        "source", type=argparse.FileType("rb"), help="original image file path",
    )
    parser.add_argument("--ignore-cache")


def print_report(image: GorkImage) -> None:
    pass


def print_image(image: GorkImage) -> None:
    pass
