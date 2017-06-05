import csv
import os
import sys
import logging
import plotter

DATA_DIR = 'work'

LANG_COL = 'Language'
#Possible measurements which results dict could contain
RESULTS = [
        'Time in seconds',
        'User time in seconds',
        'System time in seconds',
        'Percent of CPU usage',
        'Maximum resident set size in KB',
        'Voluntary context switches',
        'Involuntary context switches']

#Sanity checks can be removed if we are confident CE will pass correct input

class DataInterpreter:

    #==========================================================================
    #Optionally takes path to output csv files and plots
    def __init__(self, results_dict, output_dir=DATA_DIR):
        logging.debug("==========DATA INTERPRETER==========")
        self.results_dict = results_dict
        self.output_dir = output_dir
        
        #Storage for parsed data, used by generate_csv() and plot_graph()
        self.parsed_data= dict()
        #Nested dictionary structure:
        #<Benchmark_name>
        #   <Case_name>
        #       [csv_dict]  Dictionary of results for generating CSV file
        #       [col_keys]  Ordered list of columns in CSV
        #       [reps]      Repetitions of each run with given parameters
        #       [steps]     Number of steps of manipulated variable
        #       [langs]     Number of languages run
        #       [filename]  Filename of CSV file
        #       [path]      Path of CSV file
        
        #Convert raw input data into structured format for generating CSVs
        self.parse_data()

    #==========================================================================
    def plot_graph(self, display=True, fields='e'):
        if display:
            logging.info("Displaying graphs")
        else:
            logging.info("Generating graphs")
        for bench, case_dict in self.parsed_data.items():
            for case, info in case_dict.items():
                if info['path'] != None:
                    pl = plotter.Plotter()
                    logging.debug("PLOTTING CASE: %s", case)
                    logging.debug("Reps = %s, Steps = %s, Langs = %s, CSV Path = %s, Display = %s, Ouptut Path = %s", info['reps'], info['steps'], info['langs'], info['path'], display, self.output_dir)
                    for c in fields:
                        pl.plot(info['reps'], info['steps'], info['langs'], info['path'], display, self.output_dir + os.sep + info['filename'], c)

    #==========================================================================
    def generate_csv(self):
        logging.info("Writing CSV files to '%s'", self.output_dir)
        for bench, case_dict in self.parsed_data.items():
            for case, info in case_dict.items():
                #Output CSV file, save its path
                info['path'] = self.output_csv(info['csv_dict'], info['col_keys'], info['filename'] + '.csv', self.output_dir)

    #==========================================================================
    def output_csv(self, in_dict, keys, name, path):
        #Handle invalid path
        if not os.path.isdir(path):
            logging.warning("Path '%s' does not exist - creating it", path)
            os.makedirs(path)
            if not os.path.isdir(path):
                logging.warning("Creating path '%s' failed - dumping CSVs in current directory", path)
                self.output_dir = os.getcwd()
                path = self.output_dir
        output = path + os.sep + name
        logging.debug("Writing '%s'", output)

        #Write CSV file
        try:
            with open(output, 'w', newline='') as outfile:
                w = csv.writer(outfile)
                w.writerow(keys)
                w.writerows(zip(*[in_dict[key] for key in keys]))
        except EnvironmentError:
            logging.error("Could not create file '%s'", output)
            return None
        return output

    #==========================================================================
    def parse_data(self):
        logging.info("Parsing results")
        #We are passed a nested dictionary of the results [documenting its structure ain't my job]
        #Parse data for each benchmark
        for bench, lang_dict in self.results_dict.items():
            logging.debug("Found benchmark '%s'", bench)
            #Add this bench to data dictionary
            self.parsed_data[bench] = dict()

            #Get list of languages used (keep ordering consistent)
            languages = sorted(lang_dict.keys())
            #Get list of cases (pick a language subdictionary at random, look inside)
            cases = sorted((next(iter(lang_dict.values()))).keys())
            logging.debug("Languages = %s", languages)
            logging.debug("Cases = %s", cases)

            #Sanity check: Make sure number of cases is consistent in all languages
            numcases = len(cases)
            for lang, case_dict in lang_dict.items():
                if numcases != len(case_dict):
                    logging.critical("Number of test cases for '%s' inconsistent across languages", bench)
                    raise ValueError("Inconsistent number of test cases across languages")

            #Generate separate CSV info for each case
            for case in cases:
                logging.debug("%s:", case)
                #Add to data dictionary
                self.parsed_data[bench][case] = dict()

                #Get list of variables we have information for:
                #Take a random language that ran this benchmark, then take this case from that dict
                data_template = next(iter(lang_dict.values()))[case]
                #Get list of variables (convert to dict for ease of handling)
                var_dict = dict.fromkeys(data_template.keys())
                logging.debug("Dictionary entries = %s", sorted(var_dict.keys()))
                
                #Create a list of the results passed by the 'time' utility
                #Currently should always be all of them, but kept this way just in case
                results = list()
                for field in RESULTS:
                    if field in var_dict:
                        results.append(field) 
                        del var_dict[field]

                #Sanity check: At least one result exists
                if len(results) < 1:
                    logging.critical("No results keys found in dictionary for: %s %s", bench, case)
                    raise ValueError("Dictionary key not found")
                
                #Find the variable which changes in this case
                num_manip_vars = 0
                for var in var_dict:
                    if isinstance(data_template[var], list):
                        manipulated_variable = var
                        num_manip_vars = num_manip_vars + 1
                #Sanity check: One and only one variable changes
                if num_manip_vars > 1:
                    logging.critical("Multiple variables have multiple values for: %s %s. We currently don't handle this situtation - sorry!", bench, case)
                    raise ValueError("Multiple manipulated variables")

                if num_manip_vars == 1:
                    logging.debug("Manipulated variable = %s", manipulated_variable)
                    #Extract values for manipulated variable
                    manip_values = data_template[manipulated_variable]
                    #Remove from var_dict
                    del var_dict[manipulated_variable]
                    logging.debug("Manipulated variable values = %s", manip_values)
                else:
                    logging.debug("No manipulated variable")


                #var_dict now contains a list of the names of the constant variables
                #Add their values
                for var in var_dict:
                    var_dict[var] = data_template[var]
                logging.debug("Static variables = %s", var_dict)

                #Get number of repetitions per set of paramters in this test case
                    #Results fields are always a list containing one or more lists
                reps = len(data_template[results[0]][0])
                logging.debug("Repetitions = %s", reps)

                #Generate dictionary for the CSV file:
                csv_dict = dict()

                #For each language
                logging.debug("Creating csv_dict")
                for lang in languages:
                    #For each value of manipulated variable (number of steps in config.ini)
                    if num_manip_vars == 1:
                        index = 0 #Step count
                        for val in manip_values:
                            #Add to language column
                            csv_dict.setdefault(LANG_COL,[]).append(lang)
                            #Add to manipulated variable column
                            csv_dict.setdefault(manipulated_variable,[]).append(val)
                            
                            #For each test repetition
                            for i in range(0, reps):
                                #Add to results columns
                                for result in results:
                                    colname = result + ' ' + str(+i+1)
                                    csv_dict.setdefault(colname,[]).append(lang_dict[lang][case][result][index][i])
                            index = index + 1
                    #No manipulated variables - special case
                    else:
                        csv_dict.setdefault(LANG_COL,[]).append(lang)
                        for result in results:
                            for value in lang_dict[lang][case][result]:
                                if reps == 1:
                                    colname = result + ' 1'
                                    csv_dict.setdefault(colname,[]).append(value[0])
                                else:
                                    for i in range(0, reps):
                                        colname = result + ' ' + str(i+1)
                                        csv_dict.setdefault(colname,[]).append(value[i])

                #Get number of manipulated variable steps
                if num_manip_vars == 1:
                    manip_steps = len(manip_values)
                else:
                    manip_steps = 0

                #Maintain columns in CSV in consistent order
                    #Language, Variable, Results
                if num_manip_vars == 1:
                    col_keys = [LANG_COL, manipulated_variable]
                else:
                    col_keys = [LANG_COL]
                for result in results:
                    for i in range(0, reps):
                        col_keys.append(result + ' ' + str(i+1))
                
                #Generate CSV file name
                filename = bench + '_' + case.replace(' ', '_')
                logging.debug("csv filename = %s", filename)

                #Add parsed information to parsed_data dictionary
                self.parsed_data[bench][case]["filename"] = filename
                self.parsed_data[bench][case]["csv_dict"] = csv_dict
                self.parsed_data[bench][case]["col_keys"] = col_keys
                self.parsed_data[bench][case]["reps"] = reps
                self.parsed_data[bench][case]["steps"] = manip_steps
                self.parsed_data[bench][case]["langs"] = len(languages)

        logging.debug("Parsing complete\n")
