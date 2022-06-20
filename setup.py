from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mmd_dilated",
    version="0.0.1",
    author="Ryan D'Orazio",
    author_email="dorazio.rf@gmail.com",
    description="An implementation of MMD with dilated entropy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryan-dorazio/mmd_dilated",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
            "pygambit==16.0.2",
            "open-spiel==1.1.0",
            "numpy>=1.22.3",
            "scipy>=1.8.0",
            "matplotlib >= 2.0.0",
            "tqdm>=4.64.0"
        ],
)