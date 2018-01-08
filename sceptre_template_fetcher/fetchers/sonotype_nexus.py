'''
Created on Dec 20, 2017

@author: oazmon
pip install requests
'''
from sceptre_template_fetcher.fetchers import RemoteFetcher
import requests
from xml.etree import ElementTree


DEFAULT_NEXUS_REPO = 'https://repo.maven.apache.org/maven2'


class SonotypeNexusFetcher(RemoteFetcher):
    '''
    Fetcher for Nexus Artifacts

    :param sceptre_dir: The absolute path to the Sceptre directory.
    :type argument: str
    :param shared_template_dir: The absolute path to the Sceptre
            shared template directory.
    :type argument: str
    '''

    def __init__(self, *args, **kwargs):
        super(SonotypeNexusFetcher, self).__init__(*args, **kwargs)

    def remote_fetch(self, import_spec):
        '''
        Fetcher a Nexus Artifact

        :param import_spec: The yaml import stanza for this operation.
            The 'repo_url' must specify a base URL to a Nexus repository.
            The 'from' must specify a Nexus g-a-v or g-a-p-c-v.
        :type argument: dict

        :return: The type and content of the specified artifact
        :rtype: tuple

        '''
        remote_artifact = self._parse_gav(import_spec['from'])
        repo_url = import_spec.get('repo_url', DEFAULT_NEXUS_REPO)
        artifact_url = self._get_artifact_url(
            repo_url,
            remote_artifact
        )
        response = requests.get(
            artifact_url,
            allow_redirects=True
        )
        return (
            artifact_url,
            remote_artifact.get('e', 'zip'),
            response.content
        )

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

    def _get_artifact_url(self, repo_url, remote_artifact):
        items = remote_artifact.items()
        # so compares of query_params always work
        items.sort()
        query_params = '&'.join(
            [item[0] + '=' + item[1] for item in items]
        )

        find_repo_id_url = \
            "{}/service/local/lucene/search?count=1&{}".format(
                repo_url,
                query_params
            )
        response = requests.get(
            find_repo_id_url,
            allow_redirects=True
        )
        tree = ElementTree.fromstring(response.content)
        count_element = tree.find('totalCount')
        if count_element is None or count_element.text == '0':
            raise ValueError("gav not found using url=" + find_repo_id_url)
        repo_ids = tree.findall('.//repositoryId')
        repo_id = repo_ids[0].text
        self.logger.debug(
            "%s was found in repo: '%s'",
            remote_artifact['a'],
            repo_id
        )

        return "{}/service/local/artifact/maven/content?r={}&{}".format(
            repo_url,
            repo_id,
            query_params
        )
