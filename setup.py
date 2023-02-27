from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='Name Generator AI',
   version='1.0',
   description='A useful module',
   license="MIT",
   long_description=long_description,
   author='Yan Antônio',
   packages=['name_generator'],  #same as name
   install_requires=['tensorflow', 'numpy']
)
