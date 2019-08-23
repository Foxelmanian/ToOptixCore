from .Element import Element

class ElementSet(object):

    def __init__(self, name, elements):
        self.__name = name
        self.__elements = elements

    def get_name(self):
        return self.__name

    def get_elements(self):
        return self.__elements
