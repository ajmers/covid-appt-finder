#!/usr/bin/env python

from setuptools import setup

setup(name='covid-appt-finder',
      version='1.0.0',
      description='Find appointments on a calendly calendar',
      author='Anne J Maiale',
      install_requires=[
          'requests=2.25.1',
          'twilio=6.51.1',
          'python-dotenv=0.15.0'
      ],
)
