from setuptools import setup, find_packages
import os

setup(name='Backup',
      author='Bart Kleijngeld',
      author_email='bartkl@gmail.com',
      version='2.0.0',
      license='MIT',
      description='Backup script which provides an easily configurable rsync based solution.',
      url='https://github.com/bartkl/backup',
      packages=find_packages(),
      install_requires=[''],
      entry_points={'console_scripts': [
        'backup = backup:cli']}
)
