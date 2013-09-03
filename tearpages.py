#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License: GPLv3

__version__ = '0.1'

import argparse
import shutil
import tempfile
from PyPDF2 import PdfFileWriter, PdfFileReader


def main(filename):
    """
    Copy filename to a tempfile, write pages 1..N to filename.

    :param filename: PDF filepath
    """
    tmp = tempfile.NamedTemporaryFile()
    shutil.copy(filename, tmp.name)

    output_file = PdfFileWriter()
    input_file = PdfFileReader(open(tmp.name, 'rb'))
    num_pages = input_file.getNumPages()

    for i in range(1, num_pages):
        output_file.addPage(input_file.getPage(i))

    tmp.close()
    outputStream = open(filename, "wb")
    output_file.write(outputStream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remove the first page of a PDF',
                             epilog='')
    #parser.add_argument('--version', action='version', version=info.NAME + ' ' + info.VERSION)
    parser.add_argument('pdf', metavar='PDF', help='PDF filepath')
    args = parser.parse_args()

    main(args.pdf)
