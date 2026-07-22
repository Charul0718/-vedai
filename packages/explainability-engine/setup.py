from setuptools import setup, find_packages

setup(
    name="explainability-engine",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "knowledge-engine",
    ],
)
