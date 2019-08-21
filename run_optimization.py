from TopologyOptimizer.OptimizationController import OptimizationController
import os
import json


def run_optimization(penal,  matSets, opti_type, sol_type,
                     weight_factors, max_iteration, vol_frac,
                     files, workDir='work', solverPath='ccx', 
                     cpus=2, no_design_set=None):

    with open('config.json') as json_data_file:
        data = json.load(json_data_file)
        # Import configuraiton data
        workDir = data['work_path']
        solverPath = data['ccx_path']
        cpus = data['cpus']
        print('Start topology otpimization')

    os.environ['OMP_NUM_THREADS'] = str(cpus)
    opti_controller = OptimizationController(files, sol_type, 
                                             reverse=False, 
                                             type=opti_type)
    opti_controller.set_maximum_iterations(max_iteration)
    opti_controller.set_penalty_exponent(penal)
    opti_controller.set_number_of_material_sets(matSets)
    opti_controller.set_solver_path(solverPath)
    opti_controller.set_weight_factors(weight_factors)
    opti_controller.plot_only_last_result(False)

    # Start the optimization
    opti_controller.set_result_file_name('stl_result' + str(vol_frac) + "__")
    opti_controller.set_result_path(workDir)
    opti_controller.set_volumina_ratio(vol_frac)
    opti_controller.set_no_design_element_set(no_design_set)
    opti_controller.run()


if __name__ == "__main__":
    # Optimization type --> seperated (combined is not implemented )
    opti_type = "seperated"
    sol_type = ["heat", "static"]

    static_job = os.path.join('test', 'TestData', 'StaticTestCase.inp')
    heat_job = os.path.join('test', 'TestData', 'HeatTransferTestCase.inp')
    files = [static_job, heat_job]
    vol_frac = 0.3
    penal = 3.0
    max_iteration = 5
    matSets = 10
    weight_factors = [1.0, 1.0]
    no_design_set = None
    run_optimization(penal,  matSets, opti_type, sol_type,
                     weight_factors, max_iteration, vol_frac,
                     files, no_design_set)
