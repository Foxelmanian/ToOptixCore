from typing import List


class Elasticity(object):

    def __init__(self, young_module: float, contraction: float, temperature: float):
        self.__temperature = temperature
        self.__contraction = contraction
        self.__young_module = young_module

    def get_temperature(self) -> float:
        return self.__temperature

    def get_contraction(self) -> float:
        return self.__contraction

    def get_young_module(self) -> float:
        return self.__young_module


class Conductivity(object):
    def __init__(self, conductivity: float, temperature: float):
        self.__temperature = temperature
        self.__conductivity = conductivity

    def get_temperature(self) -> float:
        return self.__temperature

    def get_conductivity(self) -> float:
        return self.__conductivity



class Material(object):

    def __init__(self, name: str):

        self.__name = name
        self.__elasticity = []
        self.__conductivity = []

    def add_elasticity(self, young_module=70000, contraction=0.3, temperature=0.0):
        self.__elasticity.append(Elasticity(young_module, contraction, temperature))

    def add_conductivity(self, conductivity=250, temperature=0.0):
        self.__conductivity.append(Conductivity(conductivity, temperature))

    def get_name(self):
        return self.__name

    def __str__(self):
        return ('Name: {} Elasticity entrys: {} Conductivity entrys: {} '.format(
            self.__name, len(self.__elasticity), len(self.__conductivity)))

    def get_elasticity(self) -> List[Elasticity]:
        return self.__elasticity

    def get_conductivity(self) -> List[Conductivity]:
        return self.__conductivity


