from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No unique parallel component"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No unique orthogonal component"

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __iter__(self):
        return iter(self.coordinates)

    def __getitem__(self,index):
        return self.coordinates[index]

    def plus(self, v):
        new_coordinates = [x + y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def minus(self, v):
        new_coordinates = [x - y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
    
    def times_scalar(self, c):
        new_coordinates = [x * Decimal(c) for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        #print("coordinates: " + str(type(self.coordinates[1])))
        coordinates_squared = [x * x for x in self.coordinates]
        return sqrt(sum(coordinates_squared))
    
    def normalized(self): # Unit vector in the direction of self
        try:
            magnitude = self.magnitude()
            #print("magnitude: " + str(type(magnitude)))
            return self.times_scalar(Decimal('1.0')/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG) # Magnitude is zero for zero vector
    
    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])
    
    @staticmethod
    def replace_if_within_tolerance(val, compare_with, tolerance=1e-10):
        if abs(val - compare_with) < tolerance:
            return compare_with
        else:
            return val 

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            #print("u1 {}".format(u1))
            u2 = v.normalized()
            #print("u2 {}".format(u2))
            k = u1.dot(u2)
            k = Vector.replace_if_within_tolerance(k, 1)
            k = Vector.replace_if_within_tolerance(k, -1)
            #print("k {}".format(k))
            angle_in_radians = acos(k)
            #print("angle_in_radians {}".format(angle_in_radians))

            if in_degrees:
                degree_per_radian = 180.0/pi
                return angle_in_radians * degree_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with the zero vector")
            else:
                raise e
    
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi)
    
    def component_parallel_to(self, basis):
        try:
            u_b = basis.normalized()
            weight = self.dot(u_b)
            return u_b.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def component_orthogonal_to(self, basis):
        try:
            parallel_proj = self.component_parallel_to(basis)
            return self.minus(parallel_proj)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        x_1, y_1, z_1 = self.coordinates
        x_2, y_2, z_2 = v.coordinates

        cross_product = [ y_1*z_2 - y_2*z_1,
                          -(x_1*z_2 - x_2*z_1),
                          x_1*y_2 - x_2*y_1
                        ]
        return Vector(cross_product)

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()
    
    def area_of_trainge_with(self, v):
        return self.area_of_parallelogram_with(v)/2.0

"""

v = Vector([8.218, -9.341])
w = Vector([-1.129, 2.111])
print(v.plus(w))

v = Vector([7.119, 8.215])
w = Vector([-8.223, 0.878])
print(v.minus(w))

v = Vector([1.671, -1.012, -0.318])
c = 7.41
print(v.times_scalar(c))

v = Vector([-0.221, 7.437])
print(v.magnitude())

v = Vector([8.813, -1.331, -6.274])
print(v.magnitude())

v = Vector([5.581, -2.136])
print(v.normalized())

v = Vector([1.996, 3.108, -4.554])
print(v.normalized())

v = Vector([7.887, 4.138])
w = Vector([-8.802, 6.776])
print(v.dot(w))

v = Vector([-5.995, -4.904, -1.873])
w = Vector([-4.496, -8.755, 7.103])
print(v.dot(w))

v = Vector([3.183, -7.627])
w = Vector([-2.668, 5.319])
print(v.angle_with(w))

v = Vector([7.35, 0.221, 5.188])
w = Vector([2.751, 8.259, 3.985])
print(v.angle_with(w, in_degrees=True))

v = Vector([-7.579, -7.88])
w = Vector([22.737, 23.64])
print("Is parallel: {}".format(v.is_parallel_to(w)))
print("Is Orthogonal: {}".format(v.is_orthogonal_to(w)))

v = Vector([-2.029, 9.97, 4.172])
w = Vector([-9.231, -6.639, -7.245])
print("Is parallel: {}".format(v.is_parallel_to(w)))
print("Is Orthogonal: {}".format(v.is_orthogonal_to(w)))

v = Vector([-2.328, -7.284, -1.214])
w = Vector([-1.821, 1.072, -2.94])
print("Is parallel: {}".format(v.is_parallel_to(w)))
print("Is Orthogonal: {}".format(v.is_orthogonal_to(w)))

v = Vector([2.118, 4.827])
w = Vector([0, 0])
print("Is parallel: {}".format(v.is_parallel_to(w)))
print("Is Orthogonal: {}".format(v.is_orthogonal_to(w)))

v = Vector([3.039, 1.879])
w = Vector([0.825, 2.036])
print(v.component_parallel_to(w))

v = Vector([-9.88, -3.264, -8.159])
w = Vector([-2.155, -9.353, -9.473])
print(v.component_orthogonal_to(w))

v = Vector([3.009, -6.172, 3.692, -2.51])
w = Vector([6.404, -9.144, 2.759, 8.718])
vpar = v.component_parallel_to(w)
vort = v.component_orthogonal_to(w)
print("Parallel component: {}".format(vpar))
print("Orthogonal component: {}".format(vort))

v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
print(v.cross(w))

v = Vector([-8.987, -9.838, 5.031])
w = Vector([-4.268, -1.861, -8.866])
print(v.area_of_parallelogram_with(w))

v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
print(v.area_of_trainge_with(w))

"""
