#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

import argparse
import logging
import shutil
import tempfile
from PyPDF2 import PdfWriter, PdfReader

__version__ = '0.5.0'


#def fixPdf(pdfFile, destination):
#    """
#    Fix malformed pdf files when data are present after '%%EOF'
#
#    :param pdfFile: PDF filepath
#    :param destination: destination
#    """
#    with tempfile.NamedTemporaryFile() as tmp:
#        with open(tmp.name, 'wb') as output:
#            with open(pdfFile, "rb") as fh:
#                for line in fh:
#                    output.write(line)
#                    if b'%%EOF' in line:
#                        break
#        shutil.copy(tmp.name, destination)


def tearpage(filename, startpage=0, lastpage=0):
    """
    Copy filename to a tempfile, write pages startpage..N to filename.

    :param filename: PDF filepath
    :param startpage: number of pages to delete from the cover
    :param lastpage: number of pages to delete from the bacl
    """
    # Copy the pdf to a tmp file
    with tempfile.NamedTemporaryFile() as tmp:
        shutil.copy(filename, tmp.name)

        # Read the copied pdf
        input_file = PdfReader(tmp.name)
        # Seek for the number of pages
        #num_pages = input_file.getNumPages()
        num_pages = len(input_file.pages)

        if startpage >= num_pages - lastpage:
            raise ValueError('Incorrect number of pages')

        # Write pages excepted the first one
        output_file = PdfWriter()
        for i in range(startpage, num_pages-lastpage):
            output_file.add_page(input_file.pages[i])

    with open(filename, "wb") as outputStream:
        output_file.write(outputStream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove the first page of a PDF',
                                     epilog='')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('-d', '--debug', action='store_true',
                        default=False, help='Run in debug mode')
    parser.add_argument('pdf', metavar='PDF', help='PDF filepath')
    parser.add_argument('--first', action='store_true',
                        default=False, help='Tear the first page')
    parser.add_argument('--last', action='store_true',
                        default=False, help='Tear the last page')


    args = parser.parse_args()

    # Logger level
    if args.debug:
        llevel = logging.DEBUG
    else:
        llevel = logging.INFO
    logger = logging.getLogger()
    logger.setLevel(llevel)

    logger.debug(args)

    # Handle first/last page
    if args.first:
        startpage =  1
    else:
        startpage = 0

    if args.last:
        lastpage = 1
    else:
        lastpage = 0

    tearpage(args.pdf,
            startpage=startpage,
            lastpage=lastpage)
