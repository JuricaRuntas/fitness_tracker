import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name="fitness_tracker",
  version="0.1.0",
  author="Jurica Runtas, Kristijan Milić",
  license="MIT",
  description="Fitness Tracker is a tool that offers a better way of tracking your fitness progress.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_packages(),
  classifiers=["Programming Langugage :: Python :: 3",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent"],
  install_requires=["PyQt5", "requests", "psycopg2"],
  python_requires=">=3.6",
)
