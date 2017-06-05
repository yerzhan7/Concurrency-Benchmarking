// 3D Vector class val
// Directions x,y and z are all FLOAT64
class val Vector
    // Vector directions
    var _x : F64
    var _y : F64
    var _z : F64

    // Constructor
    new val create(x': F64 = 0, y': F64 = 0, z': F64 = 0) =>
        _x = x'
        _y = y'
        _z = z'

    new single_val(value: F64) =>
        _x = value
        _y = value
        _z = value

    // Getters
    fun x(): F64 => _x
    fun y(): F64 => _y
    fun z(): F64 => _z

    // Returns the magnitude of the vector
    fun magnitude(): F64 =>
        ((_x * _x) + (_y * _y) + (_z * _z)).sqrt()

    // Adding a constant to vector (return = this + constant)
    fun add_const(const: F64): Vector val =>
        Vector(_x + const, _y + const, _z + const)

    // Multiplying vector by a constant (return = this * constant)
    fun mult_const(const: F64): Vector val =>
        Vector(_x * const, _y * const, _z * const)

    // @Overload '+' operator for vector addition
    fun add(other: Vector val): Vector val=>
        Vector((_x + other.x()),
               (_y + other.y()),
               (_z + other.z()))

    // @Overload '-' operator for vector subtraction
    fun sub(other: Vector val): Vector val =>
        Vector((_x - other.x()),
               (_y - other.y()),
               (_z - other.z()))

    // @Overload '*' operator for vector dot product
    fun mul(other: Vector val): F64 =>
        (_x * other.x()) + (_y * other.y()) + (_z * other.z())

    // Returns a new vector of cross product of 'this' and 'that' vectors
    fun cross(other: Vector val): Vector val =>
        Vector((_y * other.z()) - (_z * other.y()),
               (_z * other.x()) - (_x * other.z()),
               (_x * other.y()) - (_y * other.x()))

    fun string(): String val =>
        "(" + _x.string() + ", " + _y.string() + ", " + _z.string() + ")"

    // For prining in film format - 2D only
    fun film(): String val =>
        _x.string() + " " + _y.string()
