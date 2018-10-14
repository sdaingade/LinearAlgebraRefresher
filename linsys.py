from decimal import Decimal, getcontext
from copy import deepcopy

from vector import Vector
from plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def swap_rows(self, row1, row2):
        print("swap_rows - row1: {}, row2: {}".format(row1, row2))
        temp = deepcopy(self.planes[row1])
        self.planes[row1] = self.planes[row2]
        self.planes[row2] = temp


    def multiply_coefficient_and_row(self, coefficient, row):
        print("multiply_coefficient_and_row - coefficient: {}, row: {}".format(coefficient, row))
        #new_normal_vector = [x*coefficient for x in self.planes[row].normal_vector]
        new_normal_vector = self.planes[row].normal_vector.times_scalar(coefficient)
        self.planes[row] = Plane(new_normal_vector, self.planes[row].constant_term * coefficient)


    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        print("add_multiple_times_row_to_row - coefficient: {}, row_to_add: {}, row_to_be_added_to: {}".format(coefficient, row_to_add, row_to_be_added_to))
        #new_normal = [x*coefficient for x in self.planes[row_to_add].normal_vector]
        new_normal = self.planes[row_to_add].normal_vector.times_scalar(coefficient)
        #print(str(type(new_normal)))
        self.planes[row_to_be_added_to] = Plane(self.planes[row_to_be_added_to].normal_vector.plus(new_normal),
                                                self.planes[row_to_be_added_to].constant_term +
                                                  (self.planes[row_to_add].constant_term * coefficient))

    def indices_of_first_nonzero_terms_in_each_row(self):
        num_equations = len(self)
        num_variables = self.dimension

        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices


    def __len__(self):
        return len(self.planes)


    def __getitem__(self, i):
        return self.planes[i]


    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)


    def __str__(self):
        ret = 'Linear System:\n'
        temp = ['Equation {}: {}'.format(i+1,p) for i,p in enumerate(self.planes)]
        ret += '\n'.join(temp)
        return ret

    """
        Assumptions for Test Cases:
        1. Swap with the topmost row below current row
        2. Don't numtiply rows by numbers
        3. Only add a multiple of a row to the rows underneath
    """
    def compute_triangular_form(self):
        system = deepcopy(self)

        for i in range(0, len(system)):
            LinearSystem.my_compute_current_row(system, i, len(system)-1, i)
            print("system : {}".format(system))
        return system

    @staticmethod
    def my_compute_current_row(linear_system, start_row, end_row, col):
        print("my_compute_current_row - start_row: {}, end_row: {}, col: {}".format(start_row, end_row, col))
        if start_row == end_row:
            return
        
        current = linear_system.planes[start_row].normal_vector
        if not Plane.first_nonzero_index(current) == col:
            ahead_row = start_row + 1
            while ahead_row <= end_row:
                ahead = linear_system.planes[ahead_row].normal_vector
                if Plane.first_nonzero_index(ahead) == col:
                    linear_system.swap_rows(start_row, ahead_row)
                    current = linear_system.planes[start_row].normal_vector
                    break
                ahead_row = ahead_row + 1
            
            if ahead_row > end_row:
                raise Exception("No row with non zero index for col {}".format(col))

        ahead_row = start_row + 1
        while ahead_row <= end_row:
            ahead = linear_system.planes[ahead_row].normal_vector
            coeff = (ahead[col]/current[col]) * -1
            if not MyDecimal(coeff).is_near_zero():
                linear_system.add_multiple_times_row_to_row(coeff, start_row, ahead_row)
            ahead_row = ahead_row + 1



class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])

s.swap_rows(0,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print("test case 1 failed")
else:
    print 'test case 1 passed'


s.swap_rows(1,3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print("test case 2 failed")
else:
    print 'test case 2 passed'


s.swap_rows(3,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print("test case 3 failed")
else:
    print 'test case 3 passed'


s.multiply_coefficient_and_row(1,0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 4 failed'
else:
    print 'test case 4 passed'


s.multiply_coefficient_and_row(-1,2)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 5 failed'
else:
    print 'test case 5 passed'


s.multiply_coefficient_and_row(10,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 6 failed'
else:
    print 'test case 6 passed'


s.add_multiple_times_row_to_row(0,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 7 failed'
else:
    print 'test case 7 passed'


s.add_multiple_times_row_to_row(1,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 8 failed'
else:
    print 'test case 8 passed'


s.add_multiple_times_row_to_row(-1,1,0)
if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 9 failed'
else:
    print 'test case 9 passed'


p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
print("test case 10 t: {}".format(t))
if not (t[0] == p1 and
        t[1] == p2):
    print 'test case 10 failed'
else:
    print 'test case 10 passed'


p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
print("test case 11 t: {}".format(t))
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print 'test case 11 failed'
else:
    print 'test case 11 passed'
    

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form()
print("test case 12 t: {}".format(t))
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        t[3] == Plane()):
    print 'test case 12 failed'
else:
    print 'test case 12 passed'

p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
print("test case 13 t: {}".format(t))
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print 'test case 13 failed'
else:
    print 'test case 13 passed'


print s.indices_of_first_nonzero_terms_in_each_row()
#print '{},{},{},{}'.format(s[0],s[1],s[2],s[3])
print len(s)
print s

s[0] = p1
print s

print MyDecimal('1e-9').is_near_zero()
print MyDecimal('1e-11').is_near_zero()
