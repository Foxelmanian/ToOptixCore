from .FEMPy.CCXPhraser import CCXPhraser, FRDReader, DATReader
from .FEMPy.CCXSolver import CCXSolver
from .DensityMaterial import DensityMaterial
from .TopologyOptimizer import TopologyOptimizer
from .Filter import ElementFilter
from .FEMPy.Geometry.STLPhraser import STL
from .FEMPy.Geometry.Solid import Solid
from .FEMPy.Geometry.Surface import Surface
import os
import numpy as np

use_trimesh_may_avi = False

if use_trimesh_may_avi:
    from mayavi import mlab
    import trimesh
    visualization_after_iteration = 5

    engine = mlab.get_engine()




class OptimizationController(object):

    def __init__(self, files, solution_types, reverse=False, type="seperated"):
        self.__reverse = reverse
        self.__type = type
        self.__files = files
        self.__solution_types = solution_types
        self.__solution_type_toOptix = {'heat': [], 'static':[]}
        self.__result_file_name = "stl_result"
        self.__volumina_ratio = 0.5
        if self.__reverse:
            self.__volumina_ratio = 1.0 - self.__volumina_ratio
        self.__material_sets = 20
        self.__penalty_exponent = 3
        self.__solver_path = "ccx.exe"
        self.__density_output = 0.5
        self.__result_path = "stl_results"
        self.__maximum_iterations = 100
        self.__run_counter = 0
        self.__change = 0.2
        self.__use_filter = True
        self.__plot_only_last_result = True
        self.__no_design_space = []
        self.__weight_factors = []
        self.__set_name = None

    def set_weight_factors(self, weight_factors):
        self.__weight_factors = weight_factors

    def set_no_design_element_set(self, set_name):
        self.__set_name = set_name

    def set_penalty_exponent(self, penalty):
        self.__penalty_exponent = penalty

    def set_result_path(self, path):
        self.__result_path = path

    def set_solver_path(self, path):
        self.__solver_path = path

    def plot_only_last_result(self, activate=False):
        self.__plot_only_last_result = activate

    def set_result_file_name(self, file_name: str):
        self.__result_file_name = file_name

    def use_filter(self, boolean_v):
        self.__use_filter = boolean_v

    def set_volumina_ratio(self, volumina_ratio:float):
        self.__volumina_ratio = volumina_ratio

    def set_maximum_iterations(self, maximum_iterations):
        self.__maximum_iterations = maximum_iterations

    def set_maximum_density_change(self, change):
        self.__change = change

    def set_number_of_material_sets(self, number_of_sets):
        self.__material_sets = number_of_sets

    def run(self):
        if not os.path.exists(self.__result_path):
            os.mkdir(self.__result_path)
        if self.__type == "seperated":
            for file, solution_type in zip(self.__files, self.__solution_types):
                self.__result_file_name = file[0:-4]

                if solution_type == "no_design_space":
                    fem_builder = CCXPhraser(file)
                    self.__no_design_space.extend(fem_builder.get_elements_by_set_name(None))

                if solution_type == "static" or solution_type == "heat":
                    # Create each time a new fem body for each type
                    fem_builder = CCXPhraser(file)
                    if self.__set_name != None:
                        print(f'No Design element set: {self.__set_name}')
                        self.__no_design_space.extend(fem_builder.get_elements_by_set_name(self.__set_name))
                    fem_body = fem_builder.get_fem_body()
                    ele_filter = ElementFilter(fem_body.get_elements())
                    ele_filter.create_filter_structure()
                    self.__optimization(file, fem_body, ele_filter, solution_type)
                    self.__run_counter += 1
        elif self.__type == "pareto":
            print("Pareto optimization started --> Only possible for equal meshes")
            for file, solution_type in zip(self.__files, self.__solution_types):
                if solution_type == "no_design_space":
                    fem_builder = CCXPhraser(file)
                    self.__no_design_space = fem_builder.get_elements_by_set_name(None)

            self.__pareto_optimization(self.__files, self.__solution_types, self.__weight_factors)
            self.__run_counter += 1



        else:
            print("No other mode is implemented: {}".format(self.__type))

    def __pareto_optimization(self, files, solution_types, weight_factors):

        # build up fem body with the first file
        file = files[0]
        fem_builder = CCXPhraser(file)
        fem_body = fem_builder.get_fem_body()
        ele_filter = ElementFilter(fem_body.get_elements())
        ele_filter.create_filter_structure()
        # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
        topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], self.__material_sets,
                                                         self.__penalty_exponent)
        current_density = len(fem_body.get_elements()) * [self.__volumina_ratio]

        for iteration in range(self.__maximum_iterations):
            print("[i] Iteration: {}".format(iteration))
            sensitivity_vectors = []
            for input_file_path, solution_type in zip(files, solution_types):
                print("[i] Pareto current type: {}  current file: {}".format(solution_type, input_file_path))
                if solution_type == "heat":
                    system_request = "NT"
                    sensitivity_request = "HFL"
                elif solution_type == "static":
                    system_request = "U"
                    sensitivity_request = "ENER"
                elif solution_type == "no_design_space":
                    continue
                else:
                    raise ValueError("Solution type not supported")
                sys_file_name = os.path.join(self.__result_path, system_request + "_system_optimization")
                sens_file_name = os.path.join(self.__result_path, sensitivity_request + "_sensitivity_optimization")
                ccx_topo_static = CCXSolver(self.__solver_path, input_file_path)

                # Calculix Result reader for FRD and DAT
                frd_reader = FRDReader(sys_file_name)
                dat_reader = DATReader(sens_file_name)
                dat_reader_2 = DATReader(sys_file_name)

                # Build up Optimizater
                optimizer = TopologyOptimizer(current_density, topology_optimization_material)
                optimizer.set_no_design_space(fem_body.get_elements(), self.__no_design_space)
                optimizer.set_maximum_density_change(self.__change)
                sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
                optimizer.set_compaction_ratio(self.__volumina_ratio)


                ############### start optimization

                ####optimizer.set_compaction_ratio(max(self.__volumina_ratio, 1.0 - 0.05 * iteration))
                # System calculation
                ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(),
                                             sorted_density_element_sets, sys_file_name, system_request)
                if solution_type == "heat":
                    frd_reader.get_temperature(fem_body.get_nodes())
                elif solution_type == "static":
                    frd_reader.get_displacement(fem_body.get_nodes())
                ccx_topo_static.run_topo_sens(fem_body.get_nodes(), sens_file_name, fem_body.get_elements(),
                                              sensitivity_request)

                # Sensitivity calculation
                if solution_type == "heat":
                    sensitivity_vector = dat_reader.get_heat_flux(fem_body.get_elements())
                elif solution_type == "static":
                    sensitivity_vector = dat_reader.get_energy_density(fem_body.get_elements())

                sensitivity_vectors.append(sensitivity_vector)

            # Perform pareto optimization
            #normalize by using median
            print("[i] number of different sensitivity vectors: {} normalized by median with weights {}".format(len(sensitivity_vectors), weight_factors))

            pareto_sensitivity_vector = np.zeros(len(sensitivity_vectors[0]))
            for sensitivity_vector, weight_factor in zip(sensitivity_vectors, weight_factors):
                sensitivity_vector = weight_factor * 1.0 /  np.median(sensitivity_vector) * np.array(sensitivity_vector)
                pareto_sensitivity_vector += sensitivity_vector


            # Change densitys
            print(pareto_sensitivity_vector)
            optimizer.change_density(pareto_sensitivity_vector)
            if self.__use_filter:
                print("########## FILTER IS USED")
                optimizer.filter_density(ele_filter)
            sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())

            # Select results which density is higher than a specific value
            res_elem = []
            for element_key in fem_body.get_elements():
                print(fem_body.get_elements()[element_key].get_density())
                if self.__reverse:
                    if fem_body.get_elements()[element_key].get_density() < self.__density_output:
                        res_elem.append(fem_body.get_elements()[element_key])
                else:
                    if fem_body.get_elements()[element_key].get_density() > self.__density_output:
                        res_elem.append(fem_body.get_elements()[element_key])

            if self.__plot_only_last_result:
                if iteration == self.__maximum_iterations - 1:

                    result_path = os.path.join(str(self.__result_path), str(self.__run_counter)
                                       + self.__result_file_name + "pareto" + str(iteration) + "_p_" +
                                       str(self.__penalty_exponent) + "_v_" + str(self.__volumina_ratio) +  '.stl')


                    self.__plot_result(iteration, res_elem, result_path)
            else:

                result_path = os.path.join(str(self.__result_path), str(self.__run_counter)
                                           + self.__result_file_name + "pareto" + str(iteration) + "_p_" +
                                           str(self.__penalty_exponent) + "_v_" + str(self.__volumina_ratio) + '.stl')
                self.__plot_result(iteration, res_elem, result_path)






    def __optimization(self, input_file_path, fem_body, ele_filter, solution_type):

        if solution_type == "heat":
            system_request = "NT"
            sensitivity_request = "HFL"

        elif solution_type == "static":
            system_request = "U"
            sensitivity_request = "ENER"
        else:
            raise ValueError("Solution type not supported")

        result_path_obj = os.path.join(str(self.__result_path), str(self.__run_counter)
                                   + self.__result_file_name.split("\\")[-1] + "_p_" +
                                   str(self.__penalty_exponent) + "_v_" + str(self.__volumina_ratio) + '.txt')

        if os.path.isfile(result_path_obj):
            os.remove(result_path_obj)
        obj_file = open(result_path_obj, 'w')

        obj_file.write('iteration, obj, obj_distro, p, volumina_ratio, distributed_density_ratio, full_mat_density_ratio \n')

        sys_file_name = os.path.join(self.__result_path, system_request + "_system_optimization")
        sens_file_name = os.path.join(self.__result_path, sensitivity_request + "_sensitivity_optimization")

        # Create a material according to the density rule (currently only 1 material is possible no multi material changing)
        topology_optimization_material = DensityMaterial(fem_body.get_materials()[0], self.__material_sets, self.__penalty_exponent)
        current_density = len(fem_body.get_elements()) * [self.__volumina_ratio]
        ccx_topo_static = CCXSolver(self.__solver_path, input_file_path)

        # Calculix Result reader for FRD and DAT
        frd_reader = FRDReader(sys_file_name)
        dat_reader = DATReader(sens_file_name)
        dat_reader_2 = DATReader(sys_file_name)

        # Build up Optimizater
        optimizer = TopologyOptimizer(current_density, topology_optimization_material)
        optimizer.set_no_design_space(fem_body.get_elements(), self.__no_design_space)
        optimizer.set_maximum_density_change(self.__change)
        sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())
        optimizer.set_compaction_ratio(self.__volumina_ratio)

        # Start optimization
        for iteration in range(self.__maximum_iterations):
            ####optimizer.set_compaction_ratio(max(self.__volumina_ratio, 1.0 - 0.05 * iteration))
            # System calculation
            ccx_topo_static.run_topo_sys(topology_optimization_material.get_density_materials(), sorted_density_element_sets, sys_file_name, system_request)
            if solution_type == "heat":
                frd_reader.get_temperature(fem_body.get_nodes())
                sensitivity_vector_obj = dat_reader_2.get_heat_flux(fem_body.get_elements())
            elif solution_type == "static":
                #dat_reader_2.get_displacement(fem_body.get_nodes())
                frd_reader.get_displacement(fem_body.get_nodes())
                sensitivity_vector_obj = dat_reader_2.get_energy_density(fem_body.get_elements())


            ccx_topo_static.run_topo_sens(fem_body.get_nodes(), sens_file_name, fem_body.get_elements(),  sensitivity_request)

            #Sensitivity calculation
            if solution_type == "heat":
                sensitivity_vector = dat_reader.get_heat_flux(fem_body.get_elements())
            elif solution_type == "static":
                sensitivity_vector = dat_reader.get_energy_density(fem_body.get_elements())

            if self.__use_filter:
                sensitivity_vector = optimizer.filter_sensitivity(ele_filter, sensitivity_vector)

            # Change densitys
            optimizer.change_density(sensitivity_vector)
            if self.__use_filter:
                optimizer.filter_density(ele_filter)

            sorted_density_element_sets = optimizer.get_element_sets_by_density(fem_body.get_elements())

            # Select results which density is higher than a specific value
            res_elem = []
            res_density = []
            for element_key in fem_body.get_elements():
                if self.__reverse:
                    if fem_body.get_elements()[element_key].get_density() < self.__density_output:
                        res_density.append(fem_body.get_elements()[element_key].get_density())
                        res_elem.append(fem_body.get_elements()[element_key])
                else:
                    if fem_body.get_elements()[element_key].get_density() > self.__density_output:
                        res_density.append(fem_body.get_elements()[element_key].get_density())
                        res_elem.append(fem_body.get_elements()[element_key])

            result_values = f'{iteration}, {sum(sensitivity_vector_obj)}, {sum(sensitivity_vector)}, {self.__penalty_exponent}, {self.__volumina_ratio}, {sum(res_density) / len(fem_body.get_elements())}, {len(res_density) / len(fem_body.get_elements())} \n'
            print(result_values)
            obj_file.write(result_values)


            if self.__plot_only_last_result:
                if iteration == self.__maximum_iterations -1:
                    result_path = os.path.join(str(self.__result_path), str(self.__run_counter)
                                       + self.__result_file_name + str(iteration) + "_p_" +
                                       str(self.__penalty_exponent) + "_v_" + str(self.__volumina_ratio) +  '.stl')
                    self.__plot_result(iteration, res_elem, result_path)
            else:
                result_path = os.path.join(str(self.__result_path), str(self.__run_counter)
                                           + self.__result_file_name.split("\\")[-1] + str(iteration) + "_p_" +
                                           str(self.__penalty_exponent) + "_v_" + str(self.__volumina_ratio) + '.stl')
                self.__plot_result(iteration, res_elem, result_path)
        obj_file.close()





    def __plot_result(self, iteration, res_elem, result_path):
        # Create the Surface for an stl output##



        topo_surf = Surface()
        topo_surf.create_surface_on_elements(res_elem)
        print("Number of result elements", len(res_elem))
        stl_file = STL(1)
        topo_part = Solid(1, topo_surf.triangles)
        stl_file.add_solid(topo_part)


        print("Exporting result elements: {}".format(len(res_elem)))
        stl_result_path = result_path
        print("Exporting stl result: {}".format(stl_result_path))
        if os.path.isfile(stl_result_path):
            os.remove(stl_result_path)
        stl_file.write(stl_result_path)

        if use_trimesh_may_avi:
            if iteration % visualization_after_iteration == visualization_after_iteration - 1:
                self.__plot_mayavi_function(stl_result_path)


    def __plot_mayavi_function(self, stl_result_path):
        try:
            s = engine._get_current_scene()
            mlab.close(s)
        except:
            pass
        triangle_mesh = trimesh.load(stl_result_path)
        mesh = {'x': triangle_mesh.vertices[:, 0].tolist(),
                     'y': triangle_mesh.vertices[:, 1].tolist(),
                     'z': triangle_mesh.vertices[:, 2].tolist(),
                     'faces': triangle_mesh.faces.tolist()}

        fig = mlab.figure(size=(600, 600), bgcolor=(1, 1, 1), fgcolor=(0.5, 0.5, 0.5))
        mlab.triangular_mesh(mesh['x'], mesh['y'], mesh['z'], mesh['faces'], colormap="bone", opacity=1.0)
        s = engine._get_current_scene()
        s.scene.save(stl_result_path[0:-3] + 'jpg')


        #if use_interactive:
        #    if iteration % interactive_visualization_after_iteration == 1:
        #        mlab.show()
