class Point(object):
    """ Point with attributes

    :param id(int): Point ID
    :param x(float): x-Coordinate
    :param y(float): y-Coordinate
    :param z(float): z-Coordinate


    Example for creating a tirangle object

    >>> p1 = Point(1.0, 1.0, 1.0)
    """

    def __init__(self, x:float, y:float, z:float):
        self.__x = x
        self.__y = y
        self.__z = z



    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def z(self):
        return self.__z

    @z.setter
    def z(self, z):
        self.__z = z