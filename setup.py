from setuptools import setup, find_packages

setup(
    name="displacement-visualization",
    version="0.1.0",
    packages=find_packages(),
    python_requires= "~=3.11",
    install_requires=[
        "h5py==3.16.0",
        "numpy==2.4.6",
        "matplotlib==3.11.2",
        "geopy==2.5.0",
        "rasterio==1.4.4",
        "geopandas==1.2.0",
    ],
    author="Egehan Vardar",
    author_email="egehanvardar@gmail.com",
    description="A library for processing and visualizing displacement data from earthquakes or other geophysical events",
    license="MIT",
)
