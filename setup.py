import pip
from setuptools import setup, find_packages

setup(
    name='PyMesaHandler',
    version='0.2.1',
    packages=find_packages(exclude=["*test", "dist", "build", "venv", "*egg-info*"]),
    url='https://github.com/muma7490/PyMesaHandler',
    license='MIT',
    author='Marco Müllner',
    author_email='muellnermarco@gmail.com',
    description='An easy way to handle Mesa using Python',
)
