'''
Created on Dec 20, 2017

@author: oazmon
'''
from mock import patch
import pytest
from sceptre_template_fetcher.fetchers.sonotype_nexus \
    import SonotypeNexusFetcher


class Test_SonotypeNexusFetcher(object):

    def setup_method(self):
        self.fetcher = SonotypeNexusFetcher(
            'fake-sceptre-dir',
            'fake-shared-template-dir'
        )
        self.fake_short_artifact = {
                'g': 'fake-group',
                'a': 'fake-artifact',
                'v': 'fake-version'
            }
        self.fake_long_artifact = {
                'g': 'fake-group',
                'a': 'fake-artifact',
                'p': 'fake-package',
                'c': 'fake-class',
                'v': 'fake-version'
            }

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    def test__parse_gav__short(self):
        result = self.fetcher._parse_gav(
            'fake-group:fake-artifact:fake-version'
        )
        assert len(result.keys()) == 3
        assert result == self.fake_short_artifact

    def test__parse_gav__long(self):
        result = self.fetcher._parse_gav(
            'fake-group:fake-artifact:fake-package:fake-class:fake-version'
        )
        assert len(result.keys()) == 5
        assert result == self.fake_long_artifact

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get')
    def test__query_repo_id__found(self, mock_get):
        mock_get.return_value.content = \
            '<fake>' \
            '<totalCount>1</totalCount>' \
            '<repositoryId>fake-repositoryId</repositoryId>' \
            '</fake>'
        result = self.fetcher._query_repo_id(
            'fake-url',
            self.fake_long_artifact,
            'fake-query-params'
        )
        assert result == 'fake-repositoryId'
        mock_get.assert_called_once_with(
            'fake-url/service/local/lucene/search?count=1&fake-query-params',
            allow_redirects=True
        )

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get')
    def test__query_repo_id__not_found(self, mock_get):
        mock_get.return_value.content = \
            '<fake>' \
            '<totalCount>0</totalCount>' \
            '</fake>'
        with pytest.raises(ValueError):
            self.fetcher._query_repo_id(
                'fake-url',
                self.fake_long_artifact,
                'fake-query-params'
            )
        mock_get.assert_called_once_with(
            'fake-url/service/local/lucene/search?count=1&fake-query-params',
            allow_redirects=True
        )

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get')
    def test__get_artifact(self, mock_get):
        mock_get.return_value.content = 'fake-content'
        result = self.fetcher._get_artifact(
            'fake-url',
            'fake-repo-id',
            'fake-query-params'
        )
        assert result == 'fake-content'
        mock_get.assert_called_once_with(
            'fake-url/service/local/artifact/maven/content?'
            'r=fake-repo-id&fake-query-params',
            allow_redirects=True
        )

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.'
           'SonotypeNexusFetcher._get_artifact')
    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.'
           'SonotypeNexusFetcher._query_repo_id')
    def test_remote_fetch(self, mock_query_repo_id, mock_get_artifact):
        mock_query_repo_id.return_value = 'fake-repo-id'
        mock_get_artifact.return_value = 'fake-content'
        result = self.fetcher.remote_fetch({
            'repo_url': 'fake-repo-url',
            'coordinates': 'fake-group:fake-artifact:fake-version'
        })
        assert result == ('zip', 'fake-content')
        mock_query_repo_id.assert_called_once_with(
            'fake-repo-url',
            self.fake_short_artifact,
            'a=fake-artifact&g=fake-group&v=fake-version'
        )
        mock_get_artifact.assert_called_once_with(
            'fake-repo-url',
            'fake-repo-id',
            'a=fake-artifact&g=fake-group&v=fake-version'
        )
