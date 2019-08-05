from typing import List
from .Node import Node

"""


"""


class Element(object):
    """ This class is used for creating a element of FEM
    """

    def __init__(self, element_id: int, nodes: List[Node]):
        self.__nodes = nodes
        self.__element_id = element_id
        self.__strain_energy = 0.0
        self.__heat_flux = 0.0
        self.__hflux_x = 0.0
        self.__hflux_y = 0.0
        self.__hflux_z = 0.0
        self.__density = 0.0
        self.__x_center = 0.0
        self.__y_center = 0.0
        self.__z_center = 0.0


        self.__calculate_element_center()


    def set_heat_flux_xyz(self, flx_x, flx_y, flx_z):
        self.__hflux_x = flx_x
        self.__hflux_y = flx_y
        self.__hflux_z = flx_z

    def get_heat_flux_xyz(self):
        return [self.__hflux_x, self.__hflux_y, self.__hflux_z]

    def set_heat_flux(self, hflx):
        self.__heat_flux = hflx

    def get_heat_flux(self):
        return self.__heat_flux

    def get_id(self) -> int:
        return self.__element_id

    def set_strain_energy(self, strain_energy):
        self.__strain_energy = strain_energy

    def get_strain_energy(self):
        return self.__strain_energy

    def get_nodes(self):
        return self.__nodes

    def get_density(self):
        return self.__density

    def set_density(self, density):
        self.__density = density

    def __calculate_element_center(self):
        count = 0
        x_center = 0.0
        y_center = 0.0
        z_center = 0.0

        for node in self.__nodes:
            count += 1
            x_center += node.x
            y_center += node.y
            z_center += node.z
        self.__x_center = x_center / count
        self.__y_center = y_center / count
        self.__z_center = z_center / count

    def get_x_center(self):
        return self.__x_center

    def get_y_center(self):
        return self.__y_center

    def get_z_center(self):
        return self.__z_center







