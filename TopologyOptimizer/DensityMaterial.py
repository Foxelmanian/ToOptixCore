from .FEMPy.Material import Material
from typing import List

class DensityMaterial(object):

    def __init__(self, material: Material, steps: int, penalty_exponent: float):
        self.__material = material
        self.__steps = steps
        self.__penalty = penalty_exponent

    def get_penalty_exponent(self) -> float:
        return self.__penalty

    def get_steps(self) -> int:
        return self.__steps

    def get_density_materials(self) -> List[Material]:
        density_materials = []
        for i in range(self.__steps):
            density_mat = Material("topo_material" + str(i + 1))
            for basic_conductivity in self.__material.get_conductivity():
                conductivity_reduced = (float(i + 1) / float(self.__steps)) ** self.__penalty * \
                                       basic_conductivity.get_conductivity()
                density_mat.add_conductivity(conductivity_reduced, basic_conductivity.get_temperature())

            for basic_elasticity in self.__material.get_elasticity():
                young_module_reduced = (float(i + 1) / float(self.__steps)) ** self.__penalty * \
                                       basic_elasticity.get_young_module()
                #contraction_reduced = (float(i + 1) / float(self.__steps)) ** self.__penalty * \
                #                      basic_elasticity.get_contraction()
                contraction_reduced = basic_elasticity.get_contraction()
                density_mat.add_elasticity(young_module_reduced, contraction_reduced)

            density_materials.append(density_mat)
        return density_materials






