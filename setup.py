import os
from setuptools import setup

def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

def requirements():
    # Print the current working directory to debug
    print("Current Directory:", os.getcwd())
    print("Listing Directory Contents:", os.listdir())
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return f.read().splitlines()

setup(
    name="URAG",
    version="0.0.1",
    author="Masoud Navidi",
    author_email="navidi.m.91@gmail.com",
    description="Build your own chatbot in no time!",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/masoud-n91/RAG",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.9',
    install_requires=requirements(),
)
