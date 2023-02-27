from requests import get
from setuptools import setup

here = get('https://raw.githubusercontent.com/Yan908/name-generator-ai/main/README.md')

with open(here) as f:
    long_description = '\n' + f.read()
    
setup(
    name='name-generator',
    version='1.0.0',
    description='An simple open source name generator.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='A Weirdo Dev',
    python_requires='>=3.6.0',
    py_modules=['name_creator'],
    install_requires=['tensorflow', 'numpy'],
    license='MIT'
)
