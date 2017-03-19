# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top
# level README file and 2) it's easier to type in the README file than to
# put a raw string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


requires = ['Sphinx>=0.6',
            'SQLAlchemyViz']

setup(
    name='sphinxcontrib-sqlalchemyviz',
    version='0.3',
    url='https://github.com/chintal/sphinxcontrib-sqlalchemyviz',
    download_url='https://github.com/chintal/sphinxcontrib-sqlalchemyviz',
    license='BSD',
    author='Chintalagiri Shashank',
    author_email='shashank@chintal.in',
    description='Sphinx SQLAlchemyViz extension',
    long_description=read('README.rst'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
