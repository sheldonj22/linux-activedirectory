import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="linux-activedirectory",
    version="0.0.1",
    description="An LDAP wrapper designed to allow basic Active Directory automation from Linux",
    long_description=README,
    long_description_content_type="text/markdown",
    package_dir={'': "src"},
    packages=["lindap"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Topic :: System :: Systems Administration"

    ],
    install_requires=["python-ldap ~= 3.3"],
    extras_require={
        "dev": [
            "colorama==0.4.3"
        ]
    }
)
