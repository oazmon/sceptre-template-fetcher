'''
Created on Dec 20, 2017

@author: oazmon
'''
from mock import patch
from sceptre_template_fetcher.fetchers.sonotype_nexus \
    import SonotypeNexusFetcher


class Test_SonotypeNexusFetcher(object):

    def setup_method(self):
        self.fetcher = SonotypeNexusFetcher('fake-shared-template-dir')
        pass

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch("sceptre_template_fetcher.fetchers.sonotype_nexus.requests.get")
    @patch("sceptre_template_fetcher.fetchers.sonotype_nexus."
           "repositorytools.repository_client_factory")
    def test_remote_fetch(self, mock_client_factory, mock_get):
        result = self.fetcher.remote_fetch({
            'repo_id': 'central',
            'coordinates': 'group:artifact:version'
        })
        mock_client_factory.return_value.resolve_artifact.assert_called_once()
        actual_artifact = mock_client_factory.return_value\
            .resolve_artifact.call_args[0][0]
        assert actual_artifact.artifact == 'artifact'
        assert actual_artifact.classifier == ''
        assert actual_artifact.extension == ''
        assert actual_artifact.group == 'group'
        assert actual_artifact.repo_id == 'central'
        assert actual_artifact.version == 'version'
        assert result == ('', mock_get.return_value.content)
