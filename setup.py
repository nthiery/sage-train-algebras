# -*- encoding: utf-8 -*-
from setuptools import setup  # type: ignore

setup(
    name="sage-train-algebras",
    version="0.1",
    description="",
    url='https://github.com/nthiery/sage-train-algebras',
    author="Nicolas M. Thiéry et al.",
    author_email="Nicolas.Thiery@u-psud.fr",
    license="GPLv3+",  # This should be consistent with the LICENCE file
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
    ],
    packages=["train_algebras"],
    # cmdclass = {'test': SageTest}, # adding a special setup command for tests
    # setup_requires   = ['sage-package'],
    # install_requires = ['sage-package', 'sphinx'],
)
