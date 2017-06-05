 /* Andreas Voskou and Simon Charalampous for Msc Group Project */

/* Integrating N Body Probem using Adams-Bashforth 4th order  multistep method  */



/*  u is velocity
    r is position
    m is mass

*/

package main

import (
    "fmt"
    "math"
    "./vector"
    "runtime"
    "flag"
    "strconv"
)

/***********************  globals  ************************************/

const Gr = 1.0         // global gravity constant
const Pi = 3.14159265  // Pi
var Nb int         // number of bodies

/************************* Body *****************************************/

/* Stuct of a Body */
type Body struct {
    r [3]float64 // position vector
    u [3]float64 // velocity vector
    mass float64    // mass
}

/********** methods of a  body **********/

/* momentum of a body */
func (body Body) Momentum() [3]float64 {
    return vector.Mltp(body.u, body.mass)
}

/* set the parameters of the body (position,velocity,mass)*/
func (body *Body) Set(x, y, z, ux, uy, uz, mass float64) {

    body.r = [3]float64{x, y, z}
    body.u = [3]float64{ux, uy, uz}
    body.mass = mass
}

/* kinetic energy  of a Body*/
func (body Body) K() float64 {

    v := vector.Magnitude(body.u)

    return body.mass * v * v * 0.5

}

/************************************************************************/

/* distance between 2 bodie */
func Distance(body1 Body, body2 Body) float64 {

    return vector.Magnitude(vector.Dif(body1.r, body2.r))
}

/*The Newtwons Gravity Force Function */
func Fgravity(x float64) float64 {

    return -1 / (x * x) // Newton gravity
}

/*Newton Gravity Potential*/
func Vgravity(x float64) float64 {
    return  -1/x
}

/*Force vector between 2 bodies*/
func Force(body1, body2 Body) (force [3]float64) {

    dist := Distance(body1, body2)
    d := vector.Dif(body1.r, body2.r)

    Fm := body1.mass * body2.mass * Fgravity(dist) * Gr

    force[0] = d[0] * Fm /dist
    force[1] = d[1] * Fm /dist
    force[2] = d[2] * Fm /dist

    return force

}

/*Total Force on a Body*/
func TForce(id int, body []Body) (force [3]float64) {

    for i := 0; i < Nb; i++ {

        if i != id {

            force = vector.Sum(force, Force(body[id], body[i]))
        }
    }
    return force
}

// Potential between  2 Bodies
func Potential(body1, body2 Body) (pot float64) {

    dist := Distance(body1, body2)
    pot  = body1.mass * body2.mass *Vgravity(dist) * Gr*0.5

    return pot

}

/*Potential energy of a Body */
func TV(id int, body []Body) (pot float64) {
    pot=0
    for i := 0; i < Nb; i++ {

        if i != id {

            pot = pot+Potential(body[id], body[i])
        }

    }
    return pot
}

/* Total energy of the system */
func  Energy(body []Body) (energy float64){
    energy=0;
    for i:=0;i<Nb;i++{
        energy=energy+body[i].K()+TV(i,body)


    }
    return energy
}

/************ Euler method for ODEs *************************************/

/* Move forward body using euler method (just a Dt  step)*/
func euler_step(body []Body, h float64, id int, cr, cu chan [3]float64) {

    /*return the new position of the body*/
    cr <- vector.Sum(body[id].r, vector.Mltp(body[id].u, h))

    /*return the new velocity of the body*/
    cu <- vector.Sum(body[id].u, vector.Mltp(TForce(id, body), h/body[id].mass))

}

func run_system_euler(body []Body, h float64, steps int) {


    /* creating an  array of  [3]float64 channels to  export
    the position and the velocity from the euler_step goroutine*/

    //var cu, cr []chan [3]float64
    cu:=make([]chan [3]float64,Nb,Nb)
    cr:=make([]chan [3]float64,Nb,Nb)

    for id := 0; id < Nb; id++ {

        cr[id] = make(chan [3]float64)
        cu[id] = make(chan [3]float64)

    }

    /* integrate the system for a total time = h*steps*/
    for j := 0; j < steps; j++ {

        /* run N goroutines to calcute concarently the next position of the bodies*/
        for id := 0; id < Nb; id++ {
            go euler_step(body, h, id, cr[id], cu[id])
        }

        /* passing the new codrinates to the bodies*/
        for id := 0; id < Nb; id++ {
            body[id].r = <-cr[id]
            body[id].u = <-cu[id]
        }
    }

}

/******       Adams-Bashforth 4th order method for ODEs **************************/

/**************Adams-Bashforth 4 constants****************************************/

const ab4 = 55.0 / 24.0

const ab3 = -59.0 / 24.0

const ab2 = 37.0 / 24.0

const ab1 = -3.0 / 8.0

/*one step of the 4th order Adams Bashforth method */
/* https://en.wikipedia.org/wiki/Linear_multistep_method */




