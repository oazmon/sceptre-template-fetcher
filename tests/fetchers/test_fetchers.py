'''
Created on Dec 19, 2017

@author: oazmon
'''

from mock import Mock, patch

from sceptre_template_fetcher.fetchers import Fetcher
from sceptre_template_fetcher.fetchers import FetcherMap
from sceptre_template_fetcher.fetchers import RemoteFetcher


class MockFetcher(Fetcher):
    """
    Fetcher inherits from the abstract base class Fetcher,
    and implements the abstract methods. It is used to allow testing on
    Fetcher, which is not otherwise instantiable.
    """
    mock_result = None

    def fetch(self, argument):
        return self.mock_result


class TestFetcher(object):

    def setup_method(self):
        self.fetcher = MockFetcher('fake-shared-template-dir')
        pass

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'


class MockRemoteFetcher(RemoteFetcher):
    """
    RemoteFetcher inherits from the abstract base class Fetcher,
    and implements the abstract methods. It is used to allow testing on
    RemoteFetcher, which is not otherwise instantiable.
    """
    mock_remote_result = None

    def remote_fetch(self, import_spec):
        return self.mock_remote_result


class TestRemoteFetcher(object):

    def setup_method(self):
        self.fetcher = MockRemoteFetcher('fake-shared-template-dir')
        pass

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch('sceptre_template_fetcher.fetchers.ZipFile')
    def test_fetch_zip_processing(self, mockZipFile):
        self.fetcher.mock_remote_result = ('zip', 'fake-content')
        self.fetcher.fetch({
            'to': 'fake-to'
        })
        mockZipFile.assert_called_once()
        mockZipFile.return_value.__enter__.return_value\
            .extractall.assert_called_once_with('fake-to')

    @patch('sceptre_template_fetcher.fetchers.tarfile.open')
    def test_fetch_tar_processing(self, mock_tarfile_open):
        self.fetcher.mock_remote_result = ('tar', 'fake-content')
        self.fetcher.fetch({
            'to': 'fake-to'
        })
        mock_tarfile_open.assert_called_once()
        mock_tarfile_open.return_value.__enter__.return_value\
            .extractall.assert_called_once_with('fake-to')

    @patch('sceptre_template_fetcher.fetchers.open')
    def test_fetch_other_processing(self, mock_open):
        self.fetcher.mock_remote_result = ('txt', 'fake-content')
        self.fetcher.fetch({
            'to': 'fake-to'
        })
        mock_open.assert_called_once_with('fake-to', 'wb')
        mock_open.return_value.__enter__.return_value\
            .write.assert_called_once_with('fake-content')


class TestFetcherMap(object):

    @patch('sceptre_template_fetcher.fetchers.iter_entry_points')
    def setup_method(self, test_method, mock_iter_entry_points):
        self.mock_entry_point = Mock()
        self.mock_entry_point.name = 'git'
        mock_iter_entry_points.return_value = [
            self.mock_entry_point
        ]
        self.fetcher_map = FetcherMap('fake-shared-template-dir')

    def test_class_correctly_initialised_with_one_fetchers(self):
        assert self.fetcher_map.shared_template_dir == \
            'fake-shared-template-dir'
        assert self.fetcher_map._map == {
            'git': self.mock_entry_point.load.return_value
        }

    def test_fetch(self):
        self.fetcher_map.fetch({})
        fetcher = self.mock_entry_point.load.return_value
        fetcher.assert_called_with('fake-shared-template-dir')
        fetcher.return_value.fetch.assert_called_with({})
