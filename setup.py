from setuptools import setup, find_packages

setup(
    name="displacement-visualization",
    version="0.1.0",
    packages=find_packages(),
    python_requires= "~=3.11",
    install_requires=[
        "h5py==3.8.0",
        "numpy==1.24.2",
        "matplotlib==3.7.1",
        "geopy==2.3.0",
        "rasterio==1.3.6",
        "geopandas==0.12.2",
    ],
    author="Egehan Vardar",
    author_email="egehanvardar@gmail.com",
    description="A library for processing and visualizing displacement data from earthquakes or other geophysical events",
    license="MIT",
)
