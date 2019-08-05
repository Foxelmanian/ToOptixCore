from .Element import Element
from typing import List

class ElementSet(object):

    def __init__(self, name: str, elements: List[Element]):
        self.__name = name
        self.__elements = elements

    def get_name(self) -> str:
        return self.__name

    def get_elements(self) -> List[Element]:
        return self.__elements
