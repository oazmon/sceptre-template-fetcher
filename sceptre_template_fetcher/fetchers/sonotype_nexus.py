'''
Created on Dec 20, 2017

@author: oazmon
pip install repositorytools
pip install requests
'''
from sceptre_template_fetcher.fetchers import RemoteFetcher
import repositorytools
import requests


class SonotypeNexusFetcher(RemoteFetcher):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(SonotypeNexusFetcher, self).__init__(*args, **kwargs)

    def remote_fetch(self, import_spec):
        remote_artifact = repositorytools.RemoteArtifact.\
            from_repo_id_and_coordinates(
                import_spec['repo_id'],
                import_spec['coordinates']
            )
        client = repositorytools.repository_client_factory()
        client.resolve_artifact(remote_artifact)
        response = requests.get(remote_artifact.url, allow_redirects=True)
        return (remote_artifact.extension, response.content)
