from setuptools import setup, find_packages

setup(
    name="ai-engine",
    version="1.0.0",
    description="AI engine client integration for VedAI using Gemini",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "httpx",
        "pydantic",
    ],
)
