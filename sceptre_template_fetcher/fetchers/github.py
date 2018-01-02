'''
Created on Dec 20, 2017

@author: oazmon
pip install requests
'''
from sceptre_template_fetcher.fetchers import RemoteFetcher
import requests


class GithubFetcher(RemoteFetcher):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(GithubFetcher, self).__init__(*args, **kwargs)

    def remote_fetch(self, import_spec):
        repo_url = import_spec['from']
        if 'commit_id' in import_spec:
            target = import_spec['commit_id']
        elif 'tag' in import_spec:
            target = import_spec['tag']
        elif 'branch' in import_spec:
            target = import_spec['branch']
        else:
            raise KeyError(
                "Must provide in spec 'commit_id', 'tag', or 'branch'"
                )
        archive_url = '/'.join([
            repo_url,
            'archive',
            target
        ])
        response = requests.get(archive_url, allow_redirects=True)
        return ('zip', response.content)
