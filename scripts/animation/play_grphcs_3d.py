print("Play_nbody")
from graphics import *
from math import cos,sin,log10
import time
import sys



filename=input("Input file: ")
filename=filename+".film"

time_step=0.00125

body=[Circle(Point(-100,100),10)]
rad=[3.0]
e=2.71828
space=Circle(Point(0,0),300)

#opens a graphics window
def openWindow(x,y,z):
    win = GraphWin(width = x, height = y) # create a window
    win.setCoords(-x/z,-y/z,x/z,y/z) # set the coordinates of the window; bottom left is (0, 0) and top right is (10, 10)
    win.setBackground('black')
    return win

# radius as a function of z
def radz(z):

    if  z<1000:
        return 1-0.0005*z
    return 0

#a steo of movement     
def move3d(x,y,z,r):
      
    planet=Circle(Point(x,y+0.3*z),r*radz(z))
    planet.setFill('blue')
    if r>20:
        planet.setFill('yellow')
    
    return planet

#shift 2 variables
def shift(a,b):
    
    return b,a

#sorting with ...bubble sort :( 
def sort(body,zz,n):
    for ja in range(0,n):
    
        for ia in range(ja,n):
            if zz[ia]>zz[ja]:
                body[ja],body[ia]=shift(body[ja],body[ia])
                zz[ja],zz[ia]=shift(zz[ja],zz[ia])
   
    return body,zz
    

with open(filename, 'r') as f:       
  sn ,ssteps = f.readline().split(' ') # read first line
  n=int(sn) # number of bodies
  steps=int(ssteps) # total steps
  zz=[1,2,3,4,5,5,7,8,9,10,11,12]
  new=[1,2,3,4,5,5,7,8,9,10,11,12]
  print('Bodies:' , n)
  print ('Total Time: ' ,steps*time_step ,'s')
  
  for j in range(0,n):

        #reading inital conditions
        line=f.readline()
        sx ,sy,sm = line.split(' ')
        initial_x= float(sx)
        initial_y = float(sy)
        mass=float(sm)
        print ('Body',j, 'mass:', mass)
        radius= (mass ** (1. / 3))*2+10 #radius as a function of mass

        #creating a body
        body.insert(j,Circle(Point(initial_x,initial_y),radius))
        rad.insert(j,radius)
    

        
  time.sleep(1)
  print("ready")
  
  win=openWindow(1600,900,1)
  body[j].setFill('blue')
  body[j].draw(win)
        
      #reading new positions

  for line in f:      
        time.sleep(time_step)
        i=0
        j=0
            
        for s in line.split(' '):            
            if s!='\n':     

                if  i%2==0 :
                   move_x= float(s)   

                if  i%2==1 :  
                   move_y=-float(s)
                   zz[j]=move_y
                   new[j]=move3d(move_x,0,move_y,rad[j])
                   j=j+1

                i=i+1

        new,zz=sort(new,zz,n)
        
        
        #update frame
        for id in range(0,n): 
            new[id].draw(win)
            body[id].undraw()
            
    
        for id in range(0,n):
            body[id]=new[id]
        
   
win.close()

