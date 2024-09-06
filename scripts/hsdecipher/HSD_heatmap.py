#!/usr/bin/env python3
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
import pandas as pd
from collections import defaultdict
import getopt
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as cls
from os import listdir
from os.path import isfile, join
import os

# HSD_heatmap.py visualizes the collected HSDs in a heatmap and compares HSDs sharing the same predicted biochemical pathway function. 
# The KEGG database has been used to provide KO accession numbers for each gene model identifier

#set the column header for he kegg file
class Kegg:
    def __init__(self, ct1, ct, ko, des):
        self.category1 = ct1
        self.category2 = ct
        self.ko_number = ko
        self.description = des

# define the run() function with the required parameters figure height (row size), figure width (column size) and the HSD folder files
def run(hsd_files_path, ko_files_path, row_size, col_size):
    hsd_file_list = [f for f in listdir(hsd_files_path) if isfile(join(hsd_files_path, f)) and not f.startswith('.')]
    ko_file_list = [f for f in listdir(ko_files_path) if isfile(join(ko_files_path, f)) and not f.startswith('.')]
    # if not len(hsd_file_list) == len(ko_file_list):
    #     print("The numbers of input files do not match. Found " + str(len(hsd_files_list)) + " HSD files and " + str(
    #         len(ko_files_list)) + " Gene list files.")
    #     sys.exit(2)
    # prepare data
    result = pd.DataFrame(columns=('category2', 'ko_id', 'function', 'species_name', 'hsds_num'))
    output = pd.DataFrame(columns=('category1', 'category2', 'ko_id', 'function'))
    output = output.set_index("ko_id")
    # read ko information from database
    kegg_reader = open(os.path.join(__location__,'ko.tsv'), 'r')
    kegg_content = kegg_reader.read()
    keggs = []
    for kegg_line in kegg_content.split('\n'):
        kegg_items = kegg_line.split('\t')
        keggs.append(Kegg(kegg_items[1], kegg_items[2], kegg_items[3], kegg_items[4]))
    kegg_reader.close()
    for i in range(len(hsd_file_list)):
        hsd_file = hsd_file_list[i]
        if len(hsd_file.split('.')) == 1:
            org_name = hsd_file
            find_ko = hsd_file
        else:
            org_name = '.'.join(hsd_file.split('.')[:-1])
            find_ko = hsd_file.split('.')[0]
        # print(org_name)
        ko_file = ""
        for ko in ko_file_list:
            if len(ko.split(".")) == 1:
                temp = ko
            else:
                temp = ko.split('.')[0]
            if temp == find_ko:
                ko_file = ko
        if ko_file == "":
            print(org_name + " not found in gene list folder.")
            sys.exit(2)
        # read hsd and gene pairs
        hsd_dic = defaultdict(list)
        hsd_gene_dic = {}
        hsd_file_reader = open(hsd_files_path + '/' + hsd_file, 'r')
        hsd_content = hsd_file_reader.read()
        hsd_lines = hsd_content.split('\n')
        for hsd_line in hsd_lines:
            if not hsd_line == '':
                h_items = hsd_line.split('\t')
                if len(h_items) > 1:
                    genes = h_items[1].split('; ')
                    for gene in genes:
                        hsd_dic[gene].append(h_items[0])
                    hsd_gene_dic[h_items[0]] = h_items[1]
        hsd_file_reader.close()
        # read ko numbers with genes
        ko_file_reader = open(ko_files_path + '/' + ko_file, 'r')
        ko_content = ko_file_reader.read()
        g_dic = defaultdict(list)
        ko_lines = ko_content.split('\n')
        for ko_line in ko_lines:
            if not ko_line == '':
                k_items = ko_line.split('\t')
                if len(k_items) > 1:
                    g_dic[k_items[1]].append(k_items[0])
        ko_file_reader.close()
        output[org_name+"_hsds_id"] = ""
        output[org_name + "_hsds_genes"] = ""
        output[org_name + "_hsds_num"] = ""
        for kegg in keggs:
            if kegg.ko_number in g_dic.keys():
                temp = []
                for g in g_dic[kegg.ko_number]:
                    if g in hsd_dic.keys():
                        temp += hsd_dic[g]
                temp = list(set(temp))
                temp_gene = []
                for hsd in temp:
                    temp_gene.append(hsd_gene_dic[hsd])
                hsd_num = len(temp)
                if hsd_num > 0:
                    ko_name = kegg.description.split('[EC')[0]
                    # ko_name = kegg.ko_number + '  ' + ko_name
                    result = result.append(pd.DataFrame({'category2': [kegg.category2], 'ko_id': [kegg.ko_number],
                                                         'function': [ko_name], 'species_name': [org_name], 'hsds_num': [hsd_num]}),
                                           ignore_index=True)
                    #result = pd.concat([result, pd.DataFrame({'category2': [kegg.category2], 'ko_id': [kegg.ko_number],
                    #                                     'function': [ko_name], 'species_name': [org_name], 'hsds_num': [hsd_num]})],ignore_index=True)
                    #df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    if kegg.ko_number in output.index:
                        output[org_name + "_hsds_id"][kegg.ko_number] = ", ".join(temp)
                        output[org_name + "_hsds_genes"][kegg.ko_number] = ", ".join(temp_gene)
                        output[org_name + "_hsds_num"][kegg.ko_number] = hsd_num
                    else:
                        row = pd.Series({'category1': kegg.category1, 'category2': kegg.category2, 'function': ko_name,
                                                org_name + "_hsds_id": ", ".join(temp), org_name + "_hsds_genes": ", ".join(temp_gene), org_name + "_hsds_num": hsd_num}, name=kegg.ko_number)
                        output = output.append(row)

    if len(hsd_file_list) > 0:
        # draw heatmap
        threshold = 1
        # if len(hsd_file_list) > 1:
        #     threshold = 2
        species_name = hsd_files_path.split('/')[-1] + '.'
        tests_list = ['50_10', '50_30', '50_50', '50_70', '50_100', '60_10', '60_30', '60_50', '60_70', '60_100',
                      '70_10', '70_30', '70_50', '70_70', '70_100', '80_10', '80_30', '80_50', '80_70', '80_100',
                      '90_10', '90_30', '90_50', '90_70', '90_100']
        columns_list = []
        for t in tests_list:
            columns_list.append(species_name + t)
        heatmap_data = pd.pivot_table(result, index=['category2', 'ko_id', 'function'],
                                      columns='species_name', values='hsds_num', aggfunc='first')
        # heatmap_data = heatmap_data.reindex(columns_list, axis=1)
        heatmap_data = heatmap_data.dropna(thresh=threshold)
        heatmap_data = heatmap_data.fillna(0)
        heatmap_data.reset_index(level=['category2'], inplace=True)
        heatmap_data.sort_values(by='category2', inplace=True)
        # save_file = hsd_files_path.split('/')[-1] + '_' + 'output_heatmap' + '.tsv'
        # heatmap_data.to_csv(save_file, sep='\t')
        category = heatmap_data.pop("category2")
        lut = dict(zip(category.unique(), cls.CSS4_COLORS))
        row_colors = category.map(lut)
        # cmap = sns.cubehelix_palette(light=1, as_cmap=True)
        cmap = sns.color_palette("magma_r", 256)
        cm = sns.clustermap(heatmap_data, row_cluster=False, col_cluster=False, vmax=5,
                            figsize=(row_size, col_size), dendrogram_ratio=[0.2, 0.25], cmap=cmap)
        # row_colors=row_colors
        plt.setp(cm.ax_heatmap.yaxis.get_majorticklabels(), fontsize=8)
        save_name = hsd_files_path.split('/')[-1] + '.' + 'output_heatmap' + '.eps'
        plt.savefig(save_name)
        # plt.show()
        save_file = hsd_files_path.split('/')[-1] + '.' + 'output_heatmap' + '.tsv'
        output.to_csv(save_file, sep='\t')

