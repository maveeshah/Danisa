from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in danisa/__init__.py
from danisa import __version__ as version

setup(
	name="danisa",
	version=version,
	description="Customizations for Danista",
	author="Ameer Muavia Shah",
	author_email="mavee.shah@hotmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
