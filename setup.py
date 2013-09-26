from distutils.core import setup
from setuptools import setup

setup(
    name='GitHub2NNTP',
    version='0.1.0',
    author='Raniere Silva',
    author_email='ra092767@ime.unicamp.br',
    packages=['github2nntp'],
    url='http://github2nntp.rgaiacs.com',
    license='COPYING',
    description='Gateway from GitHub to NNTP.',
    long_description=open('README').read(),
    entry_points={
        'console_scripts':['github2nntp = github2nntp.main:main']}
)
