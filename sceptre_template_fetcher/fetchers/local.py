'''
Created on Dec 20, 2017

@author: oazmon
'''
import os
from os import path
from sceptre_template_fetcher.fetchers import Fetcher
import shutil


class LocalFetcher(Fetcher):
    '''
    Fetcher for files and directory trees on the local machine.

    :param sceptre_dir: The absolute path to the Sceptre directory.
    :type argument: str
    :param shared_template_dir: The absolute path to the Sceptre
            shared template directory.
    :type argument: str
    '''

    def __init__(self, *args, **kwargs):
        super(LocalFetcher, self).__init__(*args, **kwargs)

    def fetch(self, import_spec):
        '''
        Fetcher for a local file or directory

        :param import_spec: The yaml import stanza for this operation,
            which contains:

            The 'from' key which specifies an absolute path to the
                file or directory to fetch.

            The 'to' key which specifies a path relative to the shared
                template dir where the file or directory is placed.

        :type argument: dict
        '''
        source = import_spec['from']
        if not path.isabs(source):
            source = path.join(
                    self.sceptre_dir,
                    source
                )
        target = import_spec['to']
        target = path.join(
            self.shared_template_dir,
            target
        )
        self.logger.info("Local Copy: from=%s to=%s", source, target)
        if path.isdir(source):
            shutil.copytree(source, target)
        else:
            target_dir = path.dirname(target)
            os.makedirs(target_dir, 0o750)
            shutil.copy(source, target)
