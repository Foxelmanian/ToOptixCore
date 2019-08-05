from .Geometry.Point import Point

class Node(Point):
    """ An node object with x,y,z and id

    """

    def __init__(self, node_id: int, x: float, y: float, z: float):

        super().__init__(x, y, z)
        self.__id = node_id
        self.__displacement_x = 0.0
        self.__displacement_y = 0.0
        self.__displacement_z = 0.0
        self.__temperature = 0.0

    def __str__(self):
        return ('ID: {} Coordinates: {}, {}, {} Displacements: {}, {}, {}'.format(
            self.__id, self.__x, self.__y, self.__z,
            self.__displacement_x, self.__displacement_y, self.__displacement_z))

    @property
    def id(self) -> int:
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
