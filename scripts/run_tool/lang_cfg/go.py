import os
import logging
import subprocess
import shutil

LANG_NAME = "go"
CC1 = "go"
CC2 = "build"
MISSING_COMPILER = "Compiler for go has not been found."

class LangUnit:

    def __init__(self, workdir):
        # Check if compiler exists in the system
        if shutil.which(CC1) is None:
            raise FileNotFoundError(MISSING_COMPILER)

        # Set the base working directory for language
        self.langdir = workdir + os.sep + LANG_NAME

    def compile(self, testname, testpath):
        test_workdir = self.langdir + os.sep +\
                       testname + os.sep

        current_dir = os.getcwd()
        # Create the working directory for the test
        try:
            os.makedirs(test_workdir)

        except FileExistsError:
            logging.warning(LANG_NAME + " compilation: " + test_workdir + " already exists")

        testpath += os.sep + "src"

        os.chdir(testpath + os.sep)

        cmd = [CC1, CC2, "-o", current_dir + os.sep + test_workdir + testname]


        # Compile the test
        finished_compile = subprocess.run(cmd,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

        os.chdir(current_dir)

        stderr_file = test_workdir + os.sep + testname + "_stderr.log"
        stdout_file = test_workdir + os.sep + testname + "_stdout.log"

        with open(stderr_file, 'w') as stderr_f, open(stdout_file, 'w') as stdout_f:
            stderr_f.write(finished_compile.stderr.decode("utf-8"))
            stdout_f.write(finished_compile.stdout.decode("utf-8"))

        # Return the absolute path to executable
        if finished_compile.returncode == 0:
            return os.path.abspath(test_workdir + testname)
