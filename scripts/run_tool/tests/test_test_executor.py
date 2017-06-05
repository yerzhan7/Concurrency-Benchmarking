import os
import unittest
from unittest.mock import patch
from test_executor import TestExecutor

# Dummy commands to measure, ignoring all arguments after with '#' delimeter
VALID_COMMAND = "true #"
INVALID_COMMAND = "false #"

# Patching os.path.dirname so that TE will look inside 'tests/test_cfg/' for config files
@patch('os.path.dirname', return_value=os.path.dirname(os.path.realpath(__file__)))
class TestTE(unittest.TestCase):
    def setUp(self):
        self.valid_dict = {'valid_config_1': {'go': VALID_COMMAND},
                           'valid_config_2': {'Scalla': VALID_COMMAND,
                                              'pony': VALID_COMMAND}}

    # Helper methods to test whether results dictionary is in correct format (size, keys)
    def dict_test(test_cl, dict, repetitions, steps):
        TestTE.list_test(test_cl, dict['Time in seconds'], repetitions, steps)
        TestTE.list_test(test_cl, dict['User time in seconds'], repetitions, steps)
        TestTE.list_test(test_cl, dict['System time in seconds'], repetitions, steps)
        TestTE.list_test(test_cl, dict['Percent of CPU usage'], repetitions, steps)
        TestTE.list_test(test_cl, dict['Maximum resident set size in KB'], repetitions, steps)
        TestTE.list_test(test_cl, dict['Voluntary context switches'], repetitions, steps)
        TestTE.list_test(test_cl, dict['Involuntary context switches'], repetitions, steps)

    def list_test(test_cl, list, repetitions, steps):
        test_cl.assertEqual(len(list), steps)
        for x in list:
            test_cl.assertEqual(len(x), repetitions)
            for y in x:
                # Testing that all results from 'time' output are positive numbers or 0
                test_cl.assertGreaterEqual(y, 0)

    def test_valid_config_file(self, mock_os_path_dirname):
        repetitions = 3 # number of iterations in this test
        te = TestExecutor(self.valid_dict, repetitions)

        expected_arguments_dict = {'valid_config_1': {'Case with one changing argument and only one step': ['1'],
                                                      'Case with changing range': ['3 10 10', '3 10 20', '3 10 30'],
                                                      'Case with changing steps': ['2 10 300', '5 10 300', '10 10 300'],
                                                      'Case with three arguments fixed at certain value': ['3 100 300'],
                                                      'Case with one changing argument': ['1', '3']},
                                     'valid_config_2': {'Case with one argument fixed at certain value': ['30']}}

        self.assertEqual(te.arguments_dict, expected_arguments_dict)

        actual_result = te.run_tests()

        self.assertEqual(actual_result['valid_config_1']['go']['Case with one changing argument']['Number of Bodies'], [1, 3])
        TestTE.dict_test(self, actual_result['valid_config_1']['go']['Case with one changing argument'], repetitions, 2)

        self.assertEqual(actual_result['valid_config_1']['go']['Case with one changing argument and only one step']['Number of Bodies'], [1])
        TestTE.dict_test(self, actual_result['valid_config_1']['go']['Case with one changing argument and only one step'], repetitions, 1)

        self.assertEqual(actual_result['valid_config_1']['go']['Case with three arguments fixed at certain value']['Number of Bodies'], '3')
        self.assertEqual(actual_result['valid_config_1']['go']['Case with three arguments fixed at certain value']['Number of Steps'], '100')
        self.assertEqual(actual_result['valid_config_1']['go']['Case with three arguments fixed at certain value']['Number of Planets'], '300')
        TestTE.dict_test(self, actual_result['valid_config_1']['go']['Case with three arguments fixed at certain value'], repetitions, 1)

        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing steps']['Number of Bodies'], [2, 5, 10])
        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing steps']['Number of Steps'], '10')
        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing steps']['Number of Planets'], '300')
        TestTE.dict_test(self, actual_result['valid_config_1']['go']['Case with changing steps'], repetitions, 3)

        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing range']['Number of Bodies'], '3')
        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing range']['Number of Steps'], '10')
        self.assertEqual(actual_result['valid_config_1']['go']['Case with changing range']['Number of Planets'], [10, 20, 30])
        TestTE.dict_test(self, actual_result['valid_config_1']['go']['Case with changing range'], repetitions, 3)

        self.assertEqual(actual_result['valid_config_2']['pony']['Case with one argument fixed at certain value']['Number of Bodies'], '30')
        TestTE.dict_test(self, actual_result['valid_config_2']['pony']['Case with one argument fixed at certain value'], repetitions, 1)

        self.assertEqual(actual_result['valid_config_2']['Scalla']['Case with one argument fixed at certain value']['Number of Bodies'], '30')
        TestTE.dict_test(self, actual_result['valid_config_2']['Scalla']['Case with one argument fixed at certain value'], repetitions, 1)

    def test_run_tests_with_only_certain_tests(self, mock_os_path_dirname):
        repetitions = 1 # number of iterations in this test
        te = TestExecutor(self.valid_dict, repetitions)

        actual_result = te.run_tests('valid_config_2')

        self.assertEqual(actual_result['valid_config_2']['pony']['Case with one argument fixed at certain value']['Number of Bodies'], '30')
        TestTE.dict_test(self, actual_result['valid_config_2']['pony']['Case with one argument fixed at certain value'], repetitions, 1)

        self.assertEqual(actual_result['valid_config_2']['Scalla']['Case with one argument fixed at certain value']['Number of Bodies'], '30')
        TestTE.dict_test(self, actual_result['valid_config_2']['Scalla']['Case with one argument fixed at certain value'], repetitions, 1)

    def test_with_invalid_command_should_throw_exception(self, mock_os_path_dirname):
        te = TestExecutor({'valid_config_2': {'go': INVALID_COMMAND}}, 3)
        self.assertRaises(OSError, te.run_tests)

    def test_with_invalid_config_file_should_throw_exceptions(self, mock_os_path_dirname):
        self.assertRaises(ValueError, TestExecutor, {'invalid_config_1': {'go': VALID_COMMAND}}, 3)
        self.assertRaises(ValueError, TestExecutor, {'invalid_config_2': {'go': VALID_COMMAND}}, 3)
        self.assertRaises(IOError, TestExecutor, {'non_existent_config_file': {'go': VALID_COMMAND}}, 3)

if __name__ == '__main__':
    unittest.main()
