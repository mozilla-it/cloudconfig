import os
import setuptools
from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

requirements = [
   str(r.req) for r in parse_requirements("requirements.txt", session=False)
]

setup(
    name="dynamic-property-management-module",
    version="0.0.2",
    description="Dynamic configuration module.",
    python_requires=">=3.4",
    author="IT Data Team",
    author_email="data-services@mozilla.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    scripts=[s for s in setuptools.findall("bin/") if os.path.splitext(s)[1] != ".pyc"],
    install_requires=requirements,
    package_data={"dpm": ["config/*json", "error_codes/*.json"]},
    data_files=[],
)
