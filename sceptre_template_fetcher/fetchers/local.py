'''
Created on Dec 20, 2017

@author: oazmon
pip install shutil
'''
import os
from os import path
from sceptre_template_fetcher.fetchers import Fetcher
import shutil


class LocalFetcher(Fetcher):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(LocalFetcher, self).__init__(*args, **kwargs)

    def fetch(self, import_spec):
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
            os.makedirs(target_dir, 0750)
            shutil.copy(source, target)
