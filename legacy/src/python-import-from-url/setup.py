import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyimporter",
    version="0.0.2",
    author="Example Author",
    author_email="author@example.com",
    description="Python import library extensions with implementation to import from url.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ivangeorgiev/gems/tree/master/src/python-import-from-url/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
