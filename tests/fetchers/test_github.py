'''
Created on Dec 20, 2017

@author: oazmon
'''
import pytest
from mock import patch
from sceptre_template_fetcher.fetchers.github \
    import GithubFetcher


class Test_GithubFetcher(object):

    def setup_method(self):
        self.fetcher = GithubFetcher('fake-shared-template-dir')
        pass

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_commit_id(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-repo-url',
            'commit_id': 'fake_commit_id',
            'tag': 'fake_tag',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'fake-repo-url/archive/fake_commit_id',
            allow_redirects=True
        )
        assert result == ('zip', mock_get.return_value.content)

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_tag(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-repo-url',
            'tag': 'fake_tag',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'fake-repo-url/archive/fake_tag',
            allow_redirects=True
        )
        assert result == ('zip', mock_get.return_value.content)

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_branch(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-repo-url',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'fake-repo-url/archive/fake_branch',
            allow_redirects=True
        )
        assert result == ('zip', mock_get.return_value.content)

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_bad(self, mock_get):
        with pytest.raises(KeyError):
            self.fetcher.remote_fetch({
                'from': 'fake-repo-url'
            })
        mock_get.assert_not_called()

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__missing_from(self, mock_get):
        with pytest.raises(KeyError):
            self.fetcher.remote_fetch({
            })
        mock_get.assert_not_called()
