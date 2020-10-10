from setuptools import setup, find_packages
import os

setup(name='Backup',
      version='1.0',
      description='Backup script which provides an easily configurable rsync based solution.',
      packages=find_packages(),
      install_requires=[''],
      include_package_data=True,
      entry_points={'console_scripts': [
        'backup = backup:cli']},
)