import csv
import numpy
import os
import matplotlib.pyplot as plt

class Plotter:


    def code_name(inc):
        if inc=='e':
            out= 'Time in seconds'
        if inc=='U':
            out= 'User time in seconds'
        if inc=='S':
            out= 'System time'
        if inc=='P':
            out= 'Percent of CPU usage'
        if inc=='M':
            out=  'Maximum resident set size in KB'
        if inc=='w':
            out=  'Voluntary context switches'
        if inc=='c':
            out=   'Involuntary context switches'
        return out

    def code_int(inc):
        if inc=='e':
            out= 0
        if inc=='U':
            out= 1
        if inc=='S':
            out= 2
        if inc=='P':
            out= 3
        if inc=='M':
            out= 4
        if inc=='w':
            out= 5
        if inc=='c':
            out= 6
        return out
        
    """read the csv file and calculate average times

    arguments: number of runs per freevariable, total number of values
    for the free variable, number of languages and the csvfile
    """
    def readcsv(self, runs, numfree, numlang, csvpath,whatprint):

        printcolumn=Plotter.code_int(whatprint)
        
        csvfile = open(csvpath)     # open the csv file
        Plotter.numlang = numlang
        
        times = []                  #temporary stores times for each run to calculate the aversge
        Plotter.lang = []           #stores the names of the languages

        reader = csv.reader(csvfile)
        headline = next(reader)     #read the headline of the file

        #labels for the plot
        Plotter.y_label = Plotter.code_name(whatprint)

        #in case of numfree>1 x label is the free variable else 'Language'
        if numfree > 1:
            Plotter.x_label = headline[1]
        else:
            Plotter.x_label = 'Language'

        if numfree <= 1:

            Plotter.barResults = [] #average  time per language
            for k in range(numlang):

                #read the first row of a language to identify the language
                row = next(reader)
                times = []
                Plotter.lang.append(row[0])
                for j in range(runs):
                    times.append(float(row[j+1+numfree+printcolumn]))
                    avg = numpy.mean(times)

                Plotter.barResults.append(avg)



        else:

            #average  time per freevarible
            Plotter.results = [ [] for y in range(numlang)]
            #free varible values
            Plotter.free = [ [] for y in range(numlang)]
            for k in range(numlang):

                #read the first row of a language to identify the language
                row = next(reader)
                times = []
                Plotter.lang.append(row[0])
                for j in range(runs):
                    times.append(float(row[j+2+printcolumn*runs]))
                    avg = numpy.mean(times)


                Plotter.results[k].append(avg)
                Plotter.free[k].append(int(row[1]))

                #read the rest row
                for i in range(numfree-1):
                    row = next(reader)
                    times = []
                    for j in range(runs):
                        times.append(float(row[j+2+printcolumn*runs]))
                        avg = numpy.mean(times)
                    Plotter.results[k].append(avg)
                    Plotter.free[k].append(int(row[1]))



    #draw the results as a Barchart
    def bardraw(display, filename):


        y_axis = Plotter.barResults                # the average times per lang
        x_axis = numpy.arange(Plotter.numlang)     # the x locations for the languages
        width = 1.0/Plotter.numlang                # the width of the bars

        p1 = plt.bar(x_axis, y_axis, width, color='red')

        #set the labels
        plt.ylabel(Plotter.y_label)
        plt.xlabel(Plotter.x_label)
        plt.title(Plotter.y_label + "  -  " + Plotter.x_label)
        plt.xticks(x_axis, Plotter.lang)

        #show or safe
        if not display:
            plt.savefig(filename, dpi=None, facecolor='w', edgecolor='w',
                        orientation='potrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
        else:
            plt.show()



    #draw the results as a grapg
    def draw(display, filename):
        markers=['o','<','s','p','P','h','H','+','1','2','3','4','5','6','7']  
        for i in range(Plotter.numlang):
            plt.plot(Plotter.free[i], Plotter.results[i], label=Plotter.lang[i],marker=markers[i])

        plt.xlabel(Plotter.x_label)
        plt.ylabel(Plotter.y_label)
        plt.legend()
        plt.title(Plotter.y_label + "  -  " + Plotter.x_label)
        
        if not display:
            plt.savefig(filename, dpi=None, facecolor='w', edgecolor='w',
                        orientation='potrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)
        else:
            plt.show()




    #front - reads and draw
    def plot(self, runs, numfree, numlang, csvpath, display, filename,whatprint):
        filename=filename+"_"+whatprint+".pdf"
        Plotter.readcsv(self, runs, numfree, numlang, csvpath,whatprint)
        if numfree <= 1:
            Plotter.bardraw(display, filename)
        else:
            Plotter.draw(display, filename)

        plt.clf() #clears the buffer

def main():
    #tests
    pltr = Plotter()
    pltr2 = Plotter()

    csvpath = 'work/nbody_Case_with_changing_Number_of_Bodies.csv'
    filename = 'work/bla'
    
    pltr.plot(2, 20, 3, csvpath, 0, filename,'c')
    pltr.plot(2, 20, 3, csvpath, 0, filename,'e')
    


if __name__ == "__main__":
    main()
