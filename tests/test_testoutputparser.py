import vim
import os
import unittest
import plugin.phpunit as phpunit

from mock import Mock
from mock import patch


class TestOutputParserTest(unittest.TestCase):

    """
    Unit tests for TestOutputParser class.
    """

    TEMP_FILE_PATH = os.path.dirname(__file__) + "/fixtures/error_file.out"

    def setUp(self):
        self.output_manager = phpunit.TestErrorManager()
        self.output_parser = phpunit.TestOutputParser(self.output_manager)
        vim_config = {"g:phpunit_tmpfile": "random_file.out",
                      "g:phpunit_debug": "0"}
        vim.eval = Mock(side_effect=_eval_side_effect(vim_config))
        phpunit.print_error = Mock(side_effect=phpunit.print_error, return_value=None)

    def test_should_return_true_when_line_is_parsed(self):
        # given
        line = "/path/to/test/file/and/line/Test.php:14"
        error_type = "failure"
        error = phpunit.TestError(error_type)
        # when
        with patch.object(phpunit.TestErrorManager, 'add'):
            result = self.output_parser.parseFileLine(line, error)
        # then
        self.assertTrue(result)

    def test_should_return_false_when_line_is_not_parsed(self):
        # given
        line = "/this/not/right/because/of/trace/Test.php - 14"
        error_type = "failure"
        error = phpunit.TestError(error_type)
        # when
        with patch.object(phpunit.TestErrorManager, 'add'):
            result = self.output_parser.parseFileLine(line, error)
        # then
        self.assertFalse(result)

    def test_should_read_error(self):
        # given
        _file = open(self.TEMP_FILE_PATH)
        line = "1) ExampleTest::testBasicExample"
        self.output_parser.parsingType = "failure"
        # when
        self.output_parser.readError(_file, line)
        # then
        self.assertFalse(phpunit.print_error.called)


def _eval_side_effect(vim_config):
        def _decorated_method(*arg):
            return vim_config[arg[0]]
        return _decorated_method
