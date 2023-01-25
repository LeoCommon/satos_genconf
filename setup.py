import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='satos_genconf',
    version='0.1',
    packages=['satos_genconf'],
    package_data={'satos_genconf': ['templates/*.j2']},
    entry_points = {
        'console_scripts': ['satos-genconf=satos_genconf.cli:main'],
    },
    author="Martin Böh",
    author_email='contact@martb.dev',
    long_description=read('README.md'),
    url="https://martb.dev",
    # Warning: this does not install the dependencies on buildroot
    install_requires=[
        'python-dotenv>=0.21.0',
        'jinja2>=3.1.2'
    ],
)