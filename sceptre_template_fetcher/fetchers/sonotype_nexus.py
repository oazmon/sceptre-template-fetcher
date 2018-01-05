'''
Created on Dec 20, 2017

@author: oazmon
pip install requests
'''
from sceptre_template_fetcher.fetchers import RemoteFetcher
import requests
from xml.etree import ElementTree


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
        remote_artifact = self._parse_gav(import_spec['coordinates'])
        items = remote_artifact.items()
        # so compares of query_params always work
        items.sort()
        query_params = '&'.join(
            [item[0] + '=' + item[1] for item in items]
        )
        repo_id = self._query_repo_id(
            import_spec['repo_url'],
            remote_artifact,
            query_params
        )
        content = self._get_artifact(
            import_spec['repo_url'],
            repo_id,
            query_params
        )
        return (remote_artifact.get('e', 'zip'), content)

    def _parse_gav(self, gav):
        gav_coord = gav.split(':')
        if len(gav_coord) == 3:
            return {
                'g': gav_coord[0],
                'a': gav_coord[1],
                'v': gav_coord[2]
            }
        else:
            return {
                'g': gav_coord[0],
                'a': gav_coord[1],
                'p': gav_coord[2],
                'c': gav_coord[3],
                'v': gav_coord[4]
            }

    def _query_repo_id(self, repo_url, remote_artifact, query_params):
        url = repo_url + "/service/local/lucene/search?count=1&" + query_params
        response = requests.get(
            url,
            allow_redirects=True
        )
        tree = ElementTree.fromstring(response.content)
        count_element = tree.find('totalCount')
        if count_element is None or count_element.text == '0':
            raise ValueError("gav not found using url=" + url)
        repo_ids = tree.findall('.//repositoryId')
        repo_id = repo_ids[0].text

        self.logger.debug(
            "%s was found in repo: '%s'",
            remote_artifact['a'],
            repo_id
        )
        return repo_id

    def _get_artifact(self, repo_url, repo_id, query_params):
        response = requests.get(
            repo_url +
            "/service/local/artifact/maven/content?r=" +
            repo_id +
            '&' +
            query_params,
            allow_redirects=True
        )
        return response.content
