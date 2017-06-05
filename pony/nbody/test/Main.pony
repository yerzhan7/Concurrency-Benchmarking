//Vector unit testing

use "ponytest"
use "../src"

actor Main is TestList
    new create(env: Env) =>
        PonyTest(env, this)

    new make() =>
        None

    fun tag tests(test: PonyTest) =>
        test(_TestMagnitude)
        test(_TestAddConst)
        test(_TestMultConst)
        test(_TestSumming)
        test(_TestSubtracting)
        test(_TestDotProduct)
        test(_TestCrossProduct)
        
class iso _TestMagnitude is UnitTest 
    fun name(): String => "Magnitude"

    fun apply(h: TestHelper) => 
        var a : Vector = Vector(3, 4)
        var b : Vector = Vector(5, 12, 0)
        var c : Vector = Vector(-66, 33.25, 0.5)
        var zero : Vector = Vector()
        h.assert_eq[F64](a.magnitude(), 5)
        h.assert_eq[F64](b.magnitude(), 13)
        h.assert_eq[F64](c.magnitude().floor(), 73) // 73.9040763 (Approx.)
        h.assert_eq[F64](zero.magnitude(), 0) // Magnitude of zero vector is zero

class iso _TestAddConst is UnitTest 
    fun name(): String => "Adding a constant"

    fun apply(h: TestHelper) =>
        var a : Vector = Vector(3, 4, -4.5)
        var b : F64 = 2.5
        var c : Vector = a.add_const(b)
        h.assert_eq[F64](c.x(), 5.5)
        h.assert_eq[F64](c.y(), 6.5)
        h.assert_eq[F64](c.z(), -2)
        b = -11
        c = c.add_const(b)
        h.assert_eq[F64](c.x(), -5.5)
        h.assert_eq[F64](c.y(), -4.5)
        h.assert_eq[F64](c.z(), -13)

class iso _TestMultConst is UnitTest 
    fun name(): String => "Multiplying by a constant"

    fun apply(h: TestHelper) =>        
        var a : Vector = Vector(3, 4, -4.5)
        var c : F64 = -2.5
        var b : Vector = a.mult_const(c)
        h.assert_eq[F64](b.x(), -7.5)
        h.assert_eq[F64](b.y(), -10)
        h.assert_eq[F64](b.z(), 11.25)
        c = 0
        b = b.mult_const(c)
        h.assert_eq[F64](b.x(), 0)
        h.assert_eq[F64](b.y(), 0)
        h.assert_eq[F64](b.z(), 0)
        
class iso _TestSumming is UnitTest 
    fun name(): String => "Summing vectors"

    fun apply(h: TestHelper) => 
        var a : Vector = Vector(3, 4)
        var b : Vector = Vector(2, 8, 0)
        var c : Vector
        c = a + b
        h.assert_eq[F64](c.x(), 5)
        h.assert_eq[F64](c.y(), 12)
        h.assert_eq[F64](c.z(), 0) 

class iso _TestSubtracting is UnitTest 
    fun name(): String => "Subtracting vectors"
        
    fun apply(h: TestHelper) =>
        var a : Vector = Vector(3, 4.3, 0)
        var b : Vector = Vector(3, -4, -14)
        var c : Vector
        c = a - b
        h.assert_eq[F64](c.x(), 0)
        h.assert_eq[F64](c.y(), 8.3)
        h.assert_eq[F64](c.z(), 14) 
        
class iso _TestDotProduct is UnitTest
    fun name(): String => "Dot product"

    fun apply(h: TestHelper) =>
        var a : Vector = Vector(3, -4, 34.3)
        var b : Vector = Vector(6.5, 19, -3)
        var c : F64
        c = a * b
        h.assert_eq[F64](c, -159.4)
        b = Vector(0)
        c = a * b
        h.assert_eq[F64](c, 0)
        a = Vector(0)
        c = a * b
        h.assert_eq[F64](c, 0)

class iso _TestCrossProduct is UnitTest
    fun name(): String => "Cross product"

    fun apply(h: TestHelper) =>
        var a : Vector = Vector(6.5, -19, 0.65)
        var b : Vector = Vector(-11, -0.1, -5)
        var c : Vector = a.cross(b)
        h.assert_eq[F64](c.x(), 95.065)
        h.assert_eq[F64](c.y(), 25.35)
        h.assert_eq[F64](c.z(), -209.65)
        
