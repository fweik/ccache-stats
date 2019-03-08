import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccache_stats",
    version="0.0.1",
    author="Florian Weik",
    author_email="florianweik@gmail.com",
    description="Access ccache stats in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fweik/ccache-stats",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
