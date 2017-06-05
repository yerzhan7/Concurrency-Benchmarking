/* Test for the vector package */

package main

import (
       "testing"
       "math"
        "os"
        "fmt"
        )



/*********** Helper functions ***********************************************/


/*rounding functions   -stackoverflow.com */
func round(num float64) int {
    return int(num + math.Copysign(0.5, num))
}

func toFixed(num float64, precision int) float64 {
    output := math.Pow(10, float64(precision))
    return float64(round(num * output)) / output
}



/*rounding for a vector*/
func RoundV(in [3]float64,precision int) (out [3]float64){

    out[0]=toFixed(in[0],precision)
    out[1]=toFixed(in[1],precision)
    out[2]=toFixed(in[2],precision)

    return out

}

/**************** Tests *********************************************************/


//Force between 2 Bodies
func TestForce(t * testing.T){

    //Initialisation of bodies
    var body1,body2,body3 Body
    body1.Set(0,0,0,0,0,0,1)
    body2.Set(1,0,0,0,0,0,1)
    body3.Set(0,1,1,234,302,234,10) // random floats for velocity

    //Run force functions
    result1 :=  Force(body1,body2)
    result2 :=  Force(body1,body3)
    result3 :=  Force(body3,body1)

    //expected results
    expected1:=[3]float64{1,0,0}
    expected2:=[3]float64{0,3.535534,3.535534}   // 3.535534=10/(2*sqrt(2))
    expected3:=[3]float64{0,-3.535534,-3.535534}


    if RoundV(result1,5) != RoundV(expected1,5) {
         t.Fatalf("Expected %f, got %f", expected1, result1)
    }

    if RoundV(result2,5) != RoundV(expected2,5) {
         t.Fatalf("Expected %f, got %f", expected2, result2)
    }

    if RoundV(result3,5) != RoundV(expected3,5) {
         t.Fatalf("Expected %f, got %f", expected3, result3)
    }
}


//Total Force on a body
func TestTForce(t * testing.T){
    Nb=3// tests for 3 bodies
    var body_array [3]Body // array of 3 bodies
    var body []Body // slice of the previous array

    //initialising bodies
    body_array[0].Set(0,0,0,0,0,0,1)
    body_array[1].Set(0,-1,-1,0,0,0,10)
    body_array[2].Set(0,1,1,100,100,100,10) // random floats for velocity

    body=body_array[0:3]

    //Run force funtions
    result1 :=  TForce(0,body)
    result2 :=  TForce(1,body)
    result3 :=  TForce(2,body)

    //expected results
    expected1:=[3]float64{0,0,0}
    expected2:=[3]float64{0,12.374369,12.374369}
    expected3:=[3]float64{0,-12.374369,-12.374369}

    if RoundV(result1,5) != RoundV(expected1,5) {
         t.Fatalf("Expected %f, got %f", expected1, result1)
    }

    if RoundV(result2,5) != RoundV(expected2,5) {
         t.Fatalf("Expected %f, got %f", expected2, result2)
    }

    if RoundV(result3,5) != RoundV(expected3,5)  {
         t.Fatalf("Expected %f, got %f", expected3, result3)
    }
}


//Test Euler Step
func TestEulerStep(t *testing.T) {


    Nb=3
    var body_array [3]Body // array of 3 bodies
    var body []Body // slice of the previous array

    body_array[0].Set(0,0,0,0,0,0,1)
    body_array[1].Set(0,-1,-1,0,0,0,10)
    body_array[2].Set(0,1,1,100,100,100,10) // random floats for velocity

    body=body_array[0:3]

    expected_r1:= [3]float64{0,0,0}
    expected_r2:= [3]float64{0,-1,-1}
    expected_r3:= [3]float64{1,2,2}

    expected_u1:= [3]float64{0,0,0}
    expected_u2:= [3]float64{0,0.012374,0.012374}
    expected_u3:= [3]float64{100,99.987626,99.987626}

    cu:=make([]chan [3]float64,Nb,Nb)
    cr:=make([]chan [3]float64,Nb,Nb)

    for id := 0; id < Nb; id++ {
        cr[id] = make(chan [3]float64)
        cu[id] = make(chan [3]float64)
    }

    id1:=0
    go euler_step(body, 0.01, id1, cr[id1], cu[id1])
    result_r1:=<-cr[id1]
    result_u1:=<-cu[id1]

    id2:=1
    go euler_step(body, 0.01, id2, cr[id2], cu[id2])
    result_r2:=<-cr[id2]
    result_u2:=<-cu[id2]

    id3:=2
    go euler_step(body, 0.01, id3, cr[id3], cu[id3])
    result_r3:=<-cr[id3]
    result_u3:=<-cu[id3]


    if RoundV(result_r1,5) != RoundV(expected_r1,5) {
         t.Fatalf("Expected %f, got %f", expected_r1, result_r1)
    }

    if RoundV(result_r2,5) != RoundV(expected_r2,5) {
         t.Fatalf("Expected %f, got %f", expected_r2, result_r2)
    }

    if RoundV(result_r3,5) != RoundV(expected_r3,5)  {
         t.Fatalf("Expected %f, got %f", expected_r3, result_r3)
    }

    if RoundV(result_u1,5) != RoundV(expected_u1,5) {
         t.Fatalf("Expected %f, got %f", expected_u1, result_u1)
    }

    if RoundV(result_u2,5) != RoundV(expected_u2,5) {
         t.Fatalf("Expected %f, got %f", expected_u2, result_u2)
    }

    if RoundV(result_u3,5) != RoundV(expected_u3,5)  {
         t.Fatalf("Expected %f, got %f", expected_u3, result_u3)
    }
}


