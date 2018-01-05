'''
Created on Dec 20, 2017

@author: oazmon
'''
from mock import patch
from sceptre_template_fetcher.fetchers.artifactory \
    import ArtifactoryFetcher


class Test_GithubFetcher(object):

    def setup_method(self):
        self.fetcher = ArtifactoryFetcher(
            'fake-sceptre-dir',
            'fake-shared-template-dir'
        )

    def test_class_correctly_initialised(self):
        assert self.fetcher.shared_template_dir == \
            'fake-shared-template-dir'

    @patch("sceptre_template_fetcher.fetchers.artifactory.artifactory")
    def test_remote_fetch(self, mock_artifactory):
        mock_artifactory.ArtifactoryPath.return_value.\
            open.return_value.__enter__.return_value.\
            read.return_value = 'fake-content'
        result = self.fetcher.remote_fetch({
            'from': 'fake-repo-url.fake_ext'
        })
        mock_artifactory.ArtifactoryPath.assert_called_once_with(
            'fake-repo-url.fake_ext'
        )
        assert result == ('fake_ext', 'fake-content')
