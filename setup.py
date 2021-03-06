from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='legalese',
      version=version,
      description="Manage changes of legal documents",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='legal_text patch merge changeset',
      author='',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
				"lxml>=2.2.7"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
