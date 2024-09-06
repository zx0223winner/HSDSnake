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

from collections import defaultdict
import sys
import getopt
import re

# Since the similarity of duplicate genes within and among genomes can vary significantly, 
# by using the scripts HSD_add_on.py and HSD_batch_run.py, 
# users can add newly curated HSDs using a combination of thresholds to assemble a larger dataset of HSD candidates. 

# define the column headers of HSD folder data
class Gene:
    def __init__(self, name, length, ftype, pf, domain1, evalue, ipr, domain2):
        self.name = name
        self.length = length
        self.ftype = ftype
        self.pf = pf
        self.domain1 = domain1
        self.evalue = evalue
        self.ipr = ipr
        self.domain2 = domain2

# define the same_domain function to decide if gene copies contain same conserved domain.
def same_domain(domain_list):
    domains = domain_list[0].split(', ')
    for item in domain_list:
        cur_domains = item.split(', ')
        if not set(cur_domains) == set(domains):
            return False
    return True

# define hsd_filter fucntion to filter those added HSDs. We added the HSD candidates one after another at different homology assessment metrics (i.e. HSDs identified at more relaxed thresholds were treated more strictly than those found using more conservative thresholds). 
def hsd_filter(adding_file):
    gene_list = {}
    hsd_to_add = defaultdict(list)
    with open(adding_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            items = line.split('\t')
            domain_list = items[4].split('; ')
            if "" not in domain_list and same_domain(domain_list):
                gene_names = items[1].split('; ')
                for i in range(len(gene_names)):
                    gene_list[gene_names[i]] = Gene(gene_names[i], items[2].split('; ')[i], items[3],
                                                    items[4].split('; ')[i], items[5].split('; ')[i],
                                                    items[6].split('; ')[i], items[7].split('; ')[i],
                                                    items[8].split('; ')[i])
                    hsd_to_add[items[0]].append(gene_names[i])
            elif "" in domain_list and same_domain(domain_list):
                length =[int(i) for i in items[2].split('; ')]
                if min(length)/max(length) > 0.5:
                    gene_names = items[1].split('; ')
                    for i in range(len(gene_names)):
                        gene_list[gene_names[i]] = Gene(gene_names[i], items[2].split('; ')[i], items[3],
                                                        items[4].split('; ')[i], items[5].split('; ')[i],
                                                        items[6].split('; ')[i], items[7].split('; ')[i],
                                                        items[8].split('; ')[i])
                        hsd_to_add[items[0]].append(gene_names[i])
    return hsd_to_add, gene_list

# HSDs identified at a threshold of 90%_30aa were added on to those identified at a threshold of 90%_10aa (denoted as ‘90%_30aa+90%_10aa’); any redundant HSDs candidates picked out at this combo threshold were removed if the more relaxed threshold (i.e. 90%_30aa) had the identical genes or contained the same gene copies from the stricter cut-off (i.e. 90%_10aa). Moreover, any HSD candidates pinpointed at the combo threshold (90%_30aa + 90%_10aa) were removed if the minimum gene copy length was less than half of the maximum gene copy length for each HSD.
def add_hsd(input_file, gene_list, hsd_to_add, output_file):
    old_hsd_dic = defaultdict(list)
    gene_to_hsd = defaultdict(list)
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            items = line.split('\t')
            gene_names = items[1].split('; ')
            for i in range(len(gene_names)):
                try:
                    gene_list[gene_names[i]] = Gene(gene_names[i], items[2].split('; ')[i], items[3],
                                                    items[4].split('; ')[i], items[5].split('; ')[i],
                                                    items[6].split('; ')[i], items[7].split('; ')[i],
                                                    items[8].split('; ')[i])
                except IndexError:
                    print(line)
                old_hsd_dic[items[0]].append(gene_names[i])
                gene_to_hsd[gene_names[i]].append(items[0])
    remove_list = []
    for key in sort_humanly(hsd_to_add.keys()):
        genes = hsd_to_add[key]
        for gene in genes:
            if gene in gene_to_hsd.keys():
                old_hsd_names = gene_to_hsd[gene]
                for hsd in old_hsd_names:
                    if hsd not in remove_list:
                        old_genes = old_hsd_dic[hsd]
                        check = all(item in genes for item in old_genes)
                        if check:
                            remove_list.append(hsd)
    # write to output file
    with open(output_file, 'w') as out:
        for k in sort_humanly(hsd_to_add.keys()):
            output_line = k + '\t' + write_gene_oneline(hsd_to_add[k], gene_list) + '\n'
            out.write(output_line)
        for key in sort_humanly(old_hsd_dic.keys()):
            if key not in remove_list:
                output_line = key + '\t' + write_gene_oneline(old_hsd_dic[key], gene_list) + '\n'
                out.write(output_line)
    return output_file

# write gene in one line 
def write_gene_oneline(gene_names, gene_list):
    gene = ""
    length = ""
    pf = ""
    domain1 = ""
    evalue = ""
    ipr = ""
    domain2 = ""
    for i in range(len(gene_names)):
        gene += gene_list[gene_names[i]].name
        length += gene_list[gene_names[i]].length
        pf += gene_list[gene_names[i]].pf
        domain1 += gene_list[gene_names[i]].domain1
        evalue += gene_list[gene_names[i]].evalue
        ipr += gene_list[gene_names[i]].ipr
        domain2 += gene_list[gene_names[i]].domain2
        if i < len(gene_names) - 1:
            gene += "; "
            length += "; "
            pf += "; "
            domain1 += "; "
            evalue += "; "
            ipr += "; "
            domain2 += "; "
    return gene + "\t" + length + "\t" + gene_list[gene_names[0]].ftype + "\t" + pf + "\t" + domain1 + "\t" + evalue + \
           "\t" + ipr + "\t" + domain2


# sort functions
def tryint(s):
    try:
        return int(s)
    except ValueError:
        return s


def str2int(v_str):
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]


def sort_humanly(v_list):
    return sorted(v_list, key=str2int)

# the main function of the HSD_add_on.py script
def main(argv):
    input_file = ''
    adding_file = ''
    output_file = 'HSDFinder_result.txt'
    try:
        opts, args = getopt.getopt(argv, "hi:a:o:", ["input_file=", "adding_file=", "output_file="])
    except getopt.GetoptError:
        print('use HSD_add_on.py  -h to see argument options')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('HSD_add_on.py  -i <inputfile> -a <adding_file> -o <output file>')
            print(
                'or use HSD_add_on.py  --input_file=<input file> --adding_file=<adding_file> --output_file=<output '
                'file>\n '
                '-i or --input_file\tyour HSD file\n'
                '-a or --adding_file\tHSDs to be added\n'
                '-o or --output_file\toutput file name')
            sys.exit()
        elif opt in ("-i", "--input_file"):
            input_file = arg
        elif opt in ("-a", "--adding_file"):
            adding_file = arg
        elif opt in ("-o", "--output_file"):
            output_file = arg
    if input_file == "" or adding_file == "":
        print("no input file or no adding file. use HSD_add_on.py  -h to see argument options")
        sys.exit(2)
    else:
        hsd_to_add, gene_list = hsd_filter(adding_file)
        result = add_hsd(input_file, gene_list, hsd_to_add, output_file)
        print(result + " saved!")


if __name__ == "__main__":
    main(sys.argv[1:])
