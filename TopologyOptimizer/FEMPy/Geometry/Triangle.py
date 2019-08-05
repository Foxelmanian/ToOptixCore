from .Point import Point
from typing import List
import numpy as np

class Triangle(object):
    """ Triangle which is defined by 3 points

    :param id(int): Triangle ID
    :param points(list(Point)): 3 Points for the triangle
    :param normal(list(float)): Normal-Vector of plane


    Example for creating a tirangle object

    >>> p1 = Point(1.0, 1.0, 1.0)
    >>> p2 = Point(2.0, 2.0, 2.0)
    >>> p3 = Point(1.0, 2.0, 0.0)
    >>> t1 = Triangle(1, [p1, p2, p3])
    """

    def __init__(self,ID=None, Points=[], Face_ids=[]):
        self.__points = Points
        self.__face_ids = Face_ids
        if len(Points) == 3:
            self.__normal = self.normal_vec(Points)
        else:
            self.__normal = None
        self.__id = ID

    @staticmethod
    def normal_vec(points):
        p1 = points[0]
        p2 = points[1]
        p3 = points[2]
        # Defining two vectors and using cross product for normal vector
        p1_p2 = [p2.x - p1.x, p2.y - p1.y, p2.z - p1.z]
        p1_p3 = [p3.x - p1.x, p3.y - p1.y, p3.z - p1.z]

        norm_vec = np.cross(p1_p2, p1_p3)

        norm_vec = 1.0 / np.linalg.norm(norm_vec) * norm_vec

        return norm_vec

    @property
    def face_ids(self):
        return self.__face_ids

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    @property
    def normal(self):
        return self.__normal

    @normal.setter
    def normal(self, normal):
        self.__normal = normal