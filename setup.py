from setuptools import setup

setup(
   name='ToOptix',
   version='1.0',
   description='OptimizationModule for Topology',
   author='Martin Denk https://orcid.org/0000-0002-0204-3608',
   url='https://github.com/DMST1990/ToOptix',
   packages=['ToOptix', 'ToOptix.FEMPy', 'ToOptix.FEMPy.Geometry'],  
   install_requires=['numpy'], #external packages as dependencies alternative --> Trimesh and Mayavi if true
   )


