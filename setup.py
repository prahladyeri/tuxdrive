#!/usr/bin/env python3
import os
import tuxdrive
from tuxdrive import __version__, __description__, __author__, __email__, __license__
from setuptools import setup, find_packages
from setuptools.command.install import install

pkg_name = 'tuxdrive'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

s = setup(
	name=pkg_name,
	version=__version__,
	license=__license__,
	description=__description__,
	long_description=read("README.md"),
	long_description_content_type='text/markdown',
	url='https://github.com/prahladyeri/%s' % pkg_name,
	packages=find_packages(),
	include_package_data=True,
	entry_points={
		"console_scripts": [
			"tuxdrive = tuxdrive.tuxdrive:main",
		],
	},
	install_requires=['google-api-python-client', 'oauth2client'],
	python_requires = ">= 3.4",
	author=__author__,
	author_email=__email__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	)
