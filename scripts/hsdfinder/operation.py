# This script is part of HSDFinder, which shall be put in the same directory with HSDFinder.py 

import os
import sys
import pfam

FILE_ROOT = ''


def pfam_file_fun(file_name, p_filter,  s_length, pfam_filename, find_type, output_filename):
    pathname = os.path.join(FILE_ROOT, file_name)
    pfam_pathname = os.path.join(FILE_ROOT, pfam_filename)
    try:
        with open(pathname, 'r', encoding='utf8') as f:
            lines = f.readlines()
    except OSError as e:
        print(e)
        sys.exit()
    try:
        with open(pfam_pathname, 'r', encoding='utf8') as f2:
            lines_pfam = f2.readlines()
    except OSError as e:
        print(e)
        sys.exit()
    output = pfam.step(lines, p_filter, s_length)
    result = pfam.pfam_to_oneline(lines_pfam, output, find_type, output_filename)
    return result
