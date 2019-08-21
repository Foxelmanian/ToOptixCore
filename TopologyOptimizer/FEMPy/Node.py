

class Node(object):
    """ An node object with x,y,z and id

    """

    def __init__(self, node_id, x, y, z):
        self.__x = x
        self.__y = y
        self.__z = z
        self.__id = node_id
        self.__displacement_x = 0.0
        self.__displacement_y = 0.0
        self.__displacement_z = 0.0
        self.__temperature = 0.0


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


    def __str__(self):
        return ('ID: {} Coordinates: {}, {}, {} Displacements: {}, {}, {}'.format(
            self.__id, self.__x, self.__y, self.__z,
            self.__displacement_x, self.__displacement_y, self.__displacement_z))

    @property
    def id(self):
        return self.__id

    def set_displacement(self, x, y, z):
        self.__displacement_x = x
        self.__displacement_y = y
        self.__displacement_z = z

    def get_displacement(self):
        return [self.__displacement_x, self.__displacement_y, self.__displacement_z]

    def set_temperature(self, temperature):
        self.__temperature = temperature

    def get_temperature(self):
        return self.__temperature


if __name__ == "__main__":
    n1 = Node(1, 1.0, 2, 3)
    print(n1)
    n1.x = 3.0
