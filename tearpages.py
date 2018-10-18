#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

import argparse
import shutil
import tempfile
from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.utils import PdfReadError

__version__ = '0.3.0'


def fixPdf(pdfFile, destination):
    """
    Fix malformed pdf files when data are present after '%%EOF'

    :param pdfFile: PDF filepath
    :param destination: destination
    """
    with tempfile.NamedTemporaryFile() as tmp:
        with open(tmp.name, 'wb') as output:
            with open(pdfFile, "rb") as fh:
                for line in fh:
                    output.write(line)
                    if b'%%EOF' in line:
                        break
        shutil.copy(tmp.name, destination)


def tearpage(filename, startpage=0):
    """
    Copy filename to a tempfile, write pages startpage..N to filename.

    :param filename: PDF filepath
    :param startpage: page number for the new first page
    """
    # Copy the pdf to a tmp file
    with tempfile.NamedTemporaryFile() as tmp:
        shutil.copy(filename, tmp.name)

        # Read the copied pdf
        try:
            input_file = PdfFileReader(open(tmp.name, 'rb'))
        except PdfReadError:
            fixPdf(filename, tmp.name)
            input_file = PdfFileReader(open(tmp.name, 'rb'))
        # Seek for the number of pages
        num_pages = input_file.getNumPages()

        # Write pages excepted the first one
        output_file = PdfFileWriter()
        for i in range(startpage, num_pages):
            output_file.addPage(input_file.getPage(i))

        
    with open(filename, "wb") as outputStream:
        output_file.write(outputStream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove the first page of a PDF',
                                     epilog='')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('pdf', metavar='PDF', help='PDF filepath')
    args = parser.parse_args()

    tearpage(args.pdf, startpage=1)
