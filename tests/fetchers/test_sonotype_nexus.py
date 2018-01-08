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
        self.fake_query_param = \
            '&a=fake-artifact&c=fake-class&g=fake-group'\
            '&p=fake-package&v=fake-version'

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
    def test__get_artifact_url__found(self, mock_get):
        mock_get.return_value.content = \
            '<fake>' \
            '<totalCount>1</totalCount>' \
            '<repositoryId>fake-repositoryId</repositoryId>' \
            '</fake>'
        result = self.fetcher._get_artifact_url(
            'fake-url',
            self.fake_long_artifact
        )
        assert result == 'fake-url/service/local/artifact/maven/content' + \
            '?r=fake-repositoryId' + \
            self.fake_query_param
        mock_get.assert_called_once_with(
            'fake-url/service/local/lucene/search?count=1' +
            self.fake_query_param,
            allow_redirects=True
        )

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get')
    def test__query_repo_id__not_found(self, mock_get):
        mock_get.return_value.content = \
            '<fake>' \
            '<totalCount>0</totalCount>' \
            '</fake>'
        with pytest.raises(ValueError):
            self.fetcher._get_artifact_url(
                'fake-url',
                self.fake_long_artifact
            )
        mock_get.assert_called_once_with(
            'fake-url/service/local/lucene/search?count=1' +
            self.fake_query_param,
            allow_redirects=True
        )

    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get')
    @patch('sceptre_template_fetcher.fetchers.sonotype_nexus.'
           'SonotypeNexusFetcher._get_artifact_url')
    def test_remote_fetch(self, mock_get_artifact_url, mock_get_artifact):
        mock_get_artifact_url.return_value = 'fake-repo-url'
        mock_get_artifact.return_value.content = 'fake-content'
        result = self.fetcher.remote_fetch({
            'repo_url': 'fake-repo-url',
            'from': 'fake-group:fake-artifact:fake-version'
        })
        assert result == ('fake-repo-url', 'zip', 'fake-content')
        mock_get_artifact_url.assert_called_once_with(
            'fake-repo-url',
            self.fake_short_artifact
        )
        mock_get_artifact.assert_called_once_with(
            'fake-repo-url',
            allow_redirects=True
        )
