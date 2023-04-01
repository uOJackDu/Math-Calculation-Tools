#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 15:50:54 2021

@author: jackdu
"""
class Polynomial:
    def __init__(self, coefficients):
        self.coeffs = coefficients
        for coeff in self.coeffs:  # eliminating leading zeroes
            if coeff != 0 or self.coeffs == [0]:
                break
            else:
                self.coeffs = self.coeffs[1:]
        if self.coeffs == []:
            self.coeffs = [0]
        for i, coeff in enumerate(self.coeffs):
            if int(coeff) == coeff:
                self.coeffs[i] = int(self.coeffs[i])
        self.degree = len(self.coeffs) - 1
    
    def __str__(self):
        if self.degree == 0:
            return str(self.coeffs[-1])
        output = ""
        for i in range(self.degree):
            if self.coeffs[i] != 0:
                if output == "":  # add the first coefficient
                    if self.coeffs[i] == -1: 
                        output += "-"
                    elif abs(self.coeffs[i]) != 1:
                        output += str(self.coeffs[i])
                elif abs(self.coeffs[i]) != 1:  # not the first coefficient
                    output += str(abs(self.coeffs[i]))
                # add x^power
                output += "x"
                if self.degree - i != 1:
                    output += "^" + str(self.degree-i)
            if self.coeffs[i+1] > 0:
                output += " + "
            elif self.coeffs[i+1] < 0:
                output += " - "
        if self.coeffs[-1] != 0:
            output += str(abs(self.coeffs[-1]))
        return output
    
    def is_root(self, n):
        y = 0
        for i in range(self.degree+1):
            y += self.coeffs[i] * (n**(self.degree-i))
        return y == 0
    
    def derivative(self):
        d_coeffs = []
        for i in range(self.degree):
            d_coeffs.append(self.coeffs[i]*(self.degree-i))
        return Polynomial(d_coeffs)
    
    def add(self, f):
        li1, li2 = self.coeffs[:], f.coeffs[:]
        if len(li1) < len(li2):  # li2 will be shorter
            li1, li2 = li2, li1
        res = []
        diff = len(li1) - len(li2)
        li2 = [0]*diff + li2
        for i in range(len(li1)):
            res.append(li1[i]+li2[i])
        return Polynomial(res)
    
    def subtract(self, f):
        li1, li2 = self.coeffs[:], f.coeffs[:]
        if len(li1) < len(li2):  # li2 will be shorter
            li1, li2 = li2, li1
        res = []
        diff = len(li1) - len(li2)
        li2 = [0]*diff + li2
        for i in range(len(li1)):
            res.append(li1[i]-li2[i])
        return Polynomial(res)
    
    def multiply(self, f):
        li1, li2 = self.coeffs[:], f.coeffs[:]
        if len(li1) < len(li2):  # li2 will be shorter
            li1, li2  = li2, li1
        n = len(li2) - 1
        res = Polynomial([0])
        for c2 in li2:
            temp = []
            for c1 in li1:
                temp.append(c2*c1)
            temp += [0] * n
            n -= 1
            res = res.add(Polynomial(temp))
        return res
    
    def divide(self, f):
        li1, li2 = self.coeffs[:], f.coeffs[:]
        res = []
        i = 0
        while i + len(li2) <= len(li1):
            c = li1[i] / li2[0]
            res.append(c)
            temp = f.multiply(Polynomial([c])).coeffs
            for j in range(len(temp)):
                li1[j+i] -= temp[j]
            i += 1
        if sum(li1) == 0:
            return Polynomial(res), None
        else:
            return Polynomial(res), Rational(Polynomial(li1), Polynomial(li2))


class Rational:
    def __init__(self, poly1, poly2):
        self.n = poly1
        self.d = poly2
    
    def __str__(self):
        return "{} / {}".format(self.n, self.d)
    
    def derivative(self):
        f, g = self.n, self.d
        return Rational(f.derivative().multiply(g).subtract(g.derivative().multiply(f)),
                        g.multiply(g))
    
    def asymptote(self):
        if self.n.degree < self.d.degree:
            return Polynomial([0])
        elif self.n.degree == self.d.degree:
            return Polynomial([self.n.coeffs[0]/self.d.coeffs[0]])
        else:
            f1, f2 = self.n.divide(self.d)
            return f1


class Coord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)
    
    def dis_to_line(self, l):
        s = l.direc
        return Vector.vec_btwn(self, l.point).cross(s).mag() / s.mag()
    
    def dis_to_plane(self, plane):
        n = plane.normal
        return abs(Vector.vec_btwn(self, plane.point).dot(n)) / n.mag()
    
    def is_on_plane(self, plane):
        return plane.normal.dot(self) + plane.d == 0


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.z)
    
    @staticmethod
    def pos_vec(point):
        return Vector(point.x, point.y, point.z)
    
    @staticmethod
    def vec_btwn(start_p, end_p):  # vector from start point to end point
        x1, y1, z1 = start_p.x, start_p.y, start_p.z
        x2, y2, z2 = end_p.x, end_p.y, end_p.z
        return Vector(x2-x1, y2-y1, z2-z1)
    
    def add(self, v):
        return Vector(self.x+v.x, self.y+v.y, self.z+v.z)
    
    def subtract(self, v):
        return Vector(self.x-v.x, self.y-v.y, self.z-v.z)
    
    def times(self, k):
        # k is a constant
        return Vector(k*self.x, k*self.y, k*self.z)
    
    def dot(self, v):
        return self.x*v.x + self.y*v.y + self.z*v.z
    
    def cross(self, v):
        return Vector(self.y*v.z-self.z*v.y,
                      self.z*v.x-self.x*v.z,
                      self.x*v.y-self.y*v.x)
    
    def mag(self):
        return (self.x**2+self.y**2+self.z**2) ** 0.5
    
    def proj(self, v):
        return v.times(self.dot(v)/(v.mag()**2))
    
    def is_ortho(self, v):
        return self.dot(v) == 0


class Line:
    def __init__(self, point, vector):
        self.point = point
        self.direc = vector
    
    def __str__(self):
        return "[x, y, z] = [{}, {}, {}] + t{}".format(self.point.x,
                                                       self.point.y,
                                                       self.point.z,
                                                       self.direc)
    
    def dis_to_line(self, l):
        n = self.direc.cross(l.direc)
        return abs(Vector.vec_btwn(self.point, l.point).dot(n)) / n.mag()
    
    def dis_to_plane(self, plane):
        return self.point.dis_to_plane(plane)
    
    def intersect_plane(self, plane):
        if self.direc.dot(plane.normal) == 0:
            if self.point.is_on_plane(plane):
                # the line lies on the plane
                return "There are infinite solutions."
            else:
                # the line does not intersect the plane
                return None
        else:
            n = plane.normal
            t = -(plane.d+n.dot(self.point)) / n.dot(self.direc)
            res = Vector.pos_vec(self.point).add(self.direc.times(t))
            return Coord(res.x, res.y, res.z)


class Plane:
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal
        self.a = normal.x
        self.b = normal.y
        self.c = normal.z
        self.d = -normal.dot(point)
    
    @staticmethod
    def add_next_coeff(output, n):
        if output != "":
            if n > 0:
                output += " + "
            elif n < 0:
                output += " - "
            if abs(n) != 1:
                output += str(abs(n))
        else:
            if n == -1:
                output += "-"
            elif n != 1:
                output += str(n)
        return output
        
    
    def __str__(self):
        output = ""
        if self.a != 0:
            if self.a == -1:
                output += "-"
            elif self.a != 1:
                output += str(self.a)
            output += "x"
        if self.b != 0:
            output = self.add_next_coeff(output, self.b)
            output += "y"
        if self.c != 0:
            output = self.add_next_coeff(output, self.c)
            output += "z"
        if self.d != 0:
            if output != "":
                if self.d > 0:
                    output += " + "
                elif self.d < 0:
                    output += " - "
                output += str(abs(self.d))
            else:
                output += str(self.d)
        return output + " = 0"

#%% Polynomial functions
f1 = Polynomial([4, 0, 0, -7])
f2 = Polynomial([2])

f3 = f1.multiply(f2)
f4 = f1.derivative()

print("f1:", f1)
print("f2:", f2)
print("f3:", f3)
print(f4.derivative().derivative())

f5 = Polynomial([1, 0, -1])
print("f5:", f5)
print(f5.is_root(-1))

#%% Polynomial division
f1 = Polynomial([2, 2, 3, 1, 5])
f2 = Polynomial([-2, 0, 1])

f3, f4 = f1.divide(f2)
# f3, f4 = f2.divide(f1)

print("f1:", f1)
print("f2:", f2)
print("f3:", f3)
print("f4:", f4)

#%% Derivative of rational functions
# f1 = Polynomial([1, 1])
# f2 = Polynomial([1, -1])
f1 = Polynomial([4, 0, 0, -7])
f2 = Polynomial([2, 0, 3])
f3 = Rational(f1, f2)

f4 = f3.derivative()

# print("f1:", f1)
# print("f2:", f2)
print("f3:", f3)
print("asymptote of f3:", f3.asymptote())
print("f4:", f4)
print(f4.n.coeffs)

#%% Vectors
P1 = Coord(5, 7, 3)
P2 = Coord(-8, 5, 6)
v = Vector.vec_btwn(P2, P1)
w = Vector(2, 4, 5)
l1 = Line(P1, w)

print("v =", v)
print("w =", w)
print("5v =", v.times(5))
print("w - 5v =", w.subtract(v.times(5)))

u = Vector(5, 8, 2)
v = Vector(-7, 3, 6)
w = u.cross(v)
print("u =", u)
print("v =", v)
print("w =", w)
print(u.is_ortho(v))
print(u.is_ortho(w))

#%% Distance between skew lines
l1 = Line(Coord(5, 2, -3), Vector(5, 5, 1))
l2 = Line(Coord(-1, -4, -4), Vector(7, -2, -2))

d = l1.dis_to_line(l2)

print("l1:", l1)
print("l2:", l2)
print("distance between l1 and l2:", d)

#%%Distance between a point and a line
P1 = Coord(1, 2, 3)
l1 = Line(Coord(5, -4, -2), Vector(1, 2, 3))

d = P1.dis_to_line(l1)

print("P1:", P1)
print("l1:", l1)
print("distance between P1 and l1:", d)

#%% Distance between a point and a plane
n1 = Vector(4, 2, 1)
pi1 = Plane(Coord(4, 0, 0), n1)

# P1 = Coord(10, 3, -8)
P1 = Coord(2, 2, 4)

d = P1.dis_to_plane(pi1)

print("P1:", P1)
print("pi1:", pi1)
print("distance between P1 and pi1:", d)

#%% Distance between a line and a plane
l1 = Line(Coord(3, 8, 1), Vector(-1, 3, -2))

n1 = Vector(8, -6, -13)
pi1 = Plane(Coord(0, -2, 0), n1)

d = l1.dis_to_plane(pi1)

print("l1:", l1)
print("pi1:", pi1)
print("distance between l1 and pi1:", d)

#%% Intersection between a line and a plane
l1 = Line(Coord(4, 12, -19), Vector(2, -3, 5))

n1 = Vector(6, -2, 3)
pi1 = Plane(Coord(-1, 0, 0), n1)

P = l1.intersect_plane(pi1)

print("l1:", l1)
print("pi1:", pi1)
print(P)
