import math
from decimal import Decimal

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def my_add(self, v):
        if not len(self.coordinates) == len(v.coordinates):
            raise ValueError('Vector dimensions do not match')
        
        vectorLength = len(self.coordinates)
        result = []
        for i in range(vectorLength):
            result.append(self.coordinates[i] + v.coordinates[i])

        return Vector(result)

    def my_subtract(self, v):
        if not len(self.coordinates) == len(v.coordinates):
            raise ValueError('Vector dimensions do not match')
        
        vectorLength = len(self.coordinates)
        result = []
        for i in range(vectorLength):
            result.append(self.coordinates[i] - v.coordinates[i])

        return Vector(result)

    def my_multiply(self, s):
        result = []
        vectorLength = len(self.coordinates)
        for i in range(vectorLength):
            result.append(self.coordinates[i] * s)

        return Vector(result)

    def plus(self, v):
        # list comprehension in python
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        # list comprehension in python
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        # list comprehension in python
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def my_magnitude(self):
        sum = 0.0
        for x in self.coordinates:
            sum += (x*x)
        return math.sqrt(sum)

    def my_direction(self):
        mag = self.my_magnitude()
        return self.my_multiply(1/mag)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return math.sqrt(sum(coordinates_squared))
    
    def normalized(self): #Unit vector in the direction of original vector
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1/magnitude)
        except ZeroDivisionError:
            raise Exception("Cannot normalize the zero vector")

    def my_dotproduct(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    def my_theta(self, v):
        dot_product = self.my_dotproduct(v)
        my_mag = self.my_magnitude()
        v_mag = v.my_magnitude()

        return math.acos(dot_product/(my_mag * v_mag)) # Angle in radians

    def my_parallel_proj_to(self, b):
        unit_b = b.my_direction()
        mag_of_proj_of_v_onto_b = self.my_dotproduct(unit_b)
        return unit_b.my_multiply(mag_of_proj_of_v_onto_b)

    def my_orthogonal_proj_to(self, b):
        # Orthogonal_proj_of_Vector(V) =
        # Vector(V) - parallel_proj_of_Vector(V) 
        parallel_proj = self.my_parallel_proj_to(b)
        return self.my_subtract(parallel_proj)

    def my_crossproduct(self, w):
        if len(self.coordinates) != 3 or len(w.coordinates) != 3:
            raise ValueError("Vectors need to be of size 3")
        x1 = self.coordinates[0]
        y1 = self.coordinates[1]
        z1 = self.coordinates[2]
        x2 = w.coordinates[0]
        y2 = w.coordinates[1]
        z2 = w.coordinates[2]
        return Vector([(y1*z2 - y2*z1), -1 * (x1*z2 - x2*z1), (x1*y2 - x2*y1)])

    def my_is_parallel(self, v):
        return (self.my_is_zero() or
                v.my_is_zero() or
                self.my_theta() == 0 or
                self.my_theta() == math.pi
               )

    def my_is_zero(self, tolerence=1e-10):
        return self.my_magnitude() < tolerence

    def __getitem__(self, i):
        return self.coordinates[i]

    def __iter__(self):
        return self.coordinates.__iter__()
        
        

"""
 Magnitude and Direction of a Vector

 Magnitude of a vector is sqrt(square(x) + square(y) + square(z))

 A unit vector is a vector whose magnitude is 1.
 A vectors direction can be represented by a unit vector
"""
"""
 Normalization: Process of finding a unit vector in the same direction as a
 given vector

 Steps for normalization
 1. Find the magnitude of the vector
 2. Perform a scalar multiplication of vector with 1/magnitude(v)
    (divide vector by magnitude). This gives unit vector in the direction of v

Note: A zero vector [0,0,0] has magnitude 0.
      You cannot compute the direction of a zero vector by the method above.
      A zero vector has no direction.
"""

"""
Inner Product of two vectors (also called Dot Product)

Vector(V) * Vector(W) = ||V|| * ||W|| * Cos(theta)
where theta is the angle between the two vectors V and W.

Inner product is  a number not a vector

More readily compitable formulae:
Vector(V) * Vector(W) = v1*w1 + v2*w2 + v3*w3 + ... + vn*wn

"""

"""
Finding angle between two vectors

theta = arc-cos(V*W/(||v|| * ||W||))
"""

"""
Degress to radians and back

The general formula for converting from degrees to radians
is to simply multiply the number of degree by pi/180 degrees

The general formula for converting from radians to degrees
is to simply multiply the number of radians by 180 degree/pi

"""

"""
Parallel and orthogonal vectors

1. Parallel vectors
Vector(V) and Vector(W) are parallel if one is a scalar multiple
of the other.

V and W are parallel even if the scalar is -1.
Angle between V and W is 0 or 180 degress.

2. Orthogonal vectors
Vector(V) and Vector(W) are orthogonal if their dot product is zero.

Vector(V) * Vector(W) = 0

We know Vector(V) * Vector(W) = ||V|| * ||W|| * Cos(theta)
Theta should be 90 degrees for Vector(V) * Vector(W) = 0
ie the vectors are at 90 degrees from each other.

zero vector is parallel and orthogonal to all vectors.
zero vector is the only vector orthogonal to itself

"""

"""
Projecting Vectors

Orthogonality:
Tool for decomposing objects into combination of simpler objects
in a structured way.

There are two vectors V and B

Vector(B) here is called a basis vector.

Vector(V) can be expressed as sum of two vectors
1. Vector that is parallel to vector B (projection of vector(V) on to Vector(B))
2. Vector that is orthogonal to Vector B (angle wrt vector(B) is 90 degrees)

magnitude of projection of Vector(v) on Vector(b) is
 = Vector(v)* unit vector(B)    <-- This is a dot product 

The projection is a scalar quantity.

projection of Vector(v) on Vector(b) is
= (magnitude of projection of Vector(v) on Vector(b)) * unit vector(B)
   <-- This is scalar multiplication
   
= (Vector(v)* unit vector(B)) * unit vector(B)
  See my_parallel_proj_to method above
"""

"""
Cross Product

* Another form of vector multiplication
* Only exists in three dimensions
  (No higher dimensional version)

* Cross product Vector(v) cross Vector(W) is orthogonal to both
  Vector(V) and Vector(W)
* || Vector(V) cross Vector(W)|| = ||Vector(V)|| * ||Vector(W)|| * Sin(theta)

* The output of the cross product is a VECTOR, NOT A number.
* Cross product of two parallel vectors is the zero vector as theta is 0 or 180 (pi)
  ans Sin(theta) is zero.
* If Vector(V) or Vector(W) is the zero vector, then the cross product will also be
  the zero vector.
* There are two vectors that can fit the direction of the cross product of
  Vector(V) and Vector(W). We use the right hand rule to determin the direction
  thumb points to Vector(V), index points to Vector(W) then middle finger points
  to the cross product

* Vector(V) cross Vector(W) = - (Vector(W) cross Vector(V))
  anti-commutative

"""

my_vector = Vector([1,2,3])
print(my_vector)

my_vector2 = Vector([1,2,3])
print(my_vector == my_vector2) #True

my_vector3 = Vector([3,2,1])
print(my_vector == my_vector3) #False

print(my_vector.my_add(my_vector2))

ex1_v1 = Vector([8.218, -9.341])
ex1_v2 = Vector([-1.129, 2.111])

print("Add: {}".format(ex1_v1.my_add(ex1_v2)))
print("Plus: {}".format(ex1_v1.plus(ex1_v2)))

ex2_v1 = Vector([7.119, 8.215])
ex2_v2 = Vector([-8.223, 0.878])

print("Subtract: {}".format(ex2_v1.my_subtract(ex2_v2)))
print("minus: {}".format(ex2_v1.minus(ex2_v2)))

ex3_v1 = Vector([1.671, -1.012, -0.318])

print("Scale: {}".format(ex3_v1.my_multiply(7.41)))
print("Mulyiply: {}".format(ex3_v1.times_scalar(7.41)))

mag_v1 = Vector([-0.221, 7.437])
mag_v2 = Vector([8.813, -1.331, -6.247])
print("magnitude mag_v1: {}".format(mag_v1.my_magnitude()))
print("magnitude mag_v2: {}".format(mag_v2.my_magnitude()))
print("magnitude mag_v1: {}".format(mag_v1.magnitude()))
print("magnitude mag_v2: {}".format(mag_v2.magnitude()))

dir_v1 = Vector([5.581, -2.136])
dir_v2 = Vector([1.996, 3.108,-4.554])

print("direction of unit vector for dir_v1: {}".format(dir_v1.my_direction()))
print("direction of unit vector for dir_v2: {}".format(dir_v2.my_direction()))
print("direction of unit vector for dir_v1: {}".format(dir_v1.normalized()))
print("direction of unit vector for dir_v2: {}".format(dir_v2.normalized()))

dotprod_v1 = Vector([7.887, 4.138])
dotprod_v2 = Vector([-8.802, 6.776])
print("v1 * v2: {}".format(dotprod_v1.my_dotproduct(dotprod_v2)))

dotprod_v3 = Vector([-5.955, -4.904, -1.874])
dotprod_v4 = Vector([-4.496, -8.755, 7.103])
print("v3 * v4: {}".format(dotprod_v3.my_dotproduct(dotprod_v4)))

angle_v1 = Vector([3.183, -7.627])
angle_v2 = Vector([-2.668, 5.319])
print("theta(v1, v2): {}".format(angle_v1.my_theta(angle_v2)))

angle_v3 = Vector([7.35, 0.221, 5.188])
angle_v4 = Vector([2.751, 8.259, 3.985])
print("theta(v3, v4): {}".format(angle_v3.my_theta(angle_v4)))

orth_v1 = Vector([-7.579, -7.88])
orth_v2 = Vector([22.737, 23.64])
print("Dot product of v1 and v2: {}".format(orth_v1.my_dotproduct(orth_v2)))
print("v1 multiplied by scalar: {}".format(orth_v1.my_multiply(3)))

orth_v3 = Vector([-2.029, 9.97, 4.172])
orth_v4 = Vector([-9.231, -6.639, -7.245])
print("Dot product of v3 and v4: {}".format(orth_v3.my_dotproduct(orth_v4)))

orth_v5 = Vector([-2.328, -7.284, -1.214])
orth_v6 = Vector([-1.821, 1.072, -2.94])
print("Dot product of v5 and v6: {}".format(orth_v5.my_dotproduct(orth_v6)))

orth_v7 = Vector([-2.328, -7.284, -1.214])
orth_v8 = Vector([-1.821, 1.072, -2.94])
print("Dot product of v5 and v6: {}".format(orth_v5.my_dotproduct(orth_v6)))

proj_v1 = Vector([3.039, 1.879])
proj_v2 = Vector([0.825, 2.036])
print("Projection of v1 onto v2: {}".format(proj_v1.my_parallel_proj_to(proj_v2)))

proj_v3 = Vector([-9.88, -3.264, -8.159])
proj_v4 = Vector([-2.155, -9.353, -9.473])
print("Orthogonal of v3 onto v4: {}".format(proj_v3.my_orthogonal_proj_to(proj_v4)))

proj_v5 = Vector([3.009, -6.172, 3.692, -2.51])
proj_v6 = Vector([6.404, -9.144, 2.759, 8.718])
print("Projection of v5 onto v6: {}".format(proj_v5.my_parallel_proj_to(proj_v6)))
print("Orthogonal of v5 onto v6: {}".format(proj_v5.my_orthogonal_proj_to(proj_v6)))

cross_v1 = Vector([8.462, 7.893, -8.187])
cross_v2 = Vector([6.984, -5.975, 4.778])
print("v1 cross v2: {}".format(cross_v1.my_crossproduct(cross_v2)))

cross_v3 = Vector([-8.987, -9.838, 5.031])
cross_v4 = Vector([-4.268, -1.861, -8.866])
print("Area of parallelogram spanned by v3 and v4: {}".format(
    cross_v3.my_crossproduct(cross_v4).my_magnitude()))

cross_v5 = Vector([1.5, 9.547, 3.691])
cross_v6 = Vector([-6.007, 0.124, 5.772])
print("Area of triangle spanned by v5 and v6: {}".format(
    cross_v5.my_crossproduct(cross_v6).my_magnitude() * 0.5))


