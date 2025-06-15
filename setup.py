from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")
long_description = open(readme_path, encoding="utf-8").read() if os.path.exists(readme_path) else ""

setup(
    name="hexplorer",
    version="1.0.0",
    description="A Terminal-Based HEX Color Explorer With Gradients, Mix, and Schemes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mallik Mohammad Musaddiq",
    author_email="mallikmusaddiq1@example.com",
    url="https://github.com/mallikmusaddiq1/hexplorer",
    packages=find_packages(),
    install_requires=[ ],  # No external dependencies
    entry_points={
        "console_scripts": [
            "hexplorer=hexplorer.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)