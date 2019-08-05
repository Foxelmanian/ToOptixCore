from typing import List
import os

class CCXSolver(object):

    def __init__(self, solver_path: str, input_deck_path: str):
        self.__solver_path = solver_path
        self.__input_path = input_deck_path
        self.__2D_case = False

    def run_topo_sys(self, topo_materials, topo_element_sets, run_path, output):
        self.__run_topo_system(topo_materials, topo_element_sets, run_path, output)

    def run_topo_sens(self, boundary_nodes, run_path, elements, output="ENER", ):
        tmp_run_file = run_path + ".inp"
        run_file = open(tmp_run_file, "w")
        run_file.write("*** Topology optimization input deck \n")
        input_deck = open(self.__input_path, "r")
        ignore_element_output = False
        element_output_was_set = False
        ignore_boundary = False
        for line in input_deck:
            if "*STEP" in line.upper():
                run_file.write("*ELSET, ELSET=TOPO_ALL_ELEMENTS_DMST\n")
                counter_tab = 0
                for element_id in elements:
                    counter_tab += 1
                    if counter_tab == 8:
                        run_file.write("\n")
                        counter_tab = 0
                    run_file.write(str(elements[element_id].get_id()) + ",")

                run_file.write("\n")
                run_file.write("*BOUNDARY\n")
                for node_id in boundary_nodes:
                    node = boundary_nodes[node_id]
                    if output == "ENER":
                        disp = node.get_displacement()
                        run_file.write(str(node.id) + ", 1, 1, " + str(disp[0]) + "\n")
                        run_file.write(str(node.id) + ", 2, 2, " + str(disp[1]) + "\n")
                        run_file.write(str(node.id) + ", 3, 3, " + str(disp[2]) + "\n")
                    elif output == "HFL":
                        run_file.write(str(node.id) + ", 11, 11," + str(node.get_temperature()) + "\n")

            if "*" in line.upper() and "**" not in line.upper():
                ignore_boundary = False
            if "*BOUNDARY" in line.upper():
                ignore_boundary = True
            if ignore_boundary:
                continue

            if ignore_element_output:
                if len(line) >= 2:
                    if line[0] == "*" and line[0:2] != "**":
                        ignore_element_output = False

            if ignore_element_output:
                continue


            if "*EL PRINT" in line.upper():
                element_output_was_set = True
                run_file.write("*EL PRINT, ELSET=TOPO_ALL_ELEMENTS_DMST\n")
                run_file.write(output + "\n")
                ignore_element_output = True
                continue

            if "*END STE" in line.upper():
                if not element_output_was_set:
                    run_file.write("*EL PRINT, ELSET=TOPO_ALL_ELEMENTS_DMST\n")
                    run_file.write(output + "\n")


            run_file.write(line)
        input_deck.close()
        run_file.close()
        print(self.__solver_path, run_path)
        os.system(self.__solver_path + " " + run_path)


    def __run_topo_system(self, topo_materials, topo_element_sets, run_path, output="U"):
        tmp_run_file = run_path + ".inp"
        run_file = open(tmp_run_file, "w")
        run_file.write("*** Topology optimization input deck \n")
        input_deck = open(self.__input_path, "r")
        ignore_node_output = False
        node_output_was_set = False

        mat_iter = 0
        for line in input_deck:
            if "*STEP" in line.upper():
                for material in topo_materials:
                    mat_iter += 1
                    run_file.write("*MATERIAL, name=" + str(material.get_name()) + "\n")
                    run_file.write("*ELASTIC \n")
                    for elasticity in material.get_elasticity():
                        run_file.write('{}, {}, {} \n'.format(elasticity.get_young_module(),
                                                              elasticity.get_contraction(),
                                                              elasticity.get_temperature()))

                    density = mat_iter / len(topo_materials) * 7.900e-09
                    density = 7.900e-09

                    run_file.write("*DENSITY \n "+ str(density) + " \n")

                    run_file.write("*CONDUCTIVITY  \n")
                    for conductivity in material.get_conductivity():
                        run_file.write('{},{}  \n'.format(conductivity.get_conductivity(),
                                                          conductivity.get_temperature()))

                for element_set in topo_element_sets:
                    if len(element_set.get_elements()) <= 0:
                        continue
                    run_file.write("*ELSET,ELSET=" + element_set.get_name() + "\n")
                    tmp_counter = 0
                    for element in element_set.get_elements():
                        tmp_counter += 1
                        if tmp_counter == 8:
                            run_file.write("\n")
                            tmp_counter = 0
                        run_file.write(str(element.get_id()) + ",")
                    run_file.write("\n")

                for ii in range(len(topo_element_sets)):
                    if len(topo_element_sets[ii].get_elements()) <= 0:
                        continue
                    set_name = topo_element_sets[ii].get_name()
                    mat_name = topo_materials[ii].get_name()
                    if self.__2D_case:
                        run_file.write("*SHELL SECTION,ELSET=" + str(set_name) + ",material=" + str(mat_name) + "\n")
                        run_file.write("1 \n")
                    else:
                        run_file.write("*SOLID SECTION,ELSET=" + str(set_name) + ",material=" + str(mat_name) + "\n")
            if "*SOLID SECTION" in line.upper():
                continue

            if "SHELL SECTION" in line.upper():
                continue

            if ignore_node_output:
                if len(line) >= 2:
                    if line[0] == "*" and line[0:2] != "**":
                        ignore_node_output = False

            if ignore_node_output:
                continue
            if "*NODE FILE" in line.upper():
                node_output_was_set = True
                run_file.write("*NODE FILE\n")
                run_file.write(output + "\n")
                ignore_node_output = True
                continue
            if "*END STE" in line.upper():
                if not node_output_was_set:
                    run_file.write("*NODE FILE\n")
                    run_file.write( output + "\n")

                run_file.write("*EL PRINT, ELSET=Evolumes\n")
                run_file.write('ENER' + "\n")

            run_file.write(line)
        input_deck.close()
        run_file.close()
        print(self.__solver_path, run_path)
        os.system(self.__solver_path + " " + run_path)













