### Synopsis

main.py bench_dir [-h] [-v | -q] [-c | -r | -p] [-w WORKDIR] [-t BENCH [BENCH ...]]
        [-o] [-e REPETITION_COUNT] [-g] [-f PLOT_FORMAT]
        


### Functionality

Steps that run_tool can perform:
1. iterate the directory tree passed as a positional argument assuming a pre-set
structure (see Benchmark directory structure for details) and
automatically create a list of available languages and benchmarks discovered
in the directory tree for use in following step

2. compile discovered benchmarks provided that compilation scripts are available
for languages discovered (for compilation scripts requirements, please see
Compilation Scripts section)

3. execute the compiled benchmarks through Unix time utility to generate the
performance data (for benchmark configuration files, please see Benchmark
Configuration section)

4. process the data and output plots as well as CSV files

The tool has been designed such that steps 1 and 2, step 3 and step 4 can be
run separately. This provides flexibility in how the whole benchmark suite is
run. The reason for steps 1 and 2 to always be executed together is that step
1 is relatively short compared to step 2 and these two actions are closely
coupled.

For clarity, the following names are going to be used:
- Steps 1 and 2 - Compilation Phase (CP)
- Step 2 - Execution Phase (EP)
- Step 3 - Processing Phase (PP)

Data for CP and EP is saved as text files to allow EP and PP respectively to
be run separately. Use-cases for this functionality are described in Usage
section.

### Benchmark directory structure

The assumed directory structure is such that first-level subdirectories at the
tree provided are available languages, and all second-level subdirectories
(every directory inside the language directories) are benchmarks. Visually,
this can be represented as:

benchmark_dir
|-- lang1
|   |-- benchmark1
|   |-- benchmark2
|   .
|   .
|   .
|   |-- benchmarkn-1
|   `-- benchmarkn
|
|-- lang2
|   |-- benchmark1
|   |-- benchmark2
|   .
|   .
|   .
|   |-- benchmarkn-1
|   `-- benchmarkn
.
.
.
|
`-- langn
    |-- benchmark1
    |-- benchmark2
    .
    .
    .
    |-- benchmarkn-1
    `-- benchmarkn

### ignore.txt and rename.txt

Crawler also takes into account information provided in files named as either
ignore.txt or rename.txt.

ignore.txt can be located at either the top-level benchmark_dir as indicated
in the section above, or in any of the language directories. The purpose of
this file is to force Crawler to ignore directories specified in the
ignore.txt - this is useful when only a certain subset of languages is to be
used or if benchmark tree contains folder that should not be interpreted as
languages or benchmarks.

rename.txt can only be located in benchmark directories. It is used to force a
name interpretation that does not necessarily correspond to the benchmark
directory name.  As an example, this is used to rename Scala/Akka benchmarks
to lowercase letters since the convention of Scala is to use CamelCase for
project names whereas both Go and Pony uses all-lower project names.

### Usage

Simplest possible call:

    main.py BENCHMARK_DIR
    main.py /directory/to/benchmarks
    This will crawl through BENCHMARK_DIR, discover all the languages and
    benchmarks and will compile them, then run them using default options (see
    Options section) and will process the data and output the resulting plots.

Re-run pre-compiled benchmarks

    main.py BENCHMARK_DIR -r
    main.py /directory/to/benchmarks -r
    Uses intermediate data from previous invocation (either full run as
    specified above or run with -c flag set) to re-execute the benchmarks.

    This could be useful if a subset of benchmarks should be executed as well
    as modifying the benchmark configuration files (see !!! Benchmark config
    files !!!  section) before re-executing the benchmarks.

Only process the results

    main.py BENCHMARK_DIR -p
    main.py /directory/to/benchmarks -p
    Uses intermediate data from previous invocation (either full run or run
    with -r flag set) to process the data again.

    This is useful if plots of different dependent variables is required (in
    conjunction with -f option)

### Options
-h Print brief help message and exit.

-v, -q Adjust verbosity level of the output produced by the tool. These flags
       are mutually exclusive (-v stands for [v]erbose and -q stands for
       [q]uiet). Verbose option prints all the possible messages, including
       debug information. Quiet option only prints warnings and errors. If
       none of the verbosity options are provided, default verbosity level is
       used which is a middle ground between quiet and verbose

