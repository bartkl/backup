from setuptools import setup, find_packages
import os

setup(name='Backup',
      author='Bart Kleijngeld',
      author_email='bartkl@gmail.com',
      version='1.0.1',
      license='MIT',
      description='Backup script which provides an easily configurable rsync based solution.',
      url='https://github.com/bartkl/backup',
      packages=find_packages(),
      install_requires=[''],
      include_package_data=True,
      entry_points={'console_scripts': [
        'backup = backup:cli']}
)