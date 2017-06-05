#!/usr/bin/env python3
import sys
import os
import argparse
import logging
import shutil
import datetime

import crawler
import compilation_executor
import test_executor
import data_interpreter

DEFAULT_WORKDIR = "work"
DESC = ("Script used to compile and run benchmarks for "
        "different programming languages.")
BAK_TIME_FMT = "%y%m%d%H%M%S"
RUNS_PER_PT = 2
DEFAULT_FMT = "eM"


def valid_dir(arg):
    if not os.path.isdir(arg):
        msg = arg + " is not a valid directory"
        raise argparse.ArgumentTypeError(msg)

    return arg

def valid_fmt(arg):
    for char in arg:
        if char not in "eUSPMwc":
            msg = char + " is not a valid format parameter"
            raise argparse.ArgumentTypeError(msg)

    return arg


def dump_dict_to_file(dct, filename):
    try:
        base = os.sep.join(filename.split(os.sep)[:-1])

        if base and (not os.path.exists(base)):
            os.makedirs(base)

        with open(filename, 'w') as dict_file:
            dict_file.write(repr(dct))

    except:
        logging.critical("Could not write to " + filename)
        sys.exit(1)


def read_dict_from_file(filename):
    try:
        with open(filename, 'r') as dict_file:
            read_data = dict_file.read()

        return eval(read_data)

    except FileNotFoundError:
        logging.critical("Intermediate data file " + filename + " does not exist")
        sys.exit(1)

    except:
        logging.critical("Unrecognised intermediate data")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=DESC)

    # Accepted arguments:
    verbosity_args = parser.add_mutually_exclusive_group()
    verbosity_args.add_argument("-v", "--verbose",
                                action="store_true",
                                help="print all messages")
    verbosity_args.add_argument("-q", "--quiet",
                                action="store_true",
                                help="do not print information messages")

    cfg_args = parser.add_mutually_exclusive_group()
    cfg_args.add_argument("-c", "--compile-only",
                          action="store_true",
                          help="only compile the benchmarks")
    cfg_args.add_argument("-r", "--run-only",
                          action="store_true",
                          help="only run pre-compiled benchmarks")
    cfg_args.add_argument("-p", "--process-only",
                          action="store_true",
                          help="only process pre-generated results")

    parser.add_argument("bench_dir",
                        type=valid_dir,
                        help="directory where benchmarks are located")

    parser.add_argument("-w", "--workdir",
                        default=DEFAULT_WORKDIR,
                        help="output directory")

    parser.add_argument("-t", "--benchmarks",
                        nargs='+',
                        metavar="BENCH",
                        help="list of benchmarks to be run",
                        default=[])

    parser.add_argument("-o", "--overwrite-workdir",
                        action="store_true",
                        help="overwrite workdir if it already exists")

    parser.add_argument("-e", "--repetition-count",
                        type=int,
                        default=RUNS_PER_PT,
                        help="number of times each benchmark iteration is run")

    parser.add_argument("-g", "--gui",
                        action="store_true",
                        help="show plots in a GUI")

    parser.add_argument("-f", "--plot-format",
                        type=valid_fmt,
                        default=DEFAULT_FMT,
                        help="select which dependent variables should be plotted")

    args = parser.parse_args()

    # Verbosity setup
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("Test root: " + args.bench_dir)
    logging.info("Working directory: " + args.workdir)

    # Used in most of the branches, so defined here
    itm_data_dir = args.workdir + os.sep
    itm_data_dir += "intermediate_data" + os.sep

    te_path = itm_data_dir + "te_data"
    ce_path = itm_data_dir + "ce_data"

    # Deal with working directory
    if not (args.process_only or args.run_only):
        if os.path.isdir(args.workdir):
            if args.overwrite_workdir:
                logging.warning("Overwriting working directory")
                shutil.rmtree(args.workdir)
                try:
                    os.makedirs(args.workdir)
                except:
                    logging.critical("Could not create working directory")
                    sys.exit(1)

            else: # not overwriting workdir
                backup_name = args.workdir
                backup_name += "_bak_"
                backup_name += datetime.datetime.now().strftime(BAK_TIME_FMT)

                logging.warning("Moving working directory to: " + backup_name)
                os.rename(args.workdir, backup_name)
                try:
                    os.makedirs(args.workdir)
                except:
                    logging.critical("Could not create working directory")
                    sys.exit(1)

        else: # workdir does not exist
            try:
                os.makedirs(args.workdir)
            except:
                logging.critical("Could not create working directory")
                sys.exit(1)

            logging.debug("Created working directory")

    else: # we're either running only or processing only
        if args.run_only:
            ce_dict = read_dict_from_file(ce_path)
            test_exec = test_executor.TestExecutor(ce_dict, args.repetition_count)
            results = test_exec.run_tests(args.benchmarks)
            dump_dict_to_file(results, te_path)

        elif args.process_only:
            te_dict = read_dict_from_file(te_path)
            data_interp = data_interpreter.DataInterpreter(te_dict)
            data_interp.generate_csv()
            data_interp.plot_graph(args.gui, args.plot_format)

        logging.info("Finished")
        sys.exit(0)

    # At this point we either compile-only or do the whole shebang
    crawl = crawler.Crawler(args.bench_dir)

    compilation_exec = compilation_executor.CompilationExecutor(crawl.get_dict())
    ce_dict = compilation_exec.compile_tests(args.benchmarks)

    dump_dict_to_file(ce_dict, ce_path)

    if args.compile_only:
        logging.info("Finished")
        sys.exit(0)

    test_exec = test_executor.TestExecutor(ce_dict, args.repetition_count)
    te_dict = test_exec.run_tests(args.benchmarks)

    dump_dict_to_file(te_dict, te_path)

    data_interp = data_interpreter.DataInterpreter(te_dict)
    data_interp.generate_csv()
    data_interp.plot_graph(args.gui, args.plot_format)

    logging.info("Finished")
    sys.exit(0)


if __name__ == "__main__":
    main()
