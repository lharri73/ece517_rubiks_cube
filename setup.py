from setuptools import setup, find_packages

setup(name='rubiks_cube_solver',
      version='0.0.0',
      install_requires=['gym', 'torch', 'numpy'],
      packages=find_packages())
