import os

import click
from click_default_group import DefaultGroup
from clu.tools import cli_coro

from sdsstools.daemonizer import DaemonGroup

from lvmscraper.actor.actor import ScraperActor


@click.group(cls=DefaultGroup, default="actor", default_if_no_args=True)
@click.option(
    "-c",
    "--config",
    "config_file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to the user configuration file.",
)
@click.option(
    "-r",
    "--rmq_url",
    "rmq_url",
    default=None,
    type=str,
    help="rabbitmq url, eg: amqp://guest:guest@localhost:5672/",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Debug mode. Use additional v for more details.",
)
@click.pass_context
def scraper(ctx, config_file, rmq_url, verbose):
    """scraper controller"""

    ctx.obj = {"config_file": config_file, "rmq_url": rmq_url, "verbose": verbose }


@scraper.group(cls=DaemonGroup, prog="scraper_actor", workdir=os.getcwd())
@click.pass_context
@cli_coro
async def actor(ctx):
    """Runs the actor."""

    default_config_file = os.path.join(os.path.dirname(__file__), "etc/scraper.yml")
    config_file = ctx.obj["config_file"] or default_config_file

    print(f"{config_file}")
    scraper_obj = ScraperActor.from_config(config_file, url=ctx.obj["rmq_url"], verbose=ctx.obj["verbose"])

    await scraper_obj.start()
    await scraper_obj.run_forever()

if __name__ == "__main__":
    scraper()
