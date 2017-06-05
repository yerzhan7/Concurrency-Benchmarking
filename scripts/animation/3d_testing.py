print("Play_nbody")
from graphics import *
from math import cos,sin,log10,sqrt,exp
import time
Pi=3.14
P=1/6.28
    

time_step=0.025 
win = GraphWin(width = 600, height = 600) # create a window
win.setCoords(-400,-400,400,400) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
win.setBackground('black')


body=[Circle(Point(-100,100),10)]
planet=Circle(Point(0,0),10)
planet2=Circle(Point(0,0),10)
planet3=Circle(Point(0,0),10)
axe_x=Line(Point(-300,-300),Point(300,-300))
axe_y=Line(Point(-300,-300),Point(-300,300))
axe_z=Line(Point(-300,-300),Point(50,100))
#axe_x.draw(win)
#axe_y.draw(win)
#axe_z.draw(win)
planet.setFill('blue')
planet.draw(win)
planet2.setFill('red')
planet3.draw(win)
planet3.setFill('green')
planet2.draw(win)
star=Circle(Point(50,-10),40)
star.setFill('yellow')
star.draw(win)

def move3d(planet,x,y,z):
    new=Circle(Point(x+0.7*z,y+0.7*z),10-4*0.01*(z))
    new.setFill('green')
    planet=new
    planet.draw(win)
    return planet
   
    


for i in range(1,60000):
 #   time.sleep(0.033)
    planet3.undraw()
    planet3=move3d(planet,50+100*sin(i*0.42*P),10,50*cos(i*0.42*P))
    time.sleep(0.033)
    new2=Circle(Point(50+200*sin(i*0.42*P),100*cos(i*0.42*P)),10-6*cos(0.42*i*P))
    new=Circle(Point(50+100*sin(i*0.42*P),50*cos(i*0.42*P)),10-4*cos(0.42*i*P))
    new.setFill('blue')
    new2.setFill('red')
    planet.undraw()
    planet=new
    #planet.draw(win)
    planet2.undraw()
    planet2=new2
    planet2.draw(win)
           



win.getMouse() # pause before closing
