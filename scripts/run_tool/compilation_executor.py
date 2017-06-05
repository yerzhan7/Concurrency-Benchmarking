import lang_cfg
import logging

class CompilationExecutor:
    def __init__(self, test_dict, workdir="work"):
        self.lang_tests = dict()

        # Restructure the dictionary
        for key, val in test_dict.items():
            self.lang_tests.setdefault(key[0], dict())[key[1]] = val

        # Create LangUnit per language
        self.lang_units = dict()

        for lang in self.lang_tests:
            try:
                self.lang_units[lang] = lang_cfg.create_langunit(lang, workdir)
            except KeyError:
                logging.warning("No handler for " + lang)

    def compile_tests(self, tests=[]):
        rtn_dict = dict()

        for lang, val in self.lang_tests.items():
            for testname, testpath in val.items():
                if ((tests == []) or (testname in tests)) and \
                   (lang in self.lang_units):

                    logging.info("Compiling " + lang + " - " + testname)
                    exe_path = self.lang_units[lang].compile(testname, testpath)

                    if exe_path != None:
                        rtn_dict.setdefault(testname, dict())[lang] = exe_path
                    else:
                        logging.warning("Could not compile " + testname + " for " + lang)

        return rtn_dict
