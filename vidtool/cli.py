"""Console script for vidtool."""
import sys

import click

from . import vidtool


@click.command()
def main(args=None):
    """Console script for vidtool."""
    click.echo(
        "Replace this message by putting your code into " "vidtool.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")
    vidtool.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
