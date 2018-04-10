'''
Created on Dec 20, 2017

@author: oazmon
'''
from mock import patch
from sceptre_template_fetcher.fetchers.local import LocalFetcher


class Test_LocalFetcher(object):

    def setup_method(self):
        self.fetcher = LocalFetcher(
            'fake-sceptre-dir',
            'fake-shared-template-dir'
        )

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch('shutil.copytree')
    @patch('sceptre_template_fetcher.fetchers.local.path.isdir')
    def test_fetch_dir(self, mock_isdir, mock_copytree):
        mock_isdir.return_value = True
        self.fetcher.fetch({
            'provider': 'local',
            'from': '/here',
            'to': 'there'
        })
        mock_copytree.assert_called_once_with(
            '/here',
            'fake-shared-template-dir/there'
        )

    @patch('shutil.copy')
    @patch('sceptre_template_fetcher.fetchers.local.os.makedirs')
    @patch('sceptre_template_fetcher.fetchers.local.path.isdir')
    def test_fetch_file(self, mock_isdir, mock_makedirs, mock_copy):
        mock_isdir.return_value = False
        self.fetcher.fetch({
            'provider': 'local',
            'from': 'here',
            'to': 'there'
        })
        mock_makedirs.assert_called_once_with('fake-shared-template-dir', 0o750)
        mock_copy.assert_called_once_with(
            'fake-sceptre-dir/here',
            'fake-shared-template-dir/there'
        )
