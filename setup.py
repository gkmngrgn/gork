import pathlib

import setuptools

long_description = pathlib.Path("README.md").read_text()

setuptools.setup(
    name="gork",
    version="0.0.1",
    author="Gökmen Görgen",
    author_email="gkmngrgn@gmail.com",
    description="CLI based 8bit image pixelator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gkmngrgn/gork",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
