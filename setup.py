from setuptools import setup, find_packages

setup(
    name="qps",
    version="0.0.1",
    description="A library to simulate quantum circuits",
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)
