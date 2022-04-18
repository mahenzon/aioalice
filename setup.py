#!/usr/bin/env python3
import pathlib
import sys

from setuptools import find_packages, setup

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 6)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aioAlice works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))

__version__ = '1.5.1'


def get_description():
    """
    Read full description from 'README-PyPI.md'

    :return: description
    :rtype: str
    """
    with open('README-PyPI.md', 'r', encoding='utf-8') as f:
        return f.read()


requirements_filepath = WORK_DIR / "requirements.txt"
with open(requirements_filepath) as fp:
    install_requires = fp.read()


setup(
    name='aioAlice',
    version=__version__,
    packages=find_packages(exclude=('tests', 'tests.*', 'examples',)),
    url='https://github.com/mahenzon/aioalice',
    license='MIT',
    author='Suren Khorenyan',
    requires_python='>=3.6',
    author_email='surenkhorenyan@gmail.com',
    description='Asynchronous library for Yandex Dialogs (Alice) API',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=install_requires,
)
