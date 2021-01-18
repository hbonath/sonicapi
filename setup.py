import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="sonicapi",
    version="0.1.0",
    description="Python3 Module to interact with the SonicWall® SonicOS API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hbonath/sonicapi",
    author="Henry Bonath",
    author_email="henry@thebonaths.com",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["sonicapi"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "sonicapi=sonicapi.__main__:main",
        ]
    },
)
