# HSDecipher v1.0

# Copyright 2022 Zhang X., Hu Y., Zhengyu Cheng, Archibald J.M.


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

import sys
import getopt
import os

# HSDs identified at a threshold of 90%_30aa were added on to those identified at a threshold of 90%_10aa (denoted as ‘90%_30aa+90%_10aa’); 
# any redundant HSDs candidates picked out at this combo threshold were removed if the more relaxed threshold (i.e. 90%_30aa) had the identical genes or contained the same gene copies from the stricter cut-off (i.e. 90%_10aa). 
# Moreover, any HSD candidates pinpointed at the combo threshold (90%_30aa + 90%_10aa) were removed if the minimum gene copy length was less than half of the maximum gene copy length for each HSD.

# Define the main function of batch_run.py. 
def main(argv):
    input_folder = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["input_folder="])
    except getopt.GetoptError:
        print('use HSD_add_on.py -h to see argument options')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('batch_run.py -i <inputfolder>')
            print('For example, batch_run.py -i hsdfinder')
            print('Note: The hsdfinder folder should have the sub_folder with species name, such as Arabidopsis_thaliana which should exactly match Arabidopsis_thaliana.90_10.txt  ')
            sys.exit()
        elif opt in ("-i", "--input_folder"):
            input_folder = arg
    if input_folder == "":
        print("no input folder.")
        sys.exit(2)
    else:
        # add_list = ["50_10", "50_30", "50_50", "50_70", "50_100", "60_10", "60_30", "60_50", "60_70", "60_100",
        #             "70_10", "70_30", "70_50", "70_70", "70_100", "80_10", "80_30", "80_50", "80_70", "80_100",
        #             "90_10", "90_30", "90_50", "90_70", "90_100"]
        # add_list = ["90_30", "90_50", "90_70", "90_100", "80_10", "80_30", "80_50", "80_70", "80_100",
        #             "70_10", "70_30", "70_50", "70_70", "70_100", "60_10", "60_30", "60_50", "60_70", "60_100",
        #             "50_10", "50_30", "50_50", "50_70", "50_100"]
        # add_list = ["80_10", "70_10", "60_10", "50_10", "90_30", "80_30", "70_30", "60_30", "50_30",
        #             "90_50", "80_50", "70_50", "60_50", "50_50", "90_70", "80_70", "70_70", "60_70", "50_70",
        #             "90_100", "80_100", "70_100", "60_100", "50_100"]
        add_dic = {"90": ["90_30", "90_50", "90_70", "90_100"], "80": ["80_30", "80_50", "80_70", "80_100"],
                   "70": ["70_30", "70_50", "70_70", "70_100"], "60": ["60_30", "60_50", "60_70", "60_100"],
                   "50": ["50_30", "50_50", "50_70", "50_100"]}
        add_list = ["80_10", "70_10", "60_10", "50_10"]
#         if not os.path.exists('Finished'):
#             os.mkdir('Finished')
        gene_num = {}
        for f in os.listdir(input_folder):
            if os.path.isdir(input_folder + '/' + f):
#                 if not os.path.exists('Finished/' + f):
#                     os.mkdir('Finished/' + f)
                # for file in add_list:
                #     os.system("python3 add_HSD.py -i " + input_folder + '/' + f + '/' + f + '.90_10.txt' + ' -a ' +
                #               input_folder + '/' + f + '/' + f + '.' + file + '.txt -o ' + input_folder + '/' + f + '/'
                #               + f + '.90_10.txt')
                #os.system("cp -r " + input_folder + '/' + f + " " + input_folder + '/original/' + f)
                for key in sorted(add_dic.keys()):
                    for file in add_dic[key]:
                        os.system("python3 " + os.path.join(__location__,'HSD_add_on.py') + " -i " + input_folder + '/' + f + '/' + f + '.' + key + '_10.txt' +
                                  ' -a ' + input_folder + '/' + f + '/' + f + '.' + file + '.txt -o ' + input_folder +
                                  '/' + f + '/' + f + '.' + key + '_10.txt')
                for file in add_list:
                    os.system("python3 " + os.path.join(__location__,'HSD_add_on.py') + " -i " + input_folder + '/' + f + '/' + f + '.90_10.txt' + ' -a ' +
                              input_folder + '/' + f + '/' + f + '.' + file + '.txt -o ' + input_folder + '/' + f + '/'
                              + f + '.90_10.txt')
                os.system("cp " + input_folder + '/' + f + '/' + f + '.90_10.txt ' + input_folder + '/' + f +'.batch_run.txt')
                #os.system("rm " + "-r" )
                    # output_filename = 'Finished/' + f + '/' + f + '.' + file + '_90_10.txt'
                    # with open(output_filename, 'r') as read_file:
                    #     lines = read_file.readlines()
                    #     # genes = set()
                    #     # for line in lines:
                    #     #     genes.update(line.split("\t")[1].split('; '))
                    # key = f + '.' + file + '_90_10'
                    # gene_num[key] = len(lines)
        #with open('Finished/hsd_num.tsv', 'w') as out:
        #    for key in gene_num:
        #        out.write(key + '\t' + str(gene_num[key]) + '\n')

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

if __name__ == "__main__":
    main(sys.argv[1:])