// testing adams bashforth step
func TestAB4Step(t *testing.T) {


    Nb=3
    var body_array0 [3]Body // array of 3 bodies
    var body0,body1,body2,body3 []Body // slice of the previous array

    //initialising bodies
    body_array0[0].Set(0,0,0,0,0,0,1)
    body_array0[1].Set(0,-1,-1,0,0,0,10)
    body_array0[2].Set(0,1,1,100,100,100,10) // random floats for velocity

    body_array1:=body_array0
    body_array2:=body_array0
    body_array3:=body_array0

    body0=body_array0[0:3]
    body1=body_array1[0:3]
    body2=body_array2[0:3]
    body3=body_array3[0:3]

    //calculate_initial_4(body0,body1,body2,body3,0.01)

    run_system_euler(body1, 0.01, 1)
    run_system_euler(body2, 0.01, 2)
    run_system_euler(body3, 0.01, 3)

    //expected positions
    expected_r1:= [3]float64{7.528551069814374E-5, -9.766972872791184E-4, -9.766972872791184E-4}
    expected_r2:= [3]float64{3.128473074515985E-5, -0.9993992306380816, -0.9993992306380816}


    //expected velocities
    expected_u1:= [3]float64{0.009203512690456854, -0.10132972210407891, -0.10132972210407891}
    expected_u2:= [3]float64{0.0032361046404008483, 0.02870963183016327, 0.02870963183016327}


    //creating channels  positions and velocities
    cout:=make([]chan Body,Nb,Nb)

    for id := 0; id < Nb; id++ {
        cout[id] = make(chan Body)
    }


    // run the functions
    id1:=0
    go AdamsBashforth4_step(body0,body1,body2,body3, 0.01, id1,cout[id1])
    result1:=<-cout[id1]
    result_r1:=result1.r
    result_u1:=result1.u

    id2:=1
    go AdamsBashforth4_step(body0,body1,body2,body3, 0.01, id2,cout[id2])
    result2:=<-cout[id2]
    result_r2:=result2.r
    result_u2:=result2.u



    //test results
    if RoundV(result_r1,5) != RoundV(expected_r1,5) {
         t.Fatalf("Expected %f, got %f", expected_r1, result_r1)
    }

    if RoundV(result_r2,5) != RoundV(expected_r2,5) {
         t.Fatalf("Expected %f, got %f", expected_r2, result_r2)
    }


    if RoundV(result_u1,5) != RoundV(expected_u1,5) {
         t.Fatalf("Expected %f, got %f", expected_u1, result_u1)
    }

    if RoundV(result_u2,5) != RoundV(expected_u2,5) {
         t.Fatalf("Expected %f, got %f", expected_u2, result_u2)
    }


}
//calculate_initial_4(body0,body1,body2,body3,0.01)
func TestCalculate_initial_4(t *testing.T) {


    Nb=3
    var body_array0 [3]Body // array of 3 bodies
    var body0,body1,body2,body3 []Body // slice of the previous array

    //initialising bodies
    body_array0[0].Set(0,0,0,0,0,0,1)
    body_array0[1].Set(0,-1,-1,0,0,0,10)
    body_array0[2].Set(0,1,1,100,100,100,10) // random floats for velocity

    body_array1:=body_array0
    body_array2:=body_array0
    body_array3:=body_array0

    body0=body_array0[0:3]
    body1=body_array1[0:3]
    body2=body_array2[0:3]
    body3=body_array3[0:3]

    calculate_initial_4(body0,body1,body2,body3,0.01)


    //expected positions
    expected_r1:= [3]float64{0,0,0}
    expected_r2:= [3]float64{0.000004, -0.999949, -0.999949}


    //expected velocities
    expected_u1:= [3]float64{0.002022, 0.015411,0.015411}
    expected_u2:= [3]float64{99.996367, 99.987898, 99.987898}


    result_r1:=body0[0].r
    result_r2:=body1[1].r
    result_u1:=body2[1].u
    result_u2:=body3[2].u

    //test results
    if RoundV(result_r1,5) != RoundV(expected_r1,5) {
         t.Fatalf("Expected %f, got %f", expected_r1, result_r1)
    }

    if RoundV(result_r2,5) != RoundV(expected_r2,5) {
         t.Fatalf("Expected %f, got %f", expected_r2, result_r2)
    }


    if RoundV(result_u1,5) != RoundV(expected_u1,5) {
         t.Fatalf("Expected %f, got %f", expected_u1, result_u1)
    }

    if RoundV(result_u2,5) != RoundV(expected_u2,5) {
         t.Fatalf("Expected %f, got %f", expected_u2, result_u2)
    }


}

