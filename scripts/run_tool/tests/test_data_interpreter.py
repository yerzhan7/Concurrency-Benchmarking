import unittest
import data_interpreter
import os
import sys
import pprint
import logging
import tempfile

OUT_PATH = "unittest_DI_dumps"
TIME_NAME = "Time in seconds"
plot = False
cleanup = True

def dump_dict(dct, path):
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
        path = path + os.sep + 'dict'
        with open(path, 'w') as f:
            f.write(repr(dct))
            f.write('\n')
    except:
        print("ERROR: Could not write dictionary")
        sys.exit(1)

class TestDI(unittest.TestCase):

    def setUp(self):
        #Output dir for CSVs
        if cleanup:
            self.path = tempfile.TemporaryDirectory()
        else:
            if not os.path.isdir(OUT_PATH):
                os.makedirs(OUT_PATH)
            self.path = OUT_PATH

    def tearDown(self):
        if cleanup:
            self.path.cleanup()

    def genRes(self, numbench, numlangs, numcase, numvars, numstep, nummanip, numreps, timename=TIME_NAME):
        if nummanip > numvars:
            print("Error: Num manipulated vars cannot be greater than num vars")
            sys.exit(1)

        d = dict()
        #Benchmarks
        for a in range(0, numbench):
            bench = 'bench' + str(a)
            d[bench] = dict()
            #Languages
            for b in range(0, numlangs):
                lang = 'lang' + str(b)
                d[bench][lang] = dict()
                #Cases
                for c in range(0, numcase):
                    case = 'case' + str(c)
                    d[bench][lang][case] = dict()
                    #Create entries for variables
                    for x in range(0, numvars):
                        var = 'var' + str(x)
                        #Values for manipulated var
                        if x < nummanip:
                            d[bench][lang][case][var] = list()
                            for e in range(0, numstep):
                                d[bench][lang][case][var].append(e*10)
                        else:
                            d[bench][lang][case][var] = -1
                    #Create entries for time
                    d[bench][lang][case][timename] = list()
                    for f in range(0, numstep):
                        res = list()
                        for g in range(0, numreps):
                            res.append(g)
                        d[bench][lang][case][timename].append(res)
        return d

    def runDI(self, results, path):
        if cleanup:
            path = self.path.name + os.sep + path
        else:
            path = self.path + os.sep + path

        di = data_interpreter.DataInterpreter(results, path)
        di.generate_csv()
        dump_dict(results, path)
        if plot:
            di.plot_graph(False, path)

    #===================TESTS===================================================

    def test_empty_dict(self):
        res = dict()
        self.runDI(res, 'empty_dict')

    def test_1_of_everything(self):
        res = self.genRes(1, 1, 1, 1, 1, 1, 1)
        self.runDI(res, '1_of_everything')

    def test_multiple_reps(self):
        res = self.genRes(2, 3, 2, 4, 5, 1, 5)
        self.runDI(res, 'multiple_reps')

    def test_multiple_manip_vars(self):
        #Should raise error
        res = self.genRes(2, 2, 2, 3, 2, 2, 3)
        print("\nCritical error is supposed to occur in this test:")
        with self.assertRaises(ValueError):
            self.runDI(res, 'multi_manip_vars')

    def test_different_time_name(self):
        #Should raise excpetion
        res = self.genRes(1, 1, 1, 1, 1, 1, 1, 'time')
        print("\nCritical error is supposed to occur in this test:")
        with self.assertRaises(ValueError):
            self.runDI(res, 'diff_time_name')

    def test_no_manip_vars(self):
        res = self.genRes(2, 2, 2, 4, 1, 0, 2)
        self.runDI(res, 'no_manip')

    def test_no_manip_vars_1_rep(self):
        res = self.genRes(2, 2, 2, 4, 1, 0, 1)
        self.runDI(res, 'no_manip_1_rep')

    def test_1_step_x_rep(self):
        res = self.genRes(1, 1, 1, 3, 1, 1, 4)
        self.runDI(res, '1_step_x_rep')

    def test_x_step_1_rep(self):
        res = self.genRes(1, 1, 1, 3, 5, 1, 1)
        self.runDI(res, 'x_step_1_rep')

#genRes(numbench, numlangs, numcase, numvars, numstep, nummanip, numreps, timename)
        
if __name__ == '__main__':
    #Full debug info
    debug = False
    #Call plotter too
    plot = True 
    #Tidy files afterwards
    cleanup = True#

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    unittest.main()
