import logzero
import typer

from tenempleo.core import TenEmpleo
from tenempleo.utils import init_logger

app = typer.Typer(add_completion=False)
logger = init_logger()


@app.command()
def notify(
    verbose: bool = typer.Option(False, '--verbose', '-vv', show_default=False),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)
    handler = TenEmpleo()
    handler.notify()


if __name__ == "__main__":
    app()
