
import logging

from click.testing import CliRunner
from mock import patch

from sceptre_template_fetcher import cli


class TestCli(object):

    def setup_method(self, test_method):
        self.runner = CliRunner()

    def test_setup_logging_with_debug(self):
        logger = cli.setup_logging(True)
        assert logger.getEffectiveLevel() == logging.DEBUG
        assert logging.getLogger("botocore").getEffectiveLevel() == \
            logging.INFO

        # Silence logging for the rest of the tests
        logger.setLevel(logging.CRITICAL)

    def test_setup_logging_without_debug(self):
        logger = cli.setup_logging(False)
        assert logger.getEffectiveLevel() == logging.INFO
        assert logging.getLogger("botocore").getEffectiveLevel() == \
            logging.CRITICAL

        # Silence logging for the rest of the tests
        logger.setLevel(logging.CRITICAL)

    @patch("sceptre_template_fetcher.cli.TemplateFetcher")
    @patch("sceptre_template_fetcher.cli.os.getcwd")
    def test_fetch_shared_templates_default_args(
            self, mock_getcwd, mock_template_fetcher
    ):
        mock_getcwd.return_value = 'fake-sceptre-dir'
        result = self.runner.invoke(
            cli.cli,
            ["fetch-shared-templates"]
        )
        assert result.exit_code == 0
        mock_template_fetcher.assert_called_with(
            sceptre_dir='fake-sceptre-dir',
            shared_template_dir=None
        )
        mock_template_fetcher.return_value\
            .fetch.assert_called_once()

    @patch("sceptre_template_fetcher.cli.TemplateFetcher")
    @patch("sceptre_template_fetcher.cli.os.getcwd")
    def test_fetch_shared_templates_explicit_args(
            self, mock_getcwd, mock_template_fetcher
    ):
        mock_getcwd.return_value = 'fake-sceptre-dir'
        result = self.runner.invoke(
            cli.cli,
            [
                "fetch-shared-templates",
                "--import-file", "fake-import.yaml",
                "--shared-dir", "fake-template-dir"
            ]
        )
        assert result.exit_code == 0
        mock_template_fetcher.assert_called_with(
            sceptre_dir='fake-sceptre-dir',
            shared_template_dir="fake-template-dir"
        )
        mock_template_fetcher.return_value\
            .fetch.assert_called_once()
