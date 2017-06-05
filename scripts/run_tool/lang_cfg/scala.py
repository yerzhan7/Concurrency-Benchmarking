import os
import subprocess
import shutil
import re

LANG_NAME = "ScalaAkka"
BT = 'sbt'
MISSING_BUILDTOOL = """\
SBT build tool for scala has not been found"""

class LangUnit:
    def __init__(self, workdir):
        #check if sbt exists
        if shutil.which(BT) is None:
            raise FileNotFoundError(MISSING_BUILDTOOL)
        self.langdir = workdir + os.sep + LANG_NAME



    def compile(self, testname, testpath):
        test_workdir = self.langdir + os.sep +\
                       testname + os.sep

        # Create the working directory for the test
        try:
            os.makedirs(test_workdir)

        except FileExistsError:
            logging.warning(LANG_NAME + " compilation: " + test_workdir + " already exists")

        buildsbtpath = testpath + os.sep + "build.sbt"
        projectpluginpath = testpath + os.sep + "project" + os.sep + "plugins.sbt"
        exec_filename = ""

        #check if build.sbt exists
        if not os.path.isfile(buildsbtpath):
            raise FileNotFoundError("Missing "+buildsbtpath)

        #check if project/plugins.sbt exists
        if not os.path.isfile(projectpluginpath):
            raise FileNotFoundError("Missing "+projectpluginpath)

        #check if project.sbt includes sbt native packaging plugin
        with open(buildsbtpath) as f:
            for line in f:
                cleanline = "".join(line.split())
                if "enablePlugins(JavaAppPackaging)" in cleanline:
                    plugin = True
                if "name:=" in cleanline:
                    name = True
                    #overwrite exec_filename
                    exec_filename = re.findall(r'"([^"]*)"', cleanline)[0].lower()

            if plugin is not True:
                raise ValueError("sbt native packaging plugin error: "
                                 "enablePlugins(JavaAppPackaging) not detected in "+
                                 buildsbtpath)
            if name is not True:
                raise ValueError("sbt native packaging plugin error: "
                                 "name of test does not correspond with name"
                                 "in build.sbt name:='testname' in "+
                                 buildsbtpath)

        #check if project/plugins.sbt includes sbt native packaging plugin
        if "addSbtPlugin" not in "".join(str(open(projectpluginpath).read().split())):
            raise ValueError("sbt native packaging plugin line"
                             "addSbtPlugin not detected in " +
                             str(projectpluginpath))

        #call the command 'sbt stage' in the testpath (this is a blocking proc)
        f_p = subprocess.run([BT, "clean", "stage"], cwd=testpath, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        stderr_file = test_workdir + os.sep + testname + "_stderr.log"
        stdout_file = test_workdir + os.sep + testname + "_stdout.log"

        with open(stderr_file, 'w') as stderr_f, open(stdout_file, 'w') as stdout_f:
            stderr_f.write(f_p.stderr.decode("utf-8"))
            stdout_f.write(f_p.stdout.decode("utf-8"))

        #create path to executable from sbt native packaging output
        execpath = (testpath + os.sep + "target" + os.sep + "universal" +
                    os.sep + "stage" + os.sep + "bin" + os.sep + exec_filename)

        if not os.path.isfile(execpath):
            raise FileNotFoundError("Missing executable file at "+ execpath +
                                    "; is sbt native packaging plugin using default config?")

        return os.path.abspath(execpath)
