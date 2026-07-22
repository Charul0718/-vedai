from setuptools import setup, find_packages

setup(
    name="report-engine",
    version="1.0.0",
    description="Report compiler and PDF generator for VedAI",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pydantic",
        "fpdf2",
    ],
)
