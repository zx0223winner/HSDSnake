#!/usr/bin/env python3
# HSDFinder v1.0

# Copyright 2021 Xi Zhang, Yining Hu and David R. Smith


#   This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies:
#Pandas

#To collect pandas packages: 
#sudo pip install pandas

# Usage: python3 HSDFinder.py -i <inputfile> -p <percentage identity> -l <length> -f <pfam file> -t <type> -o <output file>
#OR# python3 HSDFinder.py --input_file=<input file> --percentage_identity=<percentage identity> --length=<length> --file=<pfam file> --type=<type> --output_file=<output file>

# Usage: python3 HSD_to_KEGG.py -h
# HSD_to_KEGG.py -i <HSD file> -k <Gene list file with KO annotation> -n <species name> -o <output file name>

# e.g., python3 HSD_to_KEGG.py -i '/.../.../##.species.txt' -k '/.../.../##.species_ko.txt' -n ##.species -o ##.species.out.txt

# If you use HSDFinder for your research, please cite:
# Protocol for HSDFinder: Identifying, annotating, categorizing, and visualizing duplicated genes in eukaryotic genomes DOI:https://doi.org/10.1016/j.xpro.2021.100619

# To refer where the tool first being applied, please cite:
# X. Zhang, et.al. D.R. Smith (2021). Draft genome sequence of the Antarctic green alga Chlamydomonas sp. UWO241 DOI:https://doi.org/10.1016/j.isci.2021.102084 

import sys
import getopt
import operation


def main(argv):
    input_file = ''
    percentage = 90.0
    length = -1
    pfam = ''
    p_type = "Pfam"
    output_file = 'HSDFinder_result.txt'
    try:
        opts, args = getopt.getopt(argv, "hi:p:l:f:t:o:", ["input_file=", "percentage_identity=", "length=", "file=",
                                                           "type=", "output_file="])
    except getopt.GetoptError:
        print('use main.py -h to see argument options')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('HSDFinder.py -i <inputfile> -p <percentage identity> -l <length> -f <pfam file> -t <type> -o '
                  '<output file>')
            print(
                'or use HSDFinder.py --input_file=<input file> --percentage_identity=<percentage identity> '
                '--length=<length> --file=<pfam file> --type=<type> --output_file=<output file>\n'
                '-i or --input_file\t the BLAST output file \n'
                '-p or --percentage_identity\tidentity percent e.g. For 90%, input 90.0\n'
                '-l or --length\tlength e.g. 10\n'
                '-f or --file\tthe InterProScan output file \n'
                '-t or --type\ttype e.g. Pfam\n'
                '-o or --output_file\toutput file name')
            sys.exit()
        elif opt in ("-i", "--input_file"):
            input_file = arg
        elif opt in ("-p", "--percentage_identity"):
            try:
                percentage = float(arg)
            except ValueError:
                print("Input value error: the percentage identity must be a number.\n"
                      "use HSDFinder.py -h to see more information.")
                sys.exit(2)
        elif opt in ("-l", "--length"):
            try:
                length = int(arg)
            except ValueError:
                print("Input value error: the length must be a number.\n"
                      "use HSDFinder.py -h to see more information.")
                sys.exit(2)
        elif opt in ("-f", "--file"):
            pfam = arg
        elif opt in ("-t", "--type"):
            p_type = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
    if length == -1:
        length = 10
    if input_file == "" or pfam == "":
        print("no input file or no pfam file.")
        sys.exit(2)
    else:
        result = operation.pfam_file_fun(input_file, percentage, length, pfam, p_type, output_file)
        print("Output file " + result + " saved")


if __name__ == "__main__":
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
