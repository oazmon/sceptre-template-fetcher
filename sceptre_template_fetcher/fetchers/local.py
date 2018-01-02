'''
Created on Dec 20, 2017

@author: oazmon
pip install shutil
'''
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
        target_dir = path.join(
            self.shared_template_dir,
            import_spec['to']
        )
        source = import_spec['from']
        if path.isdir(source):
            shutil.copytree(source, target_dir)
        else:
            shutil.copy(source, target_dir)
