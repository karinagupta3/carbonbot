from setuptools import setup, find_packages

setup(
    name="miriel",  # Your package name
    version="0.1.2",  # Package version
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[],  # External dependencies your package needs (e.g., ['numpy', 'requests'])
    author="David Garcia",
    author_email="david@miriel.ai",
    description="Library for interacting with the Miriel API",
    long_description=open('README.md').read(),  # Display README contents as long description
    long_description_content_type="text/markdown",  # README format
    url="https://github.com/crazydavy/miriel-python",  # URL to your project's homepage
    classifiers=[  # Additional metadata (optional)
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
)