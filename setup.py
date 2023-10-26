#!/usr/bin/env python3
"""
Auxilary script to help sweep over design parameters in Dymola models using Python.

A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
DOCLINES = (__doc__ or '').split("\n")

from setuptools import setup, find_packages
import pathlib
import sys

# Python supported version checks. Keep right after stdlib imports to ensure we
# get a sensible error for older Python versions
if sys.version_info[:2] < (3, 8):
    raise RuntimeError("Python version >= 3.8 required.")

here = pathlib.Path(__file__).parent.resolve()
with (here/"README.md").open(mode='r', encoding="utf-8") as fh:
    long_description = fh.read()


setup(
        name='Pymola',
        version=".".join(("1", "0", "0")),
        description='Python + Dymola = Pymola',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://mohammadodeh.com',
        author='Mohammad Odeh',
        author_email='contact@mohammadodeh.com',
        keywords=["fowt", "modeling", "simulation", "technical analysis", "python3"],
        classifiers=[  # Optional
                # Check: http://pypi.python.org/pypi?%3Aaction=list_classifiers
                # How mature is this project? Common values are
                # "Development Status :: 1 - Planning",
                # "Development Status :: 2 - Pre - Alpha",
                # "Development Status :: 3 - Alpha",
                # "Development Status :: 4 - Beta",
                # "Development Status :: 5 - Production / Stable",
                "Development Status :: 6 - Mature",
                "Development Status :: 7 - Inactive",
                # Indicate who your project is intended for
                "Intended Audience :: Developers",
                "Intended Audience :: Education",
                "Intended Audience :: Science/Research",
                "Intended Audience :: Other Audience",
                # Pick your license as you wish
                "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                # Natural language the script was written in
                "Natural Language :: English",
                # Compatible operating systems
                "Operating System :: MacOS",
                "Operating System :: Unix",
                "Operating System :: Microsoft :: Windows",
                # Specify the Python versions you support here. In particular, ensure
                # that you indicate you support Python 3. These classifiers are *not*
                # checked by 'pip install'. See instead 'python_requires' below.
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3.11",
                "Programming Language :: Python :: 3 :: Only",
                # Topic of project
                "Topic :: Scientific/Engineering",
                "Topic :: Scientific/Engineering :: Information Analysis",
                "Topic :: Scientific/Engineering :: Mathematics",
                "Topic :: Scientific/Engineering :: Physics",
                ],
        package_dir={"": "pymola"},
        packages=find_packages( where="pymola",
                                include=[ '../eggs' ] ),
        include_package_data=True,
        python_requires=">=3.8, <4",
        install_requires=[
                'matplotlib',
                'numpy',
                'pandas',
                'scipy',
                'wxpython'
                ],
        extras_require={
                "GUI": ['fmpy==0.3.18',
                        'opencv-python-headless==4.8.1.78',
                        'PyQt5==5.15.10',
                        'pyqtgraph==0.13.3',
                        'PyQtWebEngine==5.15.6'
                        ],
                },
        )
