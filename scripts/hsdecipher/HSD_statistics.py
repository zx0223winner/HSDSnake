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

import os
import sys

# HSD_statistics.py is a python script that calculates the statistics of HSDs using a variety of HSDFinder thresholds. 
# The output file is written in a table with the following headers: 
# File name, Candidate HSDs, Non-redundant gene copies, Gene copies, True HSDs, Space, Incomplete HSDs, Capturing value, and Performance score. 
# ‘Capturing value’ and 'Performance score’ are two parameters used to evaluate the HSD results

if len(sys.argv)!=4: #if the input arguments not 4, showing the usage.
    print("Usage:python3 HSD_statistics.py <path to HSD species folder> <format of HSD file. e.g., 'txt' or 'tsv'> <output file name. e,g. species_stat.tsv>")
    sys.exit()

root = sys.argv[1]
folder = os.listdir(root)
folder.sort()
result_list = []
for file in sorted(folder):
    file_paths = os.path.join(root, file)
    if not os.path.isdir(file_paths) and file.split('.')[-1] == sys.argv[2]:
        false_positive = 0
        space = 0
        hsd = 0
        score = 0
        gene_list = []
        with open(file_paths, 'r') as f:
            lines = f.readlines()
            for line in lines:
                items = line.split('\t')
                if len(items) > 4:
                    is_space = True
                    domain_list = items[4].split('; ')
                    cur_domain = domain_list[0].split(', ')
                    for domain in domain_list:
                        temp_domain = domain.split(', ')
                        if not sorted(temp_domain) == sorted(cur_domain):
                            false_positive += 1
                            break
                        if not domain == "":
                            is_space = False
                    if is_space:
                        space += 1
                    hsd += 1
                    gene_list += items[1].split('; ')
        true_positive = hsd-false_positive
        precision = round(true_positive*100/hsd,2)
        score = round((true_positive+hsd-space)/(false_positive+1),2)
        gene_list_non_repeat = list(set(gene_list))
        result_list.append(".".join(file.split('.')[:-1]) + '\t' + str(hsd) + '\t' + str(len(gene_list_non_repeat)) +
                           '\t' + str(len(gene_list)) + '\t' + str(true_positive) + '\t' + str(space) + '\t' +
                           str(false_positive) + '\t' + str(precision) + '\t' + str(score))
with open(sys.argv[3], 'w') as out:
    out.write("File_name\tCandidate_HSDs#\tNon-redundant_gene_copies#\tGene_copies#\tTrue_HSDs#\tSpace#\tIncomplete_HSDs#\tCapturing_value\tPerformance_score\n")
    for r in result_list:
        out.write(r + '\n')

#file.split('.')[0]
#".".join(file.split('.')[:-1])
