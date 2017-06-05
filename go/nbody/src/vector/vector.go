/* Andreas Voskou and Simon Charalambous for MSc Group Project */

/*Integrated vector functions used in the main nbody function*/

package vector

import (
    "math"
)

/*returns the magnitude of a vector   */
func Magnitude(r [3]float64) float64 {
    return math.Abs(math.Sqrt(r[1]*r[1] + r[2]*r[2] + r[0]*r[0]))
}


/* addition of 2 vectors */
func Sum(r1 [3]float64, r2 [3]float64) (result [3]float64) {
    result[0] = r1[0] + r2[0]
    result[1] = r1[1] + r2[1]
    result[2] = r1[2] + r2[2]

    return result
}


/* addition of 4 vectors */
func Sum4(r1, r2, r3, r4 [3]float64) (result [3]float64) {
    result[0] = r1[0] + r2[0] + r3[0] + r4[0]
    result[1] = r1[1] + r2[1] + r3[1] + r4[1]
    result[2] = r1[2] + r2[2] + r3[2] + r4[2]

    return result
}


/* substraction of vectors*/
func Dif(r1 [3]float64, r2 [3]float64) (result [3]float64) {
    result[0] = r1[0] - r2[0]
    result[1] = r1[1] - r2[1]
    result[2] = r1[2] - r2[2]

    return result
}


/* dot product of vectors */
func Dot(r1 [3]float64, r2 [3]float64) float64 {
    var result [3]float64

    result[0] = r1[0] * r2[0]
    result[1] = r1[1] * r2[1]
    result[2] = r1[2] * r2[2]

    return (result[0] + result[1] + result[2])
}


/* cross product of vectors */
func Cros(r1 [3]float64, r2 [3]float64) (result [3]float64) {
    result[0] = r1[1]*r2[2] - r1[2]*r2[1]
    result[1] = r1[2]*r2[0] - r1[0]*r2[2]
    result[2] = r1[0]*r2[1] - r1[1]*r2[0]

    return result
}

/* multiply vector with a constant  */

func Mltp(r [3]float64, c float64) (result [3]float64) {
    result[0] = r[0] * c
    result[1] = r[1] * c
    result[2] = r[2] * c

    return result
}

/* add a constant to a voctor*/

func Addc(r [3]float64, c float64) (result [3]float64) {
    result[0] = r[0] + c
    result[1] = r[1] + c
    result[2] = r[2] + c

    return result
}