-c, -r, -p Select which phase of the tool to execute. These options are
           mutually exclusive (-c stands for compilation phase, -r stands for
           execution phase and -p stands for processing phase). -r should only
           be selected after either a CP or the full run has been executed
           before and -p should only be selected after either a EP or the full
           run has been executed before. If none of these options is selected,
           all of the phases are executed in turn by default.

-w WORKDIR Specify a working directory for all the output files generated by
           the script. This directory will contain intermediate files for the
           phases, output plots and CSVs as well as benchmark binaries. It is
           worth mentioning, however, that the tool does not enforce the
           storage of benchmark binaries in the WORKDIR - this depends on the
           implementation of the compilation script. If the option is not
           specified in command line, WORKDIR defaults to work in the
           directory where the script has been run from.

-t BENCH [BENCH ...] Specify which benchmarks to compile and/or run. This
                     option is ignored if the tool is run with -p. The list of
                     benchmarks that results after this option is applied is
                     effectively an intersection of benchmarks available
                     (discovered or compiled) and benchmarks provided with
                     this option. This implies that if EP is being executed,
                     no more benchmarks will be compiled even if the
                     benchmarks specified with the -t option are valid. By
                     default, all available benchmarks are used.

-o Overwrite the working directory if it already exists. The default behaviour
   if this flag is unset is to move the existing working directory to
   <directory_name>_<timestamp>_bak.

-e REPETITION_COUNT Specify the number of times each test point is repeated.
   This is useful to get more reliable data by averaging the times at each
   point and statistical error data can also be extracted from CSVs. Default
   value if this option is not specified in command line is 2.

-g Show the plots using matplotlib's tk interface. Requires X-server running
   on the machine where the script is being executed. Default is to output the
   resulting plots as image files.

-f PLOT_FORMAT Specify which dependent variables will be plotted in the
               output. PLOT_FORMAT should be a single string without
               whitespace and should be a subset of following characters:
               "eUSPMwc"
               For meaning of the characters, please refer to time(1) man
               pages - meaning of each character is euquivalent to time(1)
               format string with prepended '%' character. Default value is
               "eM". If -g is specified, this option is ignored and
               PLOT_FORMAT is assumed to be "e".

### Compilation Scripts

Compilation scripts are written in python and are located in the sub-directory
of run_tool script called lang_cfg.

The script has to define LangUnit class as well as LANG_NAME variable at the
module scope, e.g. (minimal language script that does nothing):
    LANG_NAME = "test_lang"

    class LangUnit:
        pass

The LANG_NAME variable has to correspond to the language name found in the
benchmark directory structure (see Benchmark Directory Structure).

For the language script to perform any useful work, constructor that takes in
a working directory as well as compile() method that takes name of the
benchmark (1st argument - a string) and path of the benchmark (2nd argument -
a string) needs to be defined.

compile() method is expected to perform housekeeping tasks and sanity checks,
such as making sure that working directory exists and the tool has permission
to write to it. In addition to that, compile method also saves both stderr and
stdout of the compilers for potential review if compilation does not work as
expected (i.e. the executable was not generated).

The return value of compile() method is either None if there were issues
compiling the benchmark or string containing the command that would need to be
issued in the shell to run the executable.

### Benchmark Configuration

Each benchmark in the benchmark tree has to contain a corresponding
configuration file. The file follows standard INI file structure as follows:

    [Case Name]
    arguments = variable, const_arg1, const_arg2
    argument_names = Iterations, Other Parameter, And Another One

    start = 1
    stop = 10
    step = 2

In the snippet above, Case Name can be any name as long as it provides enough
information for the user of what that particular test case is used for.

The arguments option allows to select which single argument will be varying
throughout the particular test case - or everything could be set as constants,
meaning that only a single datapoint will be generated.

It is worth mentioning that script makes an assumption about arguments to the
benchmarks - the first argument is assumed to be a boolean and it indicates
whether anything should be printed by the benchmark or not. I\O is usually
extremelly slow and since the tool was not designed to benchmark I\O, it
disables the printing in the benchmarks (implicitly passing 0 as the first
argument to the benchmark).

The range definition describes how the variable argument is going to be
changed throughout the test case and arguments follow the definition of Python
range() class.

Alternatively, variable values can be specified as a comma-separated list:
    steps = 1, 2, 3

The range or discrete step definitions of variable should be specified in
mutual exclusion.