//calculate_initial_4(body0,body1,body2,body3,0.01)
func TestEnergy(t *testing.T) {


    Nb=3
    var body_array0 [3]Body // array of 3 bodies
    var body0,body1,body2,body3 []Body // slice of the previous array

    //initialising bodies
    body_array0[0].Set(0,0,0,0,0,1,10)
    body_array0[1].Set(100,0,0,0,1,0,10)
    body_array0[2].Set(200,0,0,1,0,0,10) // random floats for velocity

    body_array1:=body_array0
    body_array2:=body_array0
    body_array3:=body_array0

    body0=body_array0[0:3]
    body1=body_array1[0:3]
    body2=body_array2[0:3]
    body3=body_array3[0:3]

    // open file
    var fo *os.File


    result1:=Energy(body0)
    run_system_AdamsBash4(body0,body1,body2,body3,0.01,1000,fo,0)
    result2:=Energy(body1)

    //expected energy
    expected1:=12.5

    //energy must be the same in 10 or more decimal places
    expected2:=12.5

    //other values for bodies
    body0[0].Set(0,0,0,0,0,2,10)
    body0[1].Set(200,0,0,0,2,0,10)
    body0[2].Set(400,0,0,2,0,0,10)

    body1=body0
    body2=body0
    body3=body0

    result3:=Energy(body2)
    run_system_AdamsBash4(body0,body1,body2,body3,0.01,1000,fo,0)
    result4:=Energy(body3)

    expected3:=58.75
    //energy must be the same in 10 or more decimal places
    expected4:=58.75



    //test results
    if toFixed(result1,5) != toFixed(expected1,5) {
         t.Fatalf("Expected %f, got %f", expected1,result1)
    }

    if toFixed(result2,4) != toFixed(expected2,4) {
         t.Fatalf("Expected %f, got %f", expected2, result2)
    }


    if toFixed(result3,5) != toFixed(expected3,5) {
         t.Fatalf("Expected %f, got %f", expected3, result3)
    }

    if toFixed(result4,5) != toFixed(expected4,5) {
         t.Fatalf("Expected %f, got %f", expected4, result4)
    }
}


func TestInitialConditions(t *testing.T) {

    Nb=3
    body1,body2,body3,body4:= InitialConditions(10000,10,100)

    //Run force funtions
    result1 :=  body1[0].u
    result2 :=  body2[0].r
    result3 :=  body3[1].r
    result4 :=  body4[2].r

    //expected results
    expected1:=[3]float64{0,0,0}
    expected2:=[3]float64{0,0,0}
    expected3:=[3]float64{200,0,0}
    expected4:=[3]float64{300,0,0}

    if RoundV(result1,5) != RoundV(expected1,5) {
         t.Fatalf("Expected %f, got %f", expected1,result1)
    }

    if RoundV(result2,4) != RoundV(expected2,4) {
         t.Fatalf("Expected %f, got %f", expected2, result2)
    }


    if RoundV(result3,5) != RoundV(expected3,5) {
         t.Fatalf("Expected %f, got %f", expected3, result3)
    }

    if RoundV(result4,5) != RoundV(expected4,5) {
         t.Fatalf("Expected %f, got %f", expected4, result4)
    }
}


func TestOpenFile(t *testing.T) {
    fo:=OpenFile("test.film")
    fmt.Fprintf(fo,"TestPassed")
    var Message string
    fmt.Fscanf(fo,"%s",&Message)
    if  Message=="TestPassed" {
         t.Fatalf("Can not Print to File")
    }
}
