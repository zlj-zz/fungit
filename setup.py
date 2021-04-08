from setuptools import setup, find_packages
import sys

PYTHON_VERSION = sys.version_info[:2]
if PYTHON_VERSION < (3, 6):
    print('Python version must be greater than or equal to 3.5')
    sys.exit()

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    LONG_DESCRIPTION = ""

VERSION = '2.0'

setup(
    name='pyzgit',
    version=VERSION,
    author="Zachary Zhang",
    author_email="zlj1997122@outlook.com",
    description="Simple terminal tool of Git.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/zlj-zz/pyzgit.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    entry_points='''
        [console_scripts]
        g=git.main:g
        fungit=fungit.main:main
    ''',
    python_requires='>=3.6',
)
