
# Topology optimization with ToOptix


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixCore/blob/master/Images/StaticLoadCaseTwoRectangle.png" width="100%">
</p>


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixCore/blob/master/Images/HeatLoadCaseTwoRectangle.png" width="100%">
</p>


<p align="center">
  <img src="https://github.com/DMST1990/ToOptixCore/blob/master/Images/QuadraticPlateLoadCase.png" width="100%">
</p>

<p align="center">
  <img src="https://github.com/DMST1990/ToOptixCore/blob/master/Images/NoDesignSpace.png" width="100%">
</p>




## Current version
- Only 3D-FEM support
- Heat Transfer
- Static load case
- Material will change only in young module and conductivity
- Filter selects only the element around the filter object

## Installation
- Install python 3.xx
- Download ToOptix

### General information
- Start this program in a user directory so Blender should be for example on the desktop 
- If you want to start Tooptix in "C:Programms\Blender Foundation ..." you need administrator rights (not reccomended)
- So i would suggest you should take a copy of blender and then use it on the desktop or some other user access folder
- (Optional) create a environment variable for Calculix (ccx)
- Test at first the two example files TwoRectanglesStruc.inp and TwoRectanglesTherm.inp





### Python Usuage
- Check if import statement of run_optimization.py is: 
from TopologyOptimizer.OptimizationController import OptimizationController 
- Open the folder with pycharm and just start your optimization
- Use the Folder ToOptix_Python

Example no design space with file:

```python,example

from run_optimization import run_optimization

cpus = 4

# Optimization type --> seperated (combined is only in beta )

opti_type = "seperated"
# no design space is used until redefinition
sol_type = ["no_design_space", "static"]
files = ["no_design_space.inp", "testinp\Cylinder_Mesh.inp"]
max_iteration = 20
vol_frac = 0.3
penal = 3.0
matSets = 10
weight_factors = [3.0]
workDir = "work"
solverPath = "ccx"
run_optimization(penal,  matSets, opti_type, sol_type,
                                      weight_factors, max_iteration, vol_frac,
                                      files, workDir, solverPath, cpus)
```
Example no design space with element set and several iterations:

- The element set created by FreeCAD will be named as follow
'SolidMaterialSolid'  'SolidMaterial001Solid'  'SolidMaterial002Solid'  
You can specify the non design space by another material definition. So that SolidMaterialSolid is free and SolidMaterial001Solid is a non design space.
- You can specify your own non design space by creating a element set in '.inp' file and use the name of the element set as the non design space definition

```python,example

#### No design space

from run_optimization import run_optimization

# Optimization type --> seperated (combined is only in beta )
cpus = 6
opti_type = "seperated"
sol_type = ["static"]
files = ["PlateWithNoDesignSpaceFine.inp"]

for vol_frac in [0.4, 0.6]:
    for penal in [3.0]:
        max_iteration = 100
        matSets = 20
        weight_factors = [1.0]
        workDir = "work"
        solverPath = "ccx"
        no_design_set = 'SolidMaterial001Solid'
        run_optimization(penal,  matSets, opti_type, sol_type,
                                              weight_factors, max_iteration, vol_frac,
                                              files, workDir, solverPath, cpus, no_design_set)


``` 

### Blender AddOn
Location of the Blender Addon
[Blender Addon](https://github.com/DMST1990/ToOptixBlenderAddon)


### FreeCAD Macro
Location of the Blender Addon
[FreeCAD Addon](https://github.com/DMST1990/ToOptixFreeCADAddon)

## Output
- STL File in a specific folder for every optimizaiton step
- Rendered Pictures of the result



