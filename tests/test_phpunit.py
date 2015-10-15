import vim
import unittest
import os
import plugin.phpunit as phpunit

from mock import Mock


class PhpUnitTest(unittest.TestCase):

    """
    Unit tests for phpunit module.
    """

    TEMP_FILE_PATH = os.path.dirname(__file__) + "/fixtures/error_file.out"

    def setUp(self):
        vim.command = Mock(return_value=None)
        phpunit.print_error = Mock(side_effect=phpunit.print_error, return_value=None)

    def test_should_pass_message_to_vim_command(self):
        # given
        message = 'random message'
        expected_message = 'echohl Error | echo \"' + message + '\" | echohl None'
        # when
        phpunit.print_error(message)
        # then
        vim.command.assert_called_once_with(expected_message)

    def test_should_throw_exception_when_not_find_tmp_file(self):
        # given
        vim_config = {"g:phpunit_tmpfile": "random_file.out",
                      "g:phpunit_debug": "0"}
        vim.eval = Mock(side_effect=_eval_side_effect(vim_config))
        # when
        phpunit.parse_test_output()
        # then
        phpunit.print_error.assert_any_call("Failed to find or open the PHPUnit"
                                            + " error log - the command may have"
                                            + " failed")

    def test_should_parse_file(self):
        # given
        vim_config = {"g:phpunit_tmpfile": self.TEMP_FILE_PATH,
                      "g:phpunit_debug": "0"}
        vim.eval = Mock(side_effect=_eval_side_effect(vim_config))
        # when
        phpunit.parse_test_output()
        # then
        self.assertFalse(phpunit.print_error.called)


def _eval_side_effect(vim_config):
        def _decorated_method(*arg):
            return vim_config[arg[0]]
        return _decorated_method

if __name__ == '__main__':
    unittest.main()
