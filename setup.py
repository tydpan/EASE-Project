import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "EASE",
    version = "1.0.0",
    author = "Tai-Yu Pan",
    author_email = "taiyupan@uw.edu",
    description = ("EASE is a suggestion model with an aim to help industrial users who desire to build an "
                   "electricity generation plant that offsets long term cost from continuously buying electricity "
                   "from the Government."),
    license = "GPL-3.0",
    url = "https://github.com/danielfather7/EASE-Project",
    packages=['EASE'],
    long_description=read('README')
    ,
)