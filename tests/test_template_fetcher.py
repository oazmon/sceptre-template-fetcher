
from mock import patch
import pytest
import yaml

# When switch to new version change EnvironmentPathNotFoundError to:
# from sceptre.exceptions import InvalidSceptreDirectoryError
from sceptre.exceptions import EnvironmentPathNotFoundError

from sceptre_template_fetcher.template_fetcher import TemplateFetcher


class TestTemplateFetcher___init__(object):

    @patch("sceptre_template_fetcher.template_fetcher.FetcherMap")
    @patch("sceptre_template_fetcher.template_fetcher.path.isdir")
    def test_correctly_initialised_with_defaults(
        self, mock_isdir, mock_fetcher_map
    ):
        mock_isdir.return_value = True
        self.template_fetcher = TemplateFetcher(
            sceptre_dir='fake-sceptre-dir'
        )
        mock_fetcher_map.assert_called_once_with(
            shared_template_dir=None
        )
        assert self.template_fetcher.sceptre_dir == "fake-sceptre-dir"
        assert self.template_fetcher.shared_template_dir == \
            "fake-sceptre-dir/shared-templates"

    @patch("sceptre_template_fetcher.template_fetcher.FetcherMap")
    @patch("sceptre_template_fetcher.template_fetcher.path.isdir")
    def test_correctly_initialised_with_values(
        self, mock_isdir, mock_fetcher_map
    ):
        mock_isdir.return_value = True
        self.template_fetcher = TemplateFetcher(
            sceptre_dir='fake-sceptre-dir',
            shared_template_dir='fake-shared-dir'
        )
        mock_fetcher_map.assert_called_once_with(
            shared_template_dir='fake-shared-dir'
        )
        assert self.template_fetcher.sceptre_dir == "fake-sceptre-dir"
        assert self.template_fetcher.shared_template_dir == \
            "fake-sceptre-dir/fake-shared-dir"

    @patch("sceptre_template_fetcher.template_fetcher.FetcherMap")
    @patch("sceptre_template_fetcher.template_fetcher.path.isdir")
    def test__invalid_sceptre_dir(
        self, mock_isdir, mock_fetcher_map
    ):
        mock_isdir.return_value = False
        with pytest.raises(EnvironmentPathNotFoundError):
            self.template_fetcher = TemplateFetcher(
                sceptre_dir='fake-sceptre-dir',
                shared_template_dir='fake-shared-dir'
            )
        mock_fetcher_map.assert_not_called()


class TestTemplateFetcher_fetch(object):

    @patch("sceptre_template_fetcher.template_fetcher.FetcherMap")
    @patch("sceptre_template_fetcher.template_fetcher.path.isdir")
    def setup_method(self, test_method, mock_isdir, mock_fetcher_map):
        mock_isdir.return_value = True
        self.mock_fetcher_map = mock_fetcher_map
        self.template_fetcher = TemplateFetcher(
            sceptre_dir='fake-sceptre-dir'
        )

    @patch("sceptre_template_fetcher.template_fetcher.open")
    def test_default_argument(self, mock_open):
        mock_open.return_value.__enter__.return_value.\
            read.return_value = yaml.dump([])
        self.template_fetcher.fetch(None)
        mock_open.assert_called_once_with('fake-sceptre-dir/import.yaml', 'r')
        self.mock_fetcher_map.fetch.assert_not_called()

    def test_missing_import_file(self):
        with pytest.raises(IOError):
            self.template_fetcher.fetch('No Such File')

    @patch("sceptre_template_fetcher.template_fetcher.open")
    def test_bad_yaml_file(self, mock_open):
        mock_open.return_value.__enter__.return_value.\
            read.return_value = "bad yaml"
        with pytest.raises(TypeError):
            self.template_fetcher.fetch('fake-import.yaml')
        mock_open.assert_called_once_with(
            'fake-sceptre-dir/fake-import.yaml',
            'r'
        )

    @patch("sceptre_template_fetcher.template_fetcher.open")
    def test_empty_import_list(self, mock_open):
        mock_open.return_value.__enter__.return_value.\
            read.return_value = yaml.dump([])
        self.template_fetcher.fetch('fake-import.yaml')
        self.mock_fetcher_map.fetch.assert_not_called()
        mock_open.assert_called_once_with(
            'fake-sceptre-dir/fake-import.yaml',
            'r'
        )

    @patch("sceptre_template_fetcher.template_fetcher.open")
    def test_one_directive_import_list(self, mock_open):
        directive = {
            'provider': 'git',
            'url': "https://git/repo/path/to/dir/template.yaml"
        }
        mock_open.return_value.__enter__.return_value.\
            read.return_value = yaml.dump([directive])
        self.template_fetcher.fetch('fake-import.yaml')
        mock_open.assert_called_once_with(
            'fake-sceptre-dir/fake-import.yaml',
            'r'
        )
        self.mock_fetcher_map.return_value.\
            fetch.assert_called_once_with(directive)
