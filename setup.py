import setuptools
import os


with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join("spherical_coordinates", "version.py")) as f:
    txt = f.read()
    last_line = txt.splitlines()[-1]
    version_string = last_line.split()[-1]
    version = version_string.strip("\"'")

setuptools.setup(
    name="spherical_coordinates",
    version=version,
    description=("This is spherical_coordinates."),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/cherenkov-plenoscope/spherical_coordinates",
    author="Sebastian A. Mueller",
    author_email="Sebastian A. Mueller@mail",
    packages=[
        "spherical_coordinates",
    ],
    package_data={"spherical_coordinates": []},
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ],
)
