import os
import logging
import subprocess
import shutil

LANG_NAME = "pony"
CC = "ponyc"
MISSING_COMPILER = "Compiler for pony has not been found."

class LangUnit:

    def __init__(self, workdir):
        # Check if compiler exists in the system
        if shutil.which(CC) is None:
            raise FileNotFoundError(MISSING_COMPILER)

        # Set the base working directory for language
        self.langdir = workdir + os.sep + LANG_NAME

    def compile(self, testname, testpath):
        test_workdir = self.langdir + os.sep +\
                       testname + os.sep

        # Create the working directory for the test
        try:
            os.makedirs(test_workdir)

        except FileExistsError:
            logging.warning(LANG_NAME + " compilation: " + test_workdir + " already exists")

        testpath += os.sep + "src"
        cmd = [CC, testpath, "-o", test_workdir]

        # Compile the test
        finished_compile = subprocess.run(cmd,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)

        stderr_file = test_workdir + os.sep + testname + "_stderr.log"
        stdout_file = test_workdir + os.sep + testname + "_stdout.log"

        with open(stderr_file, 'w') as stderr_f, open(stdout_file, 'w') as stdout_f:
            stderr_f.write(finished_compile.stderr.decode("utf-8"))
            stdout_f.write(finished_compile.stdout.decode("utf-8"))

        # Return the absolute path to executable
        if finished_compile.returncode == 0:
            # Pony-specific - rename the executable to something sensible
            os.rename(test_workdir + "src", test_workdir + testname)

            return os.path.abspath(test_workdir + testname)

        return None
