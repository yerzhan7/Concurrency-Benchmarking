from configparser import ConfigParser
import logging
import os
import subprocess
import sys

class TestExecutor:

    # Command that will give elapsed time in seconds of the process
    from sys import platform
    if platform.startswith("win"):
        raise OSError("Windows OS currently not supported by benchmark script")
    elif platform.startswith("darwin"):
    # for OSX users, install gnu-time
        MEASUREMENT_CMD = ['gtime', '-f', '"%e\n%U\n%S\n%P\n%M\n%w\n%c"']
    else:
        MEASUREMENT_CMD = ['/usr/bin/time', '-f', '"%e\n%U\n%S\n%P\n%M\n%w\n%c"']

    def __init__(self, commands_dict, iterations):
        self.results = dict()
        self.arguments_dict = dict()
        self.commands_dict = commands_dict
        self.iterations = iterations # Number of times each test run case will be executed.
        # Results will only contain mean value from all iterations for each test run case.

        script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        script_dir += os.sep

        for testname, lang_cmd in self.commands_dict.items(): # For every test
            self.results[testname] = dict()
            self.arguments_dict[testname] = dict()

            # Opening Test Configuration Files in test_cfg directory which lives
            # in the same directory as the script does.
            test_config_file = script_dir + "test_cfg" + os.sep + testname + ".ini"
            logging.info("Opening test configuration file %s", test_config_file)
            config = ConfigParser()
            if config.read(test_config_file) == []:
                raise IOError("Couldn't open test configuration file " + test_config_file)

            # Creating a dictionary for every language in results
            for lang in lang_cmd:
                self.results[testname][lang] = dict()

            # For every test case in the test configuration file
            for section in config.sections():
                logging.debug("%s.ini - Parsing section [%s]", testname, section)

                self.arguments_dict[testname][section] = []

                # Filling up section dictionary for every language
                for lang in self.results[testname]:
                    self.results[testname][lang][section] = dict()
                    self.results[testname][lang][section]['Time in seconds'] = []
                    self.results[testname][lang][section]['User time in seconds'] = []
                    self.results[testname][lang][section]['System time in seconds'] = []
                    self.results[testname][lang][section]['Percent of CPU usage'] = []
                    self.results[testname][lang][section]['Maximum resident set size in KB'] = []
                    self.results[testname][lang][section]['Voluntary context switches'] = []
                    self.results[testname][lang][section]['Involuntary context switches'] = []

                # Parsing config file
                arguments = config[section]['arguments'].split(",")
                argument_names = config[section]['argument_names'].split(",")
                arguments = [x.strip() for x in arguments]
                argument_names = [x.strip() for x in argument_names]

                # Finding the 'variable' argument and creating argument keys in results
                variable_index = None # Position of 'variable' argument
                for i, arg in enumerate(arguments):
                    if arg == 'variable':
                        # Creating empty list for the variable argument for every language
                        for lang in self.results[testname]:
                            self.results[testname][lang][section][argument_names[i]] = []

                        variable_index = i

                    else:
                        # Assign value for constant arguments into results as a string
                        for lang in self.results[testname]:
                            self.results[testname][lang][section][argument_names[i]] = arguments[i]

                # If there is a variable argument
                if variable_index != None:
                    # Creating a list for variable argument to test e.g. [100, 200, 300, 400, 500]

                    if config.has_option(section, 'step') and config.has_option(section, 'steps'):
                        raise ValueError(testname +".ini [" + section +
                                         "] - there cannot be both 'step' and 'steps' options in the same section for the variable argument!")

                    elif config.has_option(section, 'step'):
                        start = int(config[section]['start'])
                        stop = int(config[section]['stop'])
                        step = int(config[section]['step'])
                        vars = list(range(start, stop + step, step))

                    elif config.has_option(section, 'steps'):
                         vars = config[section]['steps'].split(",")
                         vars = [int(x.strip()) for x in vars]

                    else:
                        raise ValueError(testname + ".ini [" + section +
                                         "] - there is no 'step' or 'steps' options in the section for the variable argument!")

                    # For every variable argument value in the list
                    for var in vars:
                        for lang in self.results[testname]:
                            self.results[testname][lang][section][argument_names[variable_index]].append(var)

                        arguments[variable_index] = str(var)
                        self.arguments_dict[testname][section].append(" ".join(arguments))

                # Else all arguments are fixed - execute just one command
                else:
                    self.arguments_dict[testname][section].append(" ".join(arguments))

    def run_tests(self, tests=[]):
        for testname, lang_cmd in self.commands_dict.items(): # For every test
            if (tests == []) or (testname in tests):
                for lang, command in lang_cmd.items(): # For every language
                    for section, arguments in self.arguments_dict[testname].items():
                        logging.info("Executing '%s' benchmark [%s] in %s", testname, section, lang)
                        for i, arg in enumerate(arguments):
                            # Create execution command ('0' is for not printing to stdout)
                            cmd = TestExecutor.MEASUREMENT_CMD + [command] + ['0'] + [arg]

                            results = self.execute(" ".join(cmd))

                            self.results[testname][lang][section]['Time in seconds'].append(results[0])
                            self.results[testname][lang][section]['User time in seconds'].append(results[1])
                            self.results[testname][lang][section]['System time in seconds'].append(results[2])
                            self.results[testname][lang][section]['Percent of CPU usage'].append(results[3])
                            self.results[testname][lang][section]['Maximum resident set size in KB'].append(results[4])
                            self.results[testname][lang][section]['Voluntary context switches'].append(results[5])
                            self.results[testname][lang][section]['Involuntary context switches'].append(results[6])

            else:
                self.results.pop(testname)

        return self.results

    # Method executes given command 'self.iterations' times
    # Returns a list of results in seconds (in a list for all iterations):
    #   results[0] - Time in seconds
    #   results[1] - User time in seconds
    #   results[2] - System time in seconds
    #   results[3] - Percent of CPU usage
    #   results[4] - Maximum resident set size in KB
    #   results[5] - Voluntary context switches
    #   results[6] - Involuntary context switches
    def execute(self, cmd_string):
        results = [[], [], [], [], [], [], []]

        # For every iteration
        for x in range(0, self.iterations):
            # EXECUTE
            (status, output) = subprocess.getstatusoutput(cmd_string)

            if status == 0:
                # Removing any stdout of benchmarks and saving only results
                output = output.rsplit("\n", 7)

                results[0].append(float(output[-7]))
                results[1].append(float(output[-6]))
                results[2].append(float(output[-5]))
                results[3].append(int(output[-4].rstrip("%").replace("?", "0")))
                results[4].append(int(output[-3]))
                results[5].append(int(output[-2]))
                results[6].append(int(output[-1]))
            else:
                raise OSError("Failed to execute: '" + cmd_string +
                              "'\nExit status: " + str(status) + "\n" + output)

        return results
