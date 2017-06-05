import unittest
import random
import string
import tempfile
import os
import copy
from crawler import Crawler

######################################################################
# 
# 
# 
######################################################################


# Helper - returns a random string of argument length
def gen_random_str(length):
    choice_str = string.ascii_letters + string.digits
    rand_lst = [random.choice(choice_str) for _ in range(length)]
    return ''.join(rand_lst)


class CrawlerTests(unittest.TestCase):
    def setUp(self):
        self.langs = ["lang1", "lang2", "lang3"]
        self.tests = ["bench1", "bench2"]

        # Create a temporary directory to be used as root directory for dummy
        # hierarchy.
        self.tempdir = tempfile.TemporaryDirectory()
        self.dir_dict = {}

        keylist = ((lang, test) for lang in self.langs for test in self.tests)

        for key in keylist:
            lang, test = key
            self.dir_dict[key] = self.tempdir.name + os.sep + lang + os.sep + test

        for directory in self.dir_dict.values():
            os.makedirs(directory, 0o700)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_all_tests_in_all_langs(self):
        #self.maxDiff = None # Uncomment to get useful diffs
        the_crawler = Crawler(self.tempdir.name)
        self.assertEqual(the_crawler.get_dict(), self.dir_dict)

    def test_ignore_file(self):
        #self.maxDiff = None # Uncomment to get useful diffs
        ignore_lang = random.choice(self.langs)
        ignore_filename = os.path.join(self.tempdir.name, "ignore.txt")

        with open(ignore_filename, 'w') as f:
            f.write(ignore_lang + '\n')

        dir_dict_cpy = copy.deepcopy(self.dir_dict)

        for key in list(dir_dict_cpy.keys()):
            if key[0] == ignore_lang:
                del dir_dict_cpy[key]

        the_crawler = Crawler(self.tempdir.name)
        self.assertEqual(the_crawler.get_dict(), dir_dict_cpy)

        os.remove(ignore_filename)


    def test_rename_file(self):
        #self.maxDiff = None # Uncomment to get useful diffs
        rename_test = random.choice(self.tests)
        rename_test_lang = random.choice(self.langs)
        rename_filename = os.path.join(self.tempdir.name, rename_test_lang,
                                       rename_test, "rename.txt")

        renamed_testname = "renamed_" + rename_test

        with open(rename_filename, 'w') as f:
            f.write(renamed_testname + '\n')

        dir_dict_cpy = copy.deepcopy(self.dir_dict)
        testpath = dir_dict_cpy[(rename_test_lang, rename_test)]
        del dir_dict_cpy[(rename_test_lang, rename_test)]
        dir_dict_cpy[(rename_test_lang, renamed_testname)] = testpath

        the_crawler = Crawler(self.tempdir.name)
        self.assertEqual(the_crawler.get_dict(), dir_dict_cpy)

        os.remove(rename_filename)


if __name__ == "__main__":
    unittest.main()
