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
        self.fetcher = GithubFetcher(
            'fake-sceptre-dir',
            'fake-shared-template-dir'
        )

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_commit_id(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-git-repo',
            'commit_id': 'fake_commit_id',
            'tag': 'fake_tag',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'https://github.com/fake-git-repo/archive/fake_commit_id.zip',
            allow_redirects=True,
            headers=None
        )
        assert result == ('zip', mock_get.return_value.content)

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_tag(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-git-repo',
            'tag': 'fake_tag',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'https://github.com/fake-git-repo/archive/fake_tag.zip',
            allow_redirects=True,
            headers=None
        )
        assert result == ('zip', mock_get.return_value.content)

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    def test_remote_fetch__by_branch(self, mock_get):
        result = self.fetcher.remote_fetch({
            'from': 'fake-git-repo',
            'branch': 'fake_branch'
        })
        mock_get.assert_called_once_with(
            'https://github.com/fake-git-repo/archive/fake_branch.zip',
            allow_redirects=True,
            headers=None
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

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    @patch("sceptre_template_fetcher.fetchers.github.open")
    def test_remote_fetch__with_missing_auth_key(self, mock_open, mock_get):
        mock_open.return_value.__enter__.return_value.\
            read.return_value = ''
        with pytest.raises(KeyError):
            self.fetcher.remote_fetch({
                'from': 'fake-git-repo',
                'branch': 'fake_branch',
                'oauth': {
                    'file': 'fake-file',
                    'key': 'fake-key'
                }
            })
        mock_get.assert_not_called()

    @patch("sceptre_template_fetcher.fetchers.github.requests.get")
    @patch("sceptre_template_fetcher.fetchers.github.open")
    def test_remote_fetch__with_auth_header(self, mock_open, mock_get):
        mock_open.return_value.__enter__.return_value.\
            read.return_value = 'fake-key: fake-token'
        result = self.fetcher.remote_fetch({
            'from': 'fake-git-repo',
            'branch': 'fake_branch',
            'oauth': {
                'file': 'fake-file',
                'key': 'fake-key'
            }
        })
        mock_get.assert_called_once_with(
            'https://github.com/api/v3/repos/'
            'fake-git-repo/zipball/fake_branch',
            allow_redirects=True,
            headers={
                'UserAgent': 'SceptreTemplateFetcher/Python',
                'Authorization': 'token fake-token'
            }
        )
        assert result == ('zip', mock_get.return_value.content)
