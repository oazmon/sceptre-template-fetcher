'''
Created on Dec 20, 2017

@author: oazmon
pip install artifactory
'''
from os import path
import artifactory
from sceptre_template_fetcher.fetchers import RemoteFetcher


class ArtifactoryFetcher(RemoteFetcher):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(ArtifactoryFetcher, self).__init__(*args, **kwargs)

    def remote_fetch(self, import_spec):
        artifactory_path = artifactory.ArtifactoryPath(import_spec['from'])
        extension = path.splitext(import_spec['from'])[1][1:]
        with artifactory_path.open() as fobj:
            content = fobj.read()
        return (extension, content)
