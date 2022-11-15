from setuptools import setup, find_packages

setup(name='rubiks_cube_solver',
      version='0.0.0',
      install_requires=['gym_Rubiks_Cube @ git+https://github.com/lharri73/gym-Rubiks-Cube.git', 'torch', 'numpy'],
      packages=find_packages())
