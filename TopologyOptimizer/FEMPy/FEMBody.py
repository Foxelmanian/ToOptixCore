from .Node import Node
from .Element import Element
from .Material import Material
from typing import Dict, List


class FEMBody(object):
    """ Body of an FEM object with elements nodes and material data.

    """

    def __init__(self, name: str, nodes: Dict[int, Node], elements:  Dict[int, Element], material: Material):
        self.__nodes = nodes
        self.__elements = elements
        self.__materials = [material]
        self.__name = name

    def get_nodes(self) -> Dict[int, Node]:
        return self.__nodes

    def get_materials(self) -> List[Material]:
        return self.__materials

    def set_materials(self, materials: List[Material]):
        self.__materials = materials

    def get_elements(self) -> Dict[int, Element]:
        return self.__elements

    def __str__(self):
        return ('Name: {} Nodes: {} Elements: {} Materials: {}'.format(
            self.__name, len(self.__nodes), len(self.__elements), len(self.__materials)))




