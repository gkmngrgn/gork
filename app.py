"""GORK runner."""

from gork.cli import CLI


def main() -> None:
    """Define a shortcut function for running cli."""
    cli = CLI()
    cli.run_cli()


if __name__ == "__main__":
    main()
