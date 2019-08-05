from typing import List, Dict
from .FEMPy.Element import Element
from .FEMPy.ElementSet import ElementSet
from . import DensityMaterial
from .Filter import ElementFilter
import numpy as np

class TopologyOptimizer(object):

    def __init__(self, density: List[float], density_material: DensityMaterial, compaction_ratio=0.3):
        self.__system_answer = []
        self.__system_sensitivity = []
        self.__current_density = np.array(density)
        self.__next_density = np.array(density)
        self.__density_material = density_material
        self.__memory_size = 2
        self.__sensitivity_sets = []
        self.__density_sets = []
        self.__convergence_max = 0.01
        self.__max_change = 0.1
        self.__compaction_ratio = compaction_ratio
        self.__no_design_space = []

    def set_no_design_space(self, elements: Dict[int, Element], no_design_space_elements):
        print("No design space is active with {} elements".format(len(no_design_space_elements)))
        counter = -1
        for element_key in elements:
            counter += 1
            if element_key in no_design_space_elements:
                self.__no_design_space.append(counter)

    def set_maximum_density_change(self, max_change):
        self.__max_change = max_change

    def get_current_density(self):
        return self.__current_density

    def set_compaction_ratio(self, compaction_ratio):
        self.__compaction_ratio = compaction_ratio

    def get_element_sets_by_density(self, elements: Dict[int, Element]) -> List[ElementSet]:
        element_sets = []
        for i in range(self.__density_material.get_steps()):
            element_sets.append([])
        counter = 0
        for key in elements:
            elset_number = (self.__density_material.get_steps() - 1) * self.__current_density[counter]
            elements[key].set_density(self.__current_density[counter])
            element_sets[int(elset_number)].append(elements[key])
            counter += 1
        element_sets_ob = []
        counter = 1
        for element_id_set in element_sets:
            eset = ElementSet("topoElementSet" + str(counter), element_id_set)
            element_sets_ob.append(eset)
            counter += 1
        return element_sets_ob

    def filter_sensitivity(self, element_filter, sensitivity):
        return element_filter.filter_element_properties(sensitivity * self.__current_density)

    def filter_density(self, element_filter: ElementFilter):
        self.__current_density = element_filter.filter_element_properties(self.__current_density)

    def change_density(self, sensitivity):
        sensitivity = np.array(self.__current_density)**(self.__density_material.get_penalty_exponent() - 1) * np.array(sensitivity)
        if min(sensitivity) <= 0:
            sensitivity += abs(np.min(sensitivity))+ 0.1
        self.__sensitivity_sets.append(sensitivity)
        self.__density_sets.append(self.__current_density)
        if len(self.__sensitivity_sets) > self.__memory_size:
            self.__sensitivity_sets.pop(0)
            self.__density_sets.pop(0)
        weight = 0
        for sensitivity_in_memory in self.__sensitivity_sets:
            if weight == 0:
                sensitivity = sensitivity_in_memory
            else:
                sensitivity += sensitivity_in_memory
            weight += 1
        """
        weight = 0
        for density_in_memory in self.__density_sets:
            if weight == 0:
                self.__current_density = density_in_memory * np.exp(weight)
            else:
                self.__current_density += density_in_memory * np.exp(weight)
            weight += 1
        self.__current_density = self.__current_density * 1.0 / sum_weight
        """
        print("length sens sets memory: ", len(self.__sensitivity_sets))

        l_upper = max(sensitivity)
        l_lower = min(sensitivity)
        # Method of moving asympthotes
        while(abs(l_upper - l_lower) > (l_upper * self.__convergence_max)):
            l_mid = 0.5 * (l_lower + l_upper)
            # Values between 0 and 1
            # SIMP method
            self.__next_density = np.maximum(0.0,
                                             np.maximum(self.__current_density - self.__max_change,
                                                        np.minimum(1.0,
                                                                   np.minimum(self.__current_density + self.__max_change,
                                                                   self.__current_density * (sensitivity / l_mid) ** 0.5))))
            # BESO-Method
            #new_design_variable = np.maximum(0.00001, np.sign(sensitivity - l_mid))


            for id in self.__no_design_space:
                self.__next_density[id] = 1.0

            if np.mean(self.__next_density) - self.__compaction_ratio > 0.0:
                l_lower = l_mid
            else:
                l_upper = l_mid
        print("##---- MEAN DENSTIY: " + str(np.mean(self.__next_density)))
        self.__current_density = self.__next_density










