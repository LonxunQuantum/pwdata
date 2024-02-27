import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pwdata", 
    version="0.0.1",
    author="LonxunQuantum",
    author_email="lonxun@pwmat.com",
    description="pwdata is a data pre-processing tool for PWMLFF, which can be used to extract features and labels. At the same time, it provides convenient interfaces for data conversion between different software.",
    url="https://github.com/yeahooool/pwdata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)