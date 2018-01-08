# -*- coding: utf-8 -*-

"""
sceptre_migration_tool.cli

This module implements the Sceptre Migration Tool CLI
"""

import os
import logging
from logging import Formatter
import warnings

import click
import colorama
import yaml

from sceptre import cli as sceptre_cli
from . import __version__
from template_fetcher import TemplateFetcher


@click.group()
@click.version_option(version=__version__, prog_name="Sceptre Migration Tool")
@click.option("--debug", is_flag=True, help="Turn on debug logging.")
@click.option(
    "--dir", "directory", help="Specify sceptre_migration_tool directory.")
@click.option(
    "--var", multiple=True, help="A variable to template into config files.")
@click.option(
    "--var-file", type=click.File("rb"),
    help="A YAML file of variables to template into config files.")
@click.pass_context
def cli(
        ctx, debug, directory, var, var_file
):  # pragma: no cover
    """
    Implements sceptre_template_fetcher's CLI.
    """
    setup_logging(debug)
    colorama.init()
    # Enable deprecation warnings
    warnings.simplefilter("always", DeprecationWarning)
    ctx.obj = {
        "options": {},
        "sceptre_dir": directory if directory else os.getcwd()
    }
    user_variables = {}
    if var_file:
        user_variables.update(yaml.safe_load(var_file.read()))
    if var:
        # --var options overwrite --var-file options
        for variable in var:
            variable_key, variable_value = variable.split("=")
            user_variables.update({variable_key: variable_value})
    if user_variables:
        ctx.obj["options"]["user_variables"] = user_variables


@cli.command(name="fetch-shared-templates")
@click.option("--import-file", "import_file",
              help="Specify the import specification file.")
@click.option("--shared-dir", "shared_template_dir",
              help="Specify the shared templates directory.")
@click.pass_context
@sceptre_cli.catch_exceptions
def fetch_shared_templates(ctx, import_file, shared_template_dir):
    """
    Import templates.
    """
    sceptre_dir = ctx.obj["sceptre_dir"]
    fetcher = TemplateFetcher(
        sceptre_dir=sceptre_dir,
        shared_template_dir=shared_template_dir,
    )
    fetcher.fetch(import_file)


def setup_logging(debug):
    """
    Sets up logging.

    By default, the python logging module is configured to push logs to stdout
    as long as their level is at least INFO. The log format is set to
    "[%(asctime)s] - %(name)s - %(message)s" and the date format is set to
    "%Y-%m-%d %H:%M:%S".

    After this function has run, modules should:

    .. code:: python

        import logging

        logging.getLogger(__name__).info("my log message")

    :param debug: A flag indication whether to turn on debug logging.
    :type debug: bool
    :no_colour: A flag to indicating whether to turn off coloured output.
    :type no_colour: bool
    :returns: A logger.
    :rtype: logging.Logger
    """
    if debug:
        sceptre_logging_level = logging.DEBUG
        logging.getLogger("botocore").setLevel(logging.INFO)
    else:
        sceptre_logging_level = logging.INFO
        # Silence botocore logs
        logging.getLogger("botocore").setLevel(logging.CRITICAL)

    formatter = Formatter(
        fmt="[%(asctime)s] - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger("sceptre_template_fetcher")
    logger.addHandler(log_handler)
    logger.setLevel(sceptre_logging_level)
    return logger
