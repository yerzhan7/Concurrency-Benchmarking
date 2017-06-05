import unittest
import unittest.mock
import sys
import imp

class AllLangsHandledTests(unittest.TestCase):
#===============================================================================
    def setUp(self):
        init_dict = {("Lang1", "bench1"): "lang1/bench1/",
                     ("Lang1", "bench2"): "lang1/bench2/",
                     ("Lang2", "bench1"): "lang2/bench1/",
                     ("Lang2", "bench2"): "lang2/bench2/",}
        self.init_workdir = "workdir"

        self.mock_lang_cfg = unittest.mock.Mock()

        with unittest.mock.patch.dict("sys.modules", {"lang_cfg": self.mock_lang_cfg}):
            import compilation_executor
            # Hack - otherwise stuff sometimes goes wrong
            # Buuuut, since these are unit tests and not production code, it doesn't matter
            # as long as we're testing the right thing.
            imp.reload(compilation_executor)

        self.ce = compilation_executor.CompilationExecutor(init_dict, self.init_workdir)


#===============================================================================
    def test_init(self):
        predicted_calls = [unittest.mock.call("Lang1", self.init_workdir),
                           unittest.mock.call("Lang2", self.init_workdir)]
        actual_calls = self.mock_lang_cfg.create_langunit.mock_calls

        self.assertEqual(sorted(actual_calls), sorted(predicted_calls))


#===============================================================================
    def test_normal_compile(self):

        def side_effect_fn(*args):
            return args[1] + "exe"

        mock_testunit = self.mock_lang_cfg.create_langunit.return_value
        mock_testunit.compile.side_effect = side_effect_fn

        with unittest.mock.patch("compilation_executor.logging.info") as mock_info:
            ce_dict = self.ce.compile_tests()
            
        expected_dict = {"bench1": {"Lang1": "lang1/bench1/exe", "Lang2": "lang2/bench1/exe"},
                         "bench2": {"Lang1": "lang1/bench2/exe", "Lang2": "lang2/bench2/exe"}}
        self.assertEqual(ce_dict, expected_dict)


#===============================================================================
    def test_compilation_problem(self):

        def side_effect_fn(*args):
            if args[1] != "lang2/bench1/":
                return args[1] + "exe"
            else:
                return None

        mock_testunit = self.mock_lang_cfg.create_langunit.return_value
        mock_testunit.compile.side_effect = side_effect_fn

        with unittest.mock.patch("compilation_executor.logging.info") as mock_info:
            ce_dict = self.ce.compile_tests()

        expected_dict = {"bench1": {"Lang1": "lang1/bench1/exe"},
                         "bench2": {"Lang1": "lang1/bench2/exe", "Lang2": "lang2/bench2/exe"}}
        self.assertEqual(ce_dict, expected_dict)


#===============================================================================
    def test_specific_benchmarks(self):

        def side_effect_fn(*args):
            return args[1] + "exe"

        mock_testunit = self.mock_lang_cfg.create_langunit.return_value
        mock_testunit.compile.side_effect = side_effect_fn

        with unittest.mock.patch("compilation_executor.logging.info") as mock_info:
            ce_dict = self.ce.compile_tests(["bench1"])
            
        expected_dict = {"bench1": {"Lang1": "lang1/bench1/exe", "Lang2": "lang2/bench1/exe"}}
        self.assertEqual(ce_dict, expected_dict)


################################################################################
class LangUnhandledTests(unittest.TestCase):
#===============================================================================
    def setUp(self):
        init_dict = {("Lang1", "bench1"): "lang1/bench1/",
                     ("Lang1", "bench2"): "lang1/bench2/",
                     ("Lang2", "bench1"): "lang2/bench1/",
                     ("Lang2", "bench2"): "lang2/bench2/",
                     ("Lang3", "bench2"): "lang2/bench2/",}
        self.init_workdir = "workdir"

        # Throw an exception for unexpected language
        def side_effect_fn(*args):
            if args[0] == "Lang3":
                raise KeyError
            else:
                return self.mock_lang_cfg.create_langunit.return_value

        self.mock_lang_cfg = unittest.mock.Mock()
        self.mock_lang_cfg.create_langunit.side_effect = side_effect_fn

        with unittest.mock.patch.dict("sys.modules", {"lang_cfg": self.mock_lang_cfg}):
            import compilation_executor
            # Hack - otherwise stuff sometimes goes wrong
            # Buuuut, since these are unit tests and not production code, it doesn't matter
            # as long as we're testing the right thing.
            imp.reload(compilation_executor)

        with unittest.mock.patch("compilation_executor.logging.warning") as self.mock_warn:
            self.ce = compilation_executor.CompilationExecutor(init_dict, self.init_workdir)


#===============================================================================
    def test_init_unhandled_lang(self):

        self.assertEqual(set(["Lang1", "Lang2"]), set(self.ce.lang_units.keys()))

        predicted_warning_calls = [unittest.mock.call("No handler for Lang3")]
        actual_warning_calls = self.mock_warn.mock_calls

        self.assertEqual(sorted(predicted_warning_calls), sorted(actual_warning_calls))

        predicted_langunit_calls = [unittest.mock.call("Lang1", self.init_workdir),
                                    unittest.mock.call("Lang2", self.init_workdir),
                                    unittest.mock.call("Lang3", self.init_workdir)]
        actual_langunit_calls = self.mock_lang_cfg.create_langunit.mock_calls

        self.assertEqual(sorted(predicted_langunit_calls), sorted(actual_langunit_calls))


#===============================================================================
    def test_silently_ignore_language(self):

        def side_effect_fn(*args):
            return args[1] + "exe"

        mock_testunit = self.mock_lang_cfg.create_langunit.return_value
        mock_testunit.compile.side_effect = side_effect_fn

        #with unittest.mock.patch("compilation_executor.logging.info") as mock_info:
        ce_dict = self.ce.compile_tests()
            
        expected_dict = {"bench1": {"Lang1": "lang1/bench1/exe", "Lang2": "lang2/bench1/exe"},
                         "bench2": {"Lang1": "lang1/bench2/exe", "Lang2": "lang2/bench2/exe"}}
        self.assertEqual(ce_dict, expected_dict)


if __name__ == "__main__":
    unittest.main()
