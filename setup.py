import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linqit",
    version="0.1.5",
    author="Avi Lumelsky",
    author_email="noticetheg@gmail.com",
    description="Extends python's list builtin with fun, robust functionality - "
    ".NET's Language Integrated Queries (Linq) and more. Write clean code with powerful syntax.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avilum/linqit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=2.7,>=3.6",
)
