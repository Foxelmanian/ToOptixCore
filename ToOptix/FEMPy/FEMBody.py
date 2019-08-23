from .Node import Node
from .Element import Element
from .Material import Material


class FEMBody(object):
    """ Body of an FEM object with elements nodes and material data.

    """

    def __init__(self, name, nodes, elements, material):
        self.__nodes = nodes
        self.__elements = elements
        self.__materials = [material]
        self.__name = name

    def get_nodes(self):
        return self.__nodes

    def get_materials(self):
        return self.__materials

    def set_materials(self, materials):
        self.__materials = materials

    def get_elements(self):
        return self.__elements

    def __str__(self):
        return ('Name: {} Nodes: {} Elements: {} Materials: {}'.format(
            self.__name, len(self.__nodes), len(self.__elements), len(self.__materials)))




