import io
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md') as f:
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
