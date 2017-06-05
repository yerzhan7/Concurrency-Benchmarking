import unittest
import unittest.mock
import sys
import os
import logging
import datetime
import argparse

import main

######################################################################
# A LOT OF COPYPASTA! But since these are unit tests and we don't have
# that much time, I can tolerate this.
######################################################################

class GlueTest(unittest.TestCase):

    def test_no_testdir(self):
        testargs = ["main.py"]

        # Dump the error message to /dev/null
        with unittest.mock.patch("sys.argv", testargs), \
             open(os.devnull, 'w') as dev_null, \
             unittest.mock.patch("sys.stderr", dev_null):
            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

        # Exit code is 2
        self.assertEqual(sys_exit.exception.code, 2)

    def test_compile_only_existing_workdir_no_overwrite(self):
        workdir = "the_workdir"
        testargs = ["main.py", "-c", ".", "-w", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            main.logging.debug = mock_msg
            main.logging.info = mock_msg
            main.logging.warning = mock_msg
            main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = True
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock datetime for determinism
            the_time = datetime.datetime.now()
            mock_now = unittest.mock.Mock()
            mock_now.now.return_value = the_time
            main.datetime.datetime = mock_now

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the compilation_executor
            mock_ce_init = unittest.mock.Mock()
            mock_ce = mock_ce_init.return_value
            mock_ce.compile_tests.return_value = {"a": "c"}
            main.compilation_executor.CompilationExecutor = mock_ce_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            mock_rename.assert_called_with(workdir,
                                           (workdir
                                            + "_bak_"
                                            + the_time.strftime(main.BAK_TIME_FMT)))
            mock_makedirs.assert_called_with(workdir)
            mock_dict_to_file.assert_called_with({"a": "c"}, os.path.join(workdir,
                                                                          "intermediate_data",
                                                                          "ce_data"))


    def test_compile_only_existing_workdir_overwrite(self):
        workdir = "the_workdir"
        testargs = ["main.py", "-c", ".", "-ow", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            main.logging.debug = mock_msg
            main.logging.info = mock_msg
            main.logging.warning = mock_msg
            main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = True
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            mock_rmtree = unittest.mock.Mock()
            main.shutil.rmtree = mock_rmtree
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the compilation_executor
            mock_ce_init = unittest.mock.Mock()
            mock_ce = mock_ce_init.return_value
            mock_ce.compile_tests.return_value = {"a": "c"}
            main.compilation_executor.CompilationExecutor = mock_ce_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            mock_rmtree.assert_called_with(workdir)
            self.assertFalse(mock_rename.called)
            mock_makedirs.assert_called_with(workdir)
            mock_dict_to_file.assert_called_with({"a": "c"}, os.path.join(workdir,
                                                                          "intermediate_data",
                                                                          "ce_data"))

    def test_compile_only_non_existing_workdir(self):
        workdir = "the_workdir"
        testargs = ["main.py", "-c", ".", "-w", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            main.logging.debug = mock_msg
            main.logging.info = mock_msg
            main.logging.warning = mock_msg
            main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = False
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            mock_rmtree = unittest.mock.Mock()
            main.shutil.rmtree = mock_rmtree
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the compilation_executor
            mock_ce_init = unittest.mock.Mock()
            mock_ce = mock_ce_init.return_value
            mock_ce.compile_tests.return_value = {"a": "c"}
            main.compilation_executor.CompilationExecutor = mock_ce_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            self.assertFalse(mock_rmtree.called)
            self.assertFalse(mock_rename.called)
            mock_makedirs.assert_called_with(workdir)
            mock_dict_to_file.assert_called_with({"a": "c"}, os.path.join(workdir,
                                                                          "intermediate_data",
                                                                          "ce_data"))

    def test_run_only(self):
        workdir = "the_workdir"
        testargs = ["main.py", "-r", ".", "-w", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            main.logging.debug = mock_msg
            main.logging.info = mock_msg
            main.logging.warning = mock_msg
            main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = False
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            mock_rmtree = unittest.mock.Mock()
            main.shutil.rmtree = mock_rmtree
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the test executor
            mock_te_init = unittest.mock.Mock()
            mock_te = mock_te_init.return_value
            mock_te.run_tests.return_value = {"b": "c"}
            main.test_executor.TestExecutor = mock_te_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            # Mock reading dict from file
            mock_dict_from_file = unittest.mock.Mock()
            mock_dict_from_file.return_value = {"d": "c"}
            main.read_dict_from_file = mock_dict_from_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            mock_te_init.assert_called_with({"d": "c"}, main.RUNS_PER_PT)
            self.assertFalse(mock_rmtree.called)
            self.assertFalse(mock_rename.called)
            self.assertFalse(mock_makedirs.called)
            mock_dict_from_file.assert_called_with(os.path.join(workdir,
                                                                "intermediate_data",
                                                                "ce_data"))
            mock_dict_to_file.assert_called_with({"b": "c"}, os.path.join(workdir,
                                                                          "intermediate_data",
                                                                          "te_data"))


    def test_process_only(self):
        workdir = "the_workdir"
        testargs = ["main.py", "-p", ".", "-w", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            main.logging.debug = mock_msg
            main.logging.info = mock_msg
            main.logging.warning = mock_msg
            main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = False
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            mock_rmtree = unittest.mock.Mock()
            main.shutil.rmtree = mock_rmtree
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the data interpreter
            mock_di_init = unittest.mock.Mock()
            mock_di = mock_di_init.return_value
            main.data_interpreter.DataInterpreter = mock_di_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            # Mock reading dict from file
            mock_dict_from_file = unittest.mock.Mock()
            mock_dict_from_file.return_value = {"f": "c"}
            main.read_dict_from_file = mock_dict_from_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            mock_di_init.assert_called_with({"f": "c"})
            mock_di.generate_csv.assert_called_with()
            mock_di.plot_graph.assert_called_with(False, "eM")
            self.assertFalse(mock_dict_to_file.called)
            self.assertFalse(mock_rmtree.called)
            self.assertFalse(mock_rename.called)
            self.assertFalse(mock_makedirs.called)
            mock_dict_from_file.assert_called_with(os.path.join(workdir,
                                                                "intermediate_data",
                                                                "te_data"))


    def test_normal_execution(self):
        workdir = "the_workdir"
        testargs = ["main.py", ".", "-w", workdir]

        with unittest.mock.patch("sys.argv", testargs):
            # Mock the valid_dir function
            mock_valid_dir = unittest.mock.Mock()
            mock_valid_dir.return_value = "."
            main.valid_dir = mock_valid_dir

            # Mock the logger just so we don't get the messages while
            # running the tests
            mock_basic_cfg = unittest.mock.Mock()
            mock_msg = unittest.mock.Mock()

            main.logging.basicConfig = mock_basic_cfg
            #main.logging.debug = mock_msg
            #main.logging.info = mock_msg
            #main.logging.warning = mock_msg
            #main.logging.critical = mock_msg

            # Mock the os utils
            mock_isdir = unittest.mock.Mock()
            mock_isdir.return_value = False
            main.os.path.isdir = mock_isdir
            mock_rename = unittest.mock.Mock()
            main.os.rename = mock_rename
            mock_rmtree = unittest.mock.Mock()
            main.shutil.rmtree = mock_rmtree
            # Add exception situation here
            mock_makedirs = unittest.mock.Mock()
            main.os.makedirs = mock_makedirs

            # Mock the crawler
            mock_crawler_init = unittest.mock.Mock()
            mock_crawler = mock_crawler_init.return_value
            #mock_crawler.get_dict.return_value = {("a", "b"): "c", ("x", "y"): "z"}
            mock_crawler.get_dict.return_value = {"b": "c"}
            main.crawler.Crawler = mock_crawler_init

            # Mock the compilation_executor
            mock_ce_init = unittest.mock.Mock()
            mock_ce = mock_ce_init.return_value
            mock_ce.compile_tests.return_value = {"a": "c"}
            main.compilation_executor.CompilationExecutor = mock_ce_init

            # Mock the test executor
            mock_te_init = unittest.mock.Mock()
            mock_te = mock_te_init.return_value
            mock_te.run_tests.return_value = {"c": "c"}
            main.test_executor.TestExecutor = mock_te_init

            # Mock the data interpreter
            mock_di_init = unittest.mock.Mock()
            mock_di = mock_di_init.return_value
            main.data_interpreter.DataInterpreter = mock_di_init

            # Mock dumping dict to file
            mock_dict_to_file = unittest.mock.Mock()
            main.dump_dict_to_file = mock_dict_to_file

            with self.assertRaises(SystemExit) as sys_exit:
                main.main()

            self.assertEqual(sys_exit.exception.code, 0)

            mock_basic_cfg.assert_called_with(level=logging.INFO)
            self.assertFalse(mock_rmtree.called)
            self.assertFalse(mock_rename.called)
            mock_makedirs.assert_called_with(workdir)
            call_list = [unittest.mock.call({"a": "c"}, os.path.join(workdir,
                                                                     "intermediate_data",
                                                                     "ce_data")),
                         unittest.mock.call({"c": "c"}, os.path.join(workdir,
                                                                     "intermediate_data",
                                                                     "te_data"))]
            self.assertTrue(call_list == mock_dict_to_file.mock_calls)
            mock_ce_init.assert_called_with({"b": "c"})
            mock_ce.compile_tests.assert_called_with([])
            mock_te_init.assert_called_with({"a": "c"}, main.RUNS_PER_PT)
            self.assertTrue(mock_te.run_tests.called)
            mock_di_init.assert_called_with({"c": "c"})
            self.assertTrue(mock_di.generate_csv.called)
            mock_di.plot_graph.assert_called_with(False, "eM")


class AuxTest(unittest.TestCase):

    def test_invalid_fmt(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            main.valid_fmt("q")


    def test_valid_dir_true(self):
        mock_isdir = unittest.mock.Mock()
        mock_isdir.return_value = True
        main.os.path.isdir = mock_isdir

        self.assertEqual("testdir", main.valid_dir("testdir"))
        mock_isdir.assert_called_with("testdir")


    def test_valid_dir_false(self):
        mock_isdir = unittest.mock.Mock()
        mock_isdir.return_value = False
        main.os.path.isdir = mock_isdir

        with self.assertRaises(argparse.ArgumentTypeError):
            main.valid_dir("testdir")

        mock_isdir.assert_called_with("testdir")

    def test_dict_reading_no_exception(self):
        with unittest.mock.patch("main.open",
                                 unittest.mock.mock_open(read_data= '{"hi": "bye"}'),
                                 create=True) as mock_open:
            self.assertEqual({"hi": "bye"}, main.read_dict_from_file("testfile"))

    def test_dict_reading_bad_dict_exception(self):
        with unittest.mock.patch("main.open",
                                 unittest.mock.mock_open(read_data='{"hi": "bye"'),
                                 create=True) as mock_open:

            mock_logger = unittest.mock.Mock()
            main.logging.critical = mock_logger

            with self.assertRaises(SystemExit) as sys_exit:
                main.read_dict_from_file("testfile")

            self.assertEqual(sys_exit.exception.code, 1)

    def test_dict_reading_bad_dict_exception(self):
        with unittest.mock.patch("main.open",
                                 unittest.mock.mock_open(read_data='{"hi": "bye"'),
                                 create=True) as mock_open:

            mock_logger = unittest.mock.Mock()
            main.logging.critical = mock_logger

            with self.assertRaises(SystemExit) as sys_exit:
                main.read_dict_from_file("testfile")

            mock_logger.assert_called_with("Unrecognised intermediate data")
            self.assertEqual(sys_exit.exception.code, 1)

    def test_dict_reading_no_file_exception(self):
        mock_open = unittest.mock.mock_open()
        mock_open.side_effect = FileNotFoundError

        with unittest.mock.patch("main.open", mock_open, create=True):

            mock_logger = unittest.mock.Mock()
            main.logging.critical = mock_logger

            with self.assertRaises(SystemExit) as sys_exit:
                main.read_dict_from_file("testfile")

            mock_logger.assert_called_with("Intermediate data file testfile does not exist")
            self.assertEqual(sys_exit.exception.code, 1)

    def test_dict_dumping_no_exception(self):
        mock_exists = unittest.mock.Mock()
        mock_exists.return_value = False
        main.os.path.exists = mock_exists
        mock_makedirs = unittest.mock.Mock()
        main.os.makedirs = mock_makedirs

        dict_dir = "a/b/testfile"

        mock_open = unittest.mock.mock_open()

        with unittest.mock.patch("main.open", mock_open, create=True):
            main.dump_dict_to_file({"a": "b"}, dict_dir)

            mock_exists.assert_called_with("a/b")
            mock_makedirs.assert_called_with("a/b")
            mock_open().write.assert_called_with("{'a': 'b'}")

    def test_dict_dumping_exception(self):
        mock_exists = unittest.mock.Mock()
        mock_exists.return_value = True
        main.os.path.exists = mock_exists
        mock_makedirs = unittest.mock.Mock()
        main.os.makedirs = mock_makedirs

        dict_dir = "a/b/testfile"

        mock_open = unittest.mock.mock_open()
        mock_open.side_effect = ValueError

        with unittest.mock.patch("main.open", mock_open, create=True):
            mock_logger = unittest.mock.Mock()
            main.logging.critical = mock_logger

            with self.assertRaises(SystemExit) as sys_exit:
                main.dump_dict_to_file({"a": "b"}, dict_dir)

            self.assertEqual(sys_exit.exception.code, 1)

            mock_logger.assert_called_with("Could not write to a/b/testfile")
            mock_exists.assert_called_with("a/b")
            self.assertFalse(mock_makedirs.called)
            #mock_open().write.assert_called_with("{'a': 'b'}")

if __name__ == "__main__":
    unittest.main()
