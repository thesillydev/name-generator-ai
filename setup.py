from requests import get
from setuptools import setup
    
setup(
    name='name-generator',
    version='1.0.0',
    description='An simple open source name generator.',
    author='A Weirdo Dev',
    python_requires='>=3.6.0',
    py_modules=['name_creator'],
    install_requires=['tensorflow', 'numpy'],
    license='MIT'
)
