#!/usr/bin/env python2

from __future__ import print_function
from graphics import *
from math import cos, sin, log10
import time

def main():
    win = GraphWin(width=800, height=800) # create a window
    # set the coordinates of the window; bottom left is (-400, -400) and top right is (400, 400)
    win.setCoords(-400, -400, 400, 400)

    time_step = 0.025
    body = [Circle(Point(-100, 100), 10)]

    with open('nbody.film', 'r') as f:

        sn, ssteps = f.readline().split(' ') # read first line
        n = int(sn) # number of bodies
        steps = int(ssteps) # total steps 
        print('Bodies:', n)
        print('Total Time: ', steps * time_step, 's')

        for j in range(n):
            line = f.readline()

            #reading inital conditions
            sx, sy, sm = line.split(' ')
            initial_x = float(sx)
            initial_y = float(sy)
            mass = float(sm)

            print('Body', j, 'mass:', mass)

            radius = log10(mass)*5 + 5 #radius as a function of mass

            #creating a body
            body.insert(j, Circle(Point(initial_x, initial_y), radius))
            body[j].draw(win)
            body[j].setFill('blue')

        #reading new positions
        for line in f:
            time.sleep(time_step)
            j = i = 0

            for s in line.split(' '):
                if s != '\n':
                    if (i % 2) == 0:
                        new_x = float(s) - body[j].getCenter().getX()

                    else:
                        new_y = float(s) - body[j].getCenter().getY()

                        # move the bodies
                        body[j].move(new_x,new_y)
                        j += 1

                    i += 1

if __name__ == "__main__":
    print("N-body simulation")
    main()
