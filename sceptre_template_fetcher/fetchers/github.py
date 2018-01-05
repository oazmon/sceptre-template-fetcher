'''
Created on Dec 20, 2017

@author: oazmon
pip install requests
'''
from sceptre_template_fetcher.fetchers import RemoteFetcher
import requests
import os
from os import path
import yaml


DEFAULT_GITHUB_URL = 'https://github.com'


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
        headers = self._get_oauth_header(import_spec.get('oauth'))
        if headers:
            archive_url = self._make_api_archive_url(import_spec)
        else:
            archive_url = self._make_archive_url(import_spec)
        self.logger.info("Requesting url=%s", archive_url)
        response = requests.get(
            archive_url,
            allow_redirects=True,
            headers=headers
        )
        return ('zip', response.content)

    def _make_api_archive_url(self, import_spec):
        return '/'.join([
            import_spec.get('github', DEFAULT_GITHUB_URL),
            'api/v3/repos',
            import_spec['from'],
            'zipball',
            self._make_ref(import_spec)
        ])

    def _make_archive_url(self, import_spec):
        return '/'.join([
            import_spec.get('github', DEFAULT_GITHUB_URL),
            import_spec['from'],
            'archive',
            self._make_ref(import_spec) + ".zip"
        ])

    def _make_ref(self, import_spec):
        if 'commit_id' in import_spec:
            return import_spec['commit_id']
        elif 'tag' in import_spec:
            return import_spec['tag']
        elif 'branch' in import_spec:
            return import_spec['branch']
        else:
            raise KeyError(
                "Must provide in spec 'commit_id', 'tag', or 'branch'"
                )

    def _get_oauth_header(self, oauth_spec):
        if oauth_spec is None:
            return None
        key = oauth_spec['key']

        oauth_path = path.join(
            os.getenv("HOME", ''),
            '.ssh',
            oauth_spec.get('file', 'sceptre_import.yaml')
        )
        with open(oauth_path, 'r') as fobj:
            # yaml is super set of json
            content = yaml.safe_load(fobj.read())
        if content is None or key not in content:
            raise KeyError("Unable to find {} in {}".format(key, oauth_path))
        return {
            'Authorization': 'token ' + content[key],
            'UserAgent': 'SceptreTemplateFetcher/Python'
        }
