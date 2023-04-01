#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 14:42:54 2022

@author: jackdu
"""
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)
    
    def quadrant(self):
        if self.x >= 0:
            if self.y >= 0:
                return 1
            else:  # y < 0
                return 4
        else:  # x < 0
            if self.y >= 0:
                return 2
            else:  # y < 0
                return 3
    
    def distance_to(self, point):
        return ((self.x-point.x)**2+(self.y-point.y)**2) ** 0.5
    
    def midpoint(self, point):
        return Coord((self.x+point.x)/2, (self.y+point.y)/2)
    
    def translate(self, x, y):
        self.x += x
        self.y += y
    
    def reflect_x(self):
        self.y = -self.y
    
    def reflect_y(self):
        self.x = -self.x


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope = self.get_slope()
        self.y_int = self.get_y_int()
    
    def __str__(self):
        if self.slope != None:
            if self.slope == 0:
                return "y = {}".format(self.y_int)
            else:
                output = "y = {}x".format(self.slope)
                if self.y_int > 0:
                    output += " + {}".format(abs(self.y_int))
                elif self.y_int < 0:
                    output += " - {}".format(abs(self.y_int))
                return output
        else:
            return "x = {}".format(self.p1.x)
    
    def get_slope(self):
        if self.p1.x == self.p2.x:
            return None
        else:
            return (self.p2.y-self.p1.y) / (self.p2.x-self.p1.x)
    
    def get_y_int(self):
        if self.slope == None:
            return None
        else:
            return self.p1.y - self.slope*self.p1.x
    
    def y_value(self, x_val):
        if self.slope != None:
            return self.slope*x_val + self.y_int
        else:
            return self.p1.y
    
    def intersect(self, l):
        if self.slope == l.slope:
            if self.slope == None:
                if self.p1.x == l.p1.x:
                    return "There are infinite intersections."
                else:
                    return None
            else:
                if self.y_int == l.y_int:
                    return "There are infinite intersections."
                else:
                    return None
        else:
            if self.slope != None and l.slope != None:
                x_val = (l.y_int-self.y_int) / (self.slope-l.slope)
                return Coord(x_val, self.y_value(x_val))
            else:
                if self.slope == None and l.slope == None:
                    return None
                elif self.slope != None:
                    x_val = l.p1.x
                    return Coord(x_val, self.y_value(x_val))
                elif l.slope != None:
                    x_val = self.p1.x
                    return Coord(x_val, l.y_value(x_val))
    
    def perpendicular_bisector(self):
        new_p1 = self.p1.midpoint(self.p2)
        if self.slope == 0:
            new_p2 = Coord(new_p1.x, new_p1.y+1)
            return Line(new_p1, new_p2)
        else:
            if self.slope == None:
                new_slope = 0
            else:
                new_slope = -1 / self.slope
            new_p2 = Coord(new_p1.x+1, new_p1.y+new_slope)
            return Line(new_p1, new_p2)


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.get_perimeter()
        self.get_area()
    
    def get_perimeter(self):
        self.side1 = self.p1.distance_to(self.p2)
        self.side2 = self.p2.distance_to(self.p3)
        self.side3 = self.p3.distance_to(self.p1)
        self.perimeter = self.side1 + self.side2 + self.side3
    
    def get_area(self):
        s = self.perimeter / 2
        self.area = (s*(s-self.side1)*(s-self.side2)*(s-self.side3)) ** 0.5
    
    def is_right_triangle(self):
        v1 = Vector_2D.vec_btwn(self.p1, self.p2)
        v2 = Vector_2D.vec_btwn(self.p2, self.p3)
        v3 = Vector_2D.vec_btwn(self.p3, self.p1)
        return v1.is_ortho(v2) or v2.is_ortho(v3) or v3.is_ortho(v1)
    
    def translate(self, x, y):
        self.p1.translate(x, y)
        self.p2.translate(x, y)
        self.p3.translate(x, y)
    
    def reflect_x(self):
        self.p1.reflect_x()
        self.p2.reflect_x()
        self.p3.reflect_x()
    
    def reflect_y(self):
        self.p1.reflect_y()
        self.p2.reflect_y()
        self.p3.reflect_y()
    
    def centroid(self):
        '''l1 = Line(self.p1, self.p2.midpoint(self.p3))
        l2 = Line(self.p2, self.p1.midpoint(self.p3))
        centroid = l1.intersect(l2)'''
        v1 = Vector_2D.pos_vec(self.p1)
        v2 = Vector_2D.pos_vec(self.p2)
        v3 = Vector_2D.pos_vec(self.p3)
        v_centroid = v1.add(v2).add(v3).times(1/3)
        return Coord(v_centroid.x, v_centroid.y)
    
    def orthocenter(self):
        n1 = Vector_2D.vec_btwn(self.p2, self.p3).normal()
        l1 = Line_veceq(self.p1, n1)
        n2 = Vector_2D.vec_btwn(self.p3, self.p1).normal()
        l2 = Line_veceq(self.p2, n2)
        return l1.intersect(l2)
    
    def circumcenter(self):
        '''l1 = Line(self.p1, self.p2).perpendicular_bisector()
        l2 = Line(self.p2, self.p3).perpendicular_bisector()
        circumcenter = l1.intersect(l2)'''
        v1 = Vector_2D.vec_btwn(self.p1, self.p2)
        l1 = Line_veceq(self.p1.midpoint(self.p2), v1.normal())
        v2 = Vector_2D.vec_btwn(self.p2, self.p3)
        l2 = Line_veceq(self.p2.midpoint(self.p3), v2.normal())
        return l1.intersect(l2)
    
    def get_circumcircle(self):
        circumcenter = self.circumcenter()
        r = circumcenter.distance_to(self.p1)
        circumcircle = Circle(circumcenter, r)
        return circumcircle


class Quadratic:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    def __str__(self):
        output = "y = "
        if self.a == -1:
            output += "-"
        elif self.a != 1:
            output += str(self.a)
        output += "x^2"
        if self.b != 0:
            if self.b > 0:
                output += " + "
            else:
                output += " - "
            if abs(self.b) != 1:
                output += str(abs(self.b))
            output += "x"
        if self.c != 0:
            if self.c > 0:
                output += " + "
            else:
                output += " - "
            output += str(abs(self.c))
        return output
    
    def find_y(self, x_val):
        return self.a*(x_val**2) + self.b*x_val + self.c
    
    def y_intercept(self):
        return Coord(0, self.find_y(0))
    
    def roots(self):
        delta = self.b**2 - 4*self.a*self.c
        if delta < 0:
            return None
        elif delta == 0:
            root1 = (-self.b-(delta)**0.5) / (2*self.a)
            return [root1]
        else:
            root1 = (-self.b-(delta)**0.5) / (2*self.a)
            root2 = (-self.b+(delta)**0.5) / (2*self.a)
            return [root1, root2]
    
    def get_vertex(self):
        x_val = -self.b / (2*self.a)
        return Coord(x_val, self.find_y(x_val))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.r = radius
    
    def __str__(self):
        x0 = self.center.x
        y0 = self.center.y
        output = ""
        if x0 == 0:
            output += "x^2"
        elif x0 > 0:
            output += "(x-{})^2".format(x0)
        else:
            output += "(x+{})^2".format(-x0)
        output += " + "
        if y0 == 0:
            output += "y^2"
        elif y0 > 0:
            output += "(y-{})^2".format(y0)
        else:
            output += "(y+{})^2".format(-y0)
        output += " = {}^2".format(self.r)
        return output
    
    def perimeter(self):
        PI = 3.141592653589793
        return 2 * PI * self.r
    
    def area(self):
        PI = 3.141592653589793
        return PI * (self.r**2)


class Vector_2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "[{}, {}]".format(self.x, self.y)
    
    @staticmethod
    def pos_vec(point):
        return Vector_2D(point.x, point.y)
    
    @staticmethod
    def vec_btwn(start_p, end_p):  # vector from start point to end point
        x1, y1 = start_p.x, start_p.y
        x2, y2 = end_p.x, end_p.y
        return Vector_2D(x2-x1, y2-y1)
    
    def add(self, v):
        return Vector_2D(self.x+v.x, self.y+v.y)
    
    def subtract(self, v):
        return Vector_2D(self.x-v.x, self.y-v.y)
    
    def times(self, k):
        # k is a constant
        return Vector_2D(k*self.x, k*self.y)
    
    def dot(self, v):
        return self.x*v.x + self.y*v.y
    
    def is_ortho(self, v):
        return self.dot(v) == 0
    
    def normal(self):
        return Vector_2D(self.y, -self.x)


class Line_veceq:
    def __init__(self, point, vector):
        self.point = point
        self.direc = vector
    
    def __str__(self):
        return "[x, y] = [{}, {}] +t{}".format(self.point.x, self.point.y, self.dirc)
    
    def intersect(self, l):
        if self.direc.dot(l.direc.normal()) == 0:
            return None
        else:
            p1 = Coord(self.point.x+self.direc.x, self.point.y+self.direc.y)
            l1 = Line(self.point, p1)
            p2 = Coord(l.point.x+l.direc.x, l.point.y+l.direc.y)
            l2 = Line(l.point, p2)
            return l1.intersect(l2)

#%% Coordinates in general
P1 = Coord(-1, -5)
P2 = Coord(4, 7)
print("P1:", P1)
print("P2:", P2)
print("P1 is in quadrant:", P1.quadrant())
print("P2 is in quadrant:", P2.quadrant())
d = P1.distance_to(P2)
print("distance from P1 to P2:", d)
M = P1.midpoint(P2)
print("midpoint:", M)

P1.translate(1, -2)
print(P1)
print(P1.quadrant())

#%% Lines
P1 = Coord(-1, -5)
P2 = Coord(4, 7)
l1 = Line(P1, P2)
print(l1)
l2 = l1.perpendicular_bisector()
print(l2)
print(l2.intersect(l1))
print(l1.intersect(l2))
print(l1.slope*l2.slope)

#%% Triangles
P1 = Coord(0, 0)
P2 = Coord(-4, 0)
P3 = Coord(0, 3)
tri1 = Triangle(P1, P2, P3)
print("perimeter:", tri1.perimeter)
print("area:", tri1.area)
print(tri1.is_right_triangle())

print("centroid:", tri1.centroid())
print("orthocenter:", tri1.orthocenter())

circumcenter = tri1.circumcenter()
print("circumcenter:", circumcenter)
print(circumcenter.distance_to(tri1.p1))
print(circumcenter.distance_to(tri1.p2))
print(circumcenter.distance_to(tri1.p3))

circumcircle = tri1.get_circumcircle()
print(circumcircle)

#%% Quadratic functions
f1 = Quadratic(2, -1, -0.5)
# f1 = Quadratic(-2, -1, -0.5)

print("f1:", f1)
print("y-intercept:", f1.y_intercept())
print("roots:", f1.roots())
print("vertex:", f1.get_vertex())

#%% Circles
center = Coord(0, -2)
circle1 = Circle(center, 3)
print(circle1)
print("perimeter:", circle1.perimeter())
print("area:", circle1.area())
