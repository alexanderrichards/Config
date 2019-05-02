"""Setuptools Module."""
from setuptools import setup, find_packages

setup(
    name="config",
    version="0.1",
    packages=find_packages(),
    install_requires=['configparser',
                      'singleton @ git+git://github.com/alexanderrichards/Singleton.git'],

    # metadata for upload to PyPI
    author="Alexander Richards",
    author_email="a.richards@imperial.ac.uk",
    description="Configuration system based on configparser",
    license="MIT",
    keywords="config",
    url="https://github.com/alexanderrichards/Config"
)
