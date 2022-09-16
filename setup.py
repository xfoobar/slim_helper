import pathlib
from setuptools import setup

# The directory containing this file
pwd = pathlib.Path(__file__).parent

# The text of the README file
README = (pwd / "README.md").read_text()

package_name='slim_helper'

# This call to setup() does all the work
setup(
    name=package_name,
    version="1.10.2",
    python_requires='~=3.10',
    description="Simple helper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xfoobar/slim_helper",
    author="xfoobar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation'
    ],
    extras_require={
        "oracle": ["oracledb>=1.1.0, <2.0.0"],
        "postgresql": ["psycopg>=3.1.1, <4.0.0"]
    },
    packages=[package_name],
    include_package_data=True,
    install_requires=[],
    platforms=["all"]
)