import os
from setuptools import setup, find_packages

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
  name="fitness_tracker",
  version="0.3.2",
  author="Jurica Runtas, Kristijan Milić",
  url="https://github.com/JuricaRT/fitness_tracker",
  license="MIT",
  description="Fitness Tracker is a tool that offers a better way of tracking your fitness progress.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
  include_package_data=True,
  classifiers=["Programming Language :: Python :: 3",
               "License :: OSI Approved :: MIT License",
               "Operating System :: OS Independent"],
  install_requires=["PyQt5", "requests", "psycopg2",
                    "matplotlib", "numpy"],
  python_requires=">=3.6",
)
