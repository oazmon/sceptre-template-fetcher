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
    Fetcher for Artifactory artifacts

    :param sceptre_dir: The absolute path to the Sceptre directory.
    :type argument: str
    :param shared_template_dir: The absolute path to the Sceptre
            shared template directory.
    :type argument: str
    '''

    def __init__(self, *args, **kwargs):
        super(ArtifactoryFetcher, self).__init__(*args, **kwargs)

    def remote_fetch(self, import_spec):
        '''
        Fetch Artifactory artifact

        :param import_spec: The yaml import stanza for this operation.
            The 'from' must specify an Artifactory path.
        :type argument: dict

        :return: The type and content of the specified artifact
        :rtype: tuple

        '''
        artifactory_path = artifactory.ArtifactoryPath(import_spec['from'])
        extension = path.splitext(import_spec['from'])[1][1:]
        with artifactory_path.open() as fobj:
            content = fobj.read()
        return (artifactory_path, extension, content)
