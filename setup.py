from setuptools import setup

setup(
   name='ToOptix',
   version='1.0',
   description='OptimizationModule for Topology',
   author='Martin Denk',
   author_email='denk.martin1990@gmail.com',
   packages=['ToOptix', 'ToOptix.FEMPy', 'ToOptix.FEMPy.Geometry'],  
   install_requires=['numpy'], #external packages as dependencies alternative --> Trimesh and Mayavi if true
   )


