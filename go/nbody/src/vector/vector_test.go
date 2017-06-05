/* Test for the vector package */

package vector

import (
       "testing"
        )

func TestMagnitude(t *testing.T) {

    var expected1 float64 = 5
    var expected2 float64 = 13
    var expected3 float64 = 73
    var expected4 float64 = 0

    r1 := [3]float64{3,4}
    r2 := [3]float64{5,12,0}
    r3 := [3]float64{-66,33.25,0.5}
    r4 := [3]float64{}

    result1 := Magnitude(r1)
    result2 := Magnitude(r2)
    result3 := float64(int(Magnitude(r3)))    //73.9040763  (Approx.)
    result4 := Magnitude(r4)                  //Magnitude of zero vector is zero

    if result1 != expected1 {
        t.Fatalf("Expected %f, got %f", expected1, result1)
    }

     if result2 != expected2 {
         t.Fatalf("Expected %f, got %f", expected2, result2)
    }

     if result3 != expected3 {
         t.Fatalf("Expected %f, got %f", expected3, result3)
    }

     if result4 != expected4 {
         t.Fatalf("Expected %f, got %f", expected4, result4)
    }

}

func TestAddc(t *testing.T){

    exp1 := [3]float64{5.5, 6.5, -2}
    exp2 := [3]float64{-5.5, -4.5, -13}

    r := [3]float64{3, 4, -4.5}
    c1 := 2.5
    c2 := -11.0

    result1 := Addc(r,c1)
    result2 := Addc(Addc(r,c1),c2)

    for  i := 0; i < 3; i++{
        if result1[i] != exp1[i] {
            t.Fatalf("Expected %f, got %f", result1[i], exp1[i])
        }

        if result2[i] != exp2[i] {
            t.Fatalf("Expected %f, got %f", result2[i], exp2[i])
	}
    }
}


func TestMltp(t *testing.T){

    exp1 := [3]float64{-7.5, -10, 11.25}
    exp2 := [3]float64{0, 0, 0}

    r := [3]float64{3, 4, -4.5}
    c1 := -2.5
    c2 := 0.0

    result1 := Mltp(r,c1)
    result2 := Mltp(Addc(r,c1),c2)

    for  i := 0; i < 3; i++{
        if result1[i] != exp1[i] {
	    t.Fatalf("Expected %f, got %f", result1[i], exp1[i])
	}

        if result2[i] != exp2[i] {
	    t.Fatalf("Expected %f, got %f", result2[i], exp2[i])
	}
    }
}

func TestSum(t *testing.T){

    exp := [3]float64{5, 12, 0}

    a := [3]float64{3, 4}
    b := [3]float64{2, 8, 0}

    result := Sum(a, b)

    for  i := 0; i < 3; i++{
        if result[i] != exp[i]{
	    t.Fatalf("Expected %f, got %f", result[i], exp[i])
	}
    }
}

func TestSum4(t *testing.T){

    exp := [3]float64{6, 13, 1}

    a := [3]float64{3, 4,0}
    b := [3]float64{2, 8, 0} 
    c := [3]float64{0,0,0}
    d := [3]float64{1,1,1}
    result := Sum4(a, b,c,d)

    
    if result != exp{
	    t.Fatalf("Expected %f, got %f", result, exp)
    }
    
}


func TestDif(t *testing.T){

    exp := [3]float64{0, 8.3, 14}

    a := [3]float64{3, 4.3, 0}
    b := [3]float64{3, -4, -14}

    result := Dif(a, b)

    for  i := 0; i < 3; i++{
        if result[i] != exp[i] {
	    t.Fatalf("Expected %f, got %f", result[i], exp[i])
        }
    }
}


func TestDot(t *testing.T){

    var exp float64 = -159.4

    a := [3]float64{3, -4, 34.3}
    b := [3]float64{6.5, 19, -3}

    result := Dot(a, b)

    if int(result) != int(exp) {
        t.Fatalf("Expected %f, got %f", result, exp)
    }
}


func TestCros(t *testing.T){

    exp1:= [3]float64{0,0,2} 
    exp2:= [3]float64{0,0,0}
    exp3:= [3]float64{0,0,-2}

	
    a := [3]float64{1,0,0}
    b := [3]float64{0,2,0}
    c := [3]float64{0,1,0}
    result1 := Cros(a, b)
    result2 := Cros(b,c)
    result3 := Cros(b,a)
    
    if result1 != exp1 {
        t.Fatalf("Expected %f, got %f", result1, exp1)
    }
    if result2 != exp2 {
        t.Fatalf("Expected %f, got %f", result2, exp2)
    }
    if result3 != exp3 {
        t.Fatalf("Expected %f, got %f", result3, exp3)
    }
}
