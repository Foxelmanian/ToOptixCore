from .Triangle import Triangle
from typing import List

class Solid(object):
    """ A solid structure defined by triangles

    :param id(int): Solid ID
    :param triangles(list(Triangle)): List of all Triangles

    Example for creating a Tetrahedral-Solid out of triangles

    >>> t1 = Triangle(1, p1, p2, p3)
    >>> t2 = Triangle(2, p2, p3, p4)
    >>> t3 = Triangle(3, p3, p4, p1)
    >>> t4 = Triangle(4, p2, p4, p1)
    >>> s1 = Solid(1, [t1, t2, t3, t4])
    """

    def __init__(self, id: int, triangles: List[Triangle]):
        self.__id = id
        self.__triangles = triangles

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def triangles(self):
        return self.__triangles

    @triangles.setter
    def triangles(self, Triangles):
        if len(Triangles) == 0:
            raise ValueError ("No triangle were found for solid ", self.__id)