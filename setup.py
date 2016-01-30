#!/usr/bin/env python

from distutils.core import setup
from tearpages import __version__

setup(
    name         = 'tear-pages',
    version      = __version__,
    url          = 'https://github.com/sciunto/tear-pages',
    author       = "Francois Boulogne",
    author_email = 'devel@sciunto.org',
    license      = 'GPLv3',
    description  = 'Simple script to remove the first page of a PDF',
    scripts      = ['tearpages.py'],
    install_requires=['PyPDF2>=1.25.1'],
)
