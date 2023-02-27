from requests import get
from setuptools import setup, find_packages
    
setup(
    name='name-generator',
    version='1.0.0',
    description='An simple open source name generator.',
    author='A Weirdo Dev',
    python_requires='>=3.6.0',
    packages=find_packages(),
    install_requires=['name-generator-ai @ https://github.com/Yan908/name-generator-ai.git'],
    license='MIT'
)
