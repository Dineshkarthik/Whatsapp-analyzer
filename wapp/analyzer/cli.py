"""Whatsapp Analyzer CLI."""
import click

from wapp.analyzer.app import start


@click.group()
def main():
    """
    WhatsApp-Analyzer is a simple analytics and visualization Python app.
    """
    pass


@main.command()
@click.option(
    "-p", "--port", help="Port on which the app will run", default=5000
)
def run(port):
    """
    Starts Whatsapp-analyser --> wapp-analyzer run

    You can pass  custom port number on which the app needs to run.

	>>>    wapp-analyzer run -p 8080

    If none given it takes 5000 as default.
    """
    start(port)
