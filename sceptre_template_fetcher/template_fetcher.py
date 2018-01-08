# -*- coding: utf-8 -*-

"""
sceptre_template_fetcher.template_fetcher

This module imports templates into a shared templates directory

"""

from __future__ import print_function
import logging
import yaml
import os
from os import path
from six import string_types

# When switch to new version change EnvironmentPathNotFoundError to:
# from sceptre.exceptions import InvalidSceptreDirectoryError
from sceptre.exceptions import EnvironmentPathNotFoundError
from fetchers import FetcherMap


class TemplateFetcher(object):
    """
    This module implements the fetching of shared templates from
    locations outside of 'sceptre_dir'. The fetching uses fetch
    providers that know how to fetch from different locations:
    a local directory, git, etc.

    :param sceptre_dir: The absolute path to the Sceptre directory.
    :type sceptre_dir: str
    :param shared_template_dir: The path relative to sceptre dir
        to the shared template directory.
    :type shared_template_dir: str
    :param import_file: The path relative to sceptre dir to the yaml file.
        that contains the import instructions.
    :type import_file: str
    """

    def __init__(
        self, sceptre_dir, shared_template_dir=None
    ):
        self.logger = logging.getLogger(__name__)
        # Check is valid sceptre project folder
        self._check_valid_sceptre_dir(sceptre_dir)

        self.sceptre_dir = sceptre_dir
        self.shared_template_dir = path.join(
                self.sceptre_dir,
                shared_template_dir
                if shared_template_dir
                else "shared-templates"
            )
        if not path.isdir(self.shared_template_dir):
            os.makedirs(self.shared_template_dir, 0750)

        self._fetcher_map = FetcherMap(
            sceptre_dir=self.sceptre_dir,
            shared_template_dir=self.shared_template_dir
        )

    # From sceptre.config_reader.py
    def _check_valid_sceptre_dir(self, a_path):
        """
        Raises an InvalidSceptreDirectoryError if ``a_path`` is
        not a directory.

        :param shared_template_path: A shared template directory path.
        :type shared_template_path: str
        :raises: sceptre.exceptions.InvalidSceptreDirectoryError
        """
        if not path.isdir(a_path):
            raise EnvironmentPathNotFoundError(a_path)

    def fetch(self, import_file=None):
        """
        Fetch all the shared templates found in the import configuration.

        :raises: sceptre.exceptions.???
        """
        self.logger.info(
            "Importing templates into '%s'",
            self.shared_template_dir
        )
        if not import_file or not path.isabs(import_file):
            if not import_file:
                import_file = "import.yaml"
            import_file = path.join(
                self.sceptre_dir,
                'config',
                import_file
            )
        self.logger.info(
            "Using import config '%s'",
            import_file
        )
        with open(import_file, 'r') as fobj:
            content = fobj.read()
        spec = yaml.safe_load(content)
        if spec and 'imports' in spec:
            if isinstance(spec['imports'], string_types):
                raise TypeError(
                    "{} should be a list of import directives"
                    .format(import_file)
                )
            for import_spec in spec['imports']:
                self._fetcher_map.fetch(import_spec)