# define the main function to run the HSD_heatmap.py --hsd_files_path=<HSD file folder> --ko_files_path=<KO file folder> --row_size=<width of output heatmap> --col_size=<height of output heatmap>
def main(argv):
    hsd_files_path = ''
    ko_files_path = ''
    row_size = 30
    col_size = 20
    try:
        opts, args = getopt.getopt(argv, "hf:k:r:c:", ["hsd_files_path=", "ko_files_path=", "row_size=", "col_size="])
    except getopt.GetoptError as e:
        print(str(e) + '. Use HSD_heatmap.py -h to see argument options')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('HSD_heatmap.py -f <HSD file folder> -k <KO file folder> -r <width of output heatmap> '
                  '-c <length of output heatmap>')
            print('HSD_heatmap.py --hsd_files_path=<HSD file folder> --ko_files_path=<KO file folder>'
                  ' --row_size=<width of output heatmap> --col_size=<height of output heatmap>')
            sys.exit(0)
        elif opt in ("-f", "--hsd_files_path"):
            hsd_files_path = arg
        elif opt in ("-k", "--ko_files_path"):
            ko_files_path = arg
        elif opt in ("-r", "--row_size"):
            row_size = int(arg)
        elif opt in ("-c", "--col_size"):
            col_size = int(arg)
    if hsd_files_path == "":
        print("No HSD file path. Use HSD_heatmap.py -h to see argument options")
        sys.exit(2)
    if ko_files_path == "":
        print("No KO file path. Use HSD_heatmap.py -h to see argument options")
        sys.exit(2)
    # print(hsd_files_list)
    # print(ko_files_list)
    run(hsd_files_path, ko_files_path, row_size, col_size)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
if __name__ == "__main__":
    main(sys.argv[1:])