func AdamsBashforth4_step(body1, body2, body3, body4 []Body, h float64, id int, cout chan Body) {


    /*return the new position of the body*/

    u4 := vector.Mltp(body4[id].u, ab4)
    u3 := vector.Mltp(body3[id].u, ab3)
    u2 := vector.Mltp(body2[id].u, ab2)
    u1 := vector.Mltp(body1[id].u, ab1)

    u1234 := vector.Sum4(u1, u2, u3, u4)

    /*return the new velocity of the body*/

    f4 := vector.Mltp(TForce(id, body4), ab4)
    f3 := vector.Mltp(TForce(id, body3), ab3)
    f2 := vector.Mltp(TForce(id, body2), ab2)
    f1 := vector.Mltp(TForce(id, body1), ab1)

    f1234 := vector.Sum4(f1, f2, f3, f4)

    //u1234=vector.Sum(b4[id].u, vector.Mltp(f1234, h/b4[id].mass))

    cout <- Body{vector.Sum(body4[id].r, vector.Mltp(u1234, h)),vector.Sum(body4[id].u, vector.Mltp(f1234, h/body4[id].mass)),body4[id].mass}


}

/* using eulers to calculate the 4 first parameters for AdamsBasf4 */
func calculate_initial_4(body0, body1, body2, body3 []Body, h float64) {

    steps := 1000
	h_in := h / float64(steps)
	run_system_euler(body1, h_in, steps)
	copy(body2, body1)
	run_system_euler(body2, h_in, steps)
	copy(body3, body2)
	run_system_euler(body3, h_in, steps)
}


func run_system_AdamsBash4(body0,body1,body2,body3 []Body, h float64, steps int,print int) {

    /* initial_E:=Energy(body0)*/

    printstep:= int(1 / h)

    /* temp and temps will be used to store new positions temporary */
    var temp [128]Body
    var temps[]Body
    temps=temp[0:Nb]


    /* calculating the initial values b0 will be the system at time t=h*0 b1 at y=h*1 ...*/
    calculate_initial_4(body0, body1, body2, body3, h)

    /* creating a slice of Body channels to  export
    the position and the velocity from the step goroutine*/
    cout:=make([]chan Body,Nb,Nb)
    for id := 0; id < Nb; id++ {

        cout[id] = make(chan Body)
    }

    /* integrate the system for a total time = h*steps*/
    for j := 1; j <= steps; j++ {

        /* run N goroutines to calcute concarently the next position of the bodies*/
        for id := 0; id < Nb; id++ {
            go AdamsBashforth4_step(body0, body1, body2, body3, h, id, cout[id])
        }

        /* passing the new codrinates to the bodies*/
        for id := 0; id < Nb; id++ {
            temps[id] = <-cout[id]
        }

        copy(body0,body1)
        copy(body1,body2)
        copy(body2,body3)
        copy(body3,temps)

        if print==1 && j%printstep == 0 {

            /*printing the results to in.txt  (only x,y)*/
            for id:=0 ;id<Nb ; id++ {

                fmt.Printf("%0.1f %0.1f ",body3[id].r[0],body3[id].r[1] )
            }
            fmt.Printf("\n")
        }

    }

    /* printng the energy error */
    /*
    if print ==1{
        final_E:=Energy(body3)
        Energy_Error:=math.Abs((initial_E-final_E)/initial_E)
        fmt.Printf("Energy Error Order= %0.0f\n",math.Log10(Energy_Error))
    }
    */
}


//Initilising Bodies
func InitialConditions(star_mass,planet_mass,space float64)(body1,body2,body3,body4 [128]Body){
    /* Body.Set(x,y,z,ux,uy,uz,mass)*/
    body1[0].Set(0, 0, 0, 0, 0, 0, star_mass)
    for i:=1;i<Nb;i++{
        body1[i].Set(space+space*float64(i),0, 0, 0,math.Sqrt(star_mass/(space+space*float64(i))),0, planet_mass)
    }
    body2=body1
    body3=body1
    body4=body1

    return body1,body2,body3,body4
}



func main() {

    runtime.GOMAXPROCS(1024)//Max number of Cores

    /*read Commandline*/
    flag.Parse()
    p := flag.Arg(0)
    n := flag.Arg(1)
    s := flag.Arg(2)
    print , err := strconv.Atoi(p)
    Nb, err = strconv.Atoi(n)
    steps, err := strconv.Atoi(s)

    if (err != nil) || (Nb < 1) || (steps < 1) {
        fmt.Printf("Usage: nbody <output log 0/1> <number of bodies (1 or more)> <number of steps (1 or more)>")
        return
    }

    if (err != nil) || (Nb == 0) {Nb = 2}
    if (err != nil) || (steps == 0) {steps = 1} // total steps => total time = h*steps

    h := 0.01      // h the size of the step  (Dt)

    /* initial conditions of the system*/
    body1,body2,body3,body4:= InitialConditions(10000,10,100)

    /* slices to arrays of bodies (like pointers)*/
    var bodySlice1,bodySlice2,bodySlice3,bodySlice4 []Body
    bodySlice1=body1[0:Nb]
    bodySlice2=body2[0:Nb]
    bodySlice3=body3[0:Nb]
    bodySlice4=body4[0:Nb]


    /* print to in.txt the number of bodies,total printed steps and initial condintions*/
    if print==1 {
        fmt.Printf("%d %d\r\n",Nb,int(h*float64(steps)))
        for printid:=0 ;printid<Nb ; printid++ {
            fmt.Printf("%0.1f %0.1f %0.1f\n",body1[printid].r[0],body1[printid].r[1],body1[printid].mass )
        }
    }
    /* integrating the system and count time*/
    run_system_AdamsBash4(bodySlice1,bodySlice2,bodySlice3,bodySlice4, h, steps,print)

    return
}
