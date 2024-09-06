# This script is part of HSDFinder, which shall be put in the same directory with HSDFinder.py 

from collections import defaultdict
import re
import os


FILE_ROOT = ""


class Pfam:
    def __init__(self, name, ftype, pf, domain1, value, ipr, domain2):
        self.name = name
        self.ftype = ftype
        self.pf = pf
        self.domain1 = domain1
        self.value = value
        self.ipr = ipr
        self.domain2 = domain2


class Blast:
    def __init__(self, relate, length):
        self.relate = relate
        self.length = length


def step(lines, p_filter, s_length):
    pairs = defaultdict(list)
    genes = {}
    for line in lines:
        line = line.strip('\n')
        items = line.split('\t')
        if len(items) > 3 and items[0] == items[1]:
            genes[items[0]] = items[3]
    for line in lines:
        line = line.strip('\n')
        items = line.split('\t')
        if len(items) > 3 and float(items[2]) > p_filter:
            if items[1] not in pairs[items[0]]:
                lengtha = int(genes[items[0]])
                lengthb = int(genes[items[1]])
                if abs(lengtha - lengthb) < s_length + 1:
                    pairs[items[0]].append(items[1])
    # combination operation
    d_out = defaultdict(list)  # expected output data
    removed = []
    for key in sort_humanly(pairs.keys()):
        if key not in removed:
            d_out[key].extend(pairs[key])
            i = 0  # loop index
            cur = d_out[key].copy()  # current list of this key
            length = len(d_out[key])  # the amount of items related to this key
            while i < length:
                if cur[i] in pairs.keys() and not cur[i] == key:
                    for n in pairs[cur[i]]:
                        if n not in cur:
                            cur.append(n)  # remove duplicates
                    removed.append(cur[i])  # add cur[i] to remove list
                    length = len(cur)  # update length
                i += 1
            d_out[key] = cur.copy()  # update d_out[key]
            cur.clear()
    pairs.clear()
    output = defaultdict(list)
    for item in d_out.keys():
        if item not in removed:
            if len(d_out[item]) > 1:
                for g in d_out[item]:
                    if g in genes.keys():
                        gene_length = genes[g]
                    else:
                        gene_length = 'NaN'
                    output[item].append(Blast(g, gene_length))
    d_out.clear()
    genes.clear()
    return output


def pfam_to_oneline(lines, file, find_type, output_filename):
    # pfam to one line
    d_pfam = defaultdict(list)
    d_temp = {}
    result = defaultdict(list)
    d_output = {}
    for line in lines:
        line = line.strip('\n')
        items = line.split('\t')
        if len(items) > 12 and items[3].lower() == find_type.lower():
            temp_key = items[0] + '/' + items[4]
            d_pfam[temp_key].append(Pfam(items[0], items[3], items[4], items[5], items[8], items[11], items[12]))
    # select the one with smallest value
    for key in d_pfam.keys():
        min_index = 0
        min_value = float(d_pfam[key][0].value)
        for i in range(len(d_pfam[key])):
            if float(d_pfam[key][i].value) < min_value:
                min_index = i
                min_value = float(d_pfam[key][i].value)
        d_temp[key] = d_pfam[key][min_index]
    d_pfam.clear()
    # use gene name as key
    for name in d_temp.keys():
        gene_name, pf_num = name.split('/')
        result[gene_name].append(d_temp[name])
    d_temp.clear()
    # to one line
    result_filename = output_filename
    result_pathname = os.path.join(FILE_ROOT, result_filename)
    for gene in result.keys():
        pf_line = ''
        domain1_line = ''
        value_line = ''
        ipr_line = ''
        domain2_line = ''
        for n in range(len(result[gene])):
            pf_line += result[gene][n].pf
            domain1_line += result[gene][n].domain1
            value_line += result[gene][n].value
            ipr_line += result[gene][n].ipr
            domain2_line += result[gene][n].domain2
            if n < len(result[gene]) - 1:
                pf_line += ', '
                domain1_line += ', '
                value_line += ', '
                ipr_line += ', '
                domain2_line += ', '
        d_output[gene] = Pfam(gene, find_type, pf_line, domain1_line, value_line, ipr_line, domain2_line)
    result.clear()
    # read pairs
    # d_file = defaultdict(list)
    # file_lines = file.split('\n')
    # for file_line in file_lines:
    #     file_items = file_line.split('\t')
    #     if len(file_items) > 2:
    #         relates = file_items[1].split(', ')
    #         lengths = file_items[2].split(', ')
    #         for i in range(len(relates)):
    #             d_file[file_items[0]].append(Blast(relates[i], lengths[i]))
    d_file = file
    # find pfam
    with open(result_pathname, 'w') as f:
        for file_key in sort_humanly(d_file.keys()):
            blast_relate = ''
            blast_length = ''
            pfam_pf_line = ''
            pfam_domain1_line = ''
            pfam_value_line = ''
            pfam_ipr_line = ''
            pfam_domain2_line = ''
            if len(d_file[file_key]) > 1:
                for n in range(len(d_file[file_key])):
                    g_name = d_file[file_key][n].relate
                    blast_relate += g_name
                    blast_length += d_file[file_key][n].length
                    if g_name in d_output.keys():
                        pfam_pf_line += d_output[g_name].pf
                        pfam_domain1_line += d_output[g_name].domain1
                        pfam_value_line += d_output[g_name].value
                        pfam_ipr_line += d_output[g_name].ipr
                        pfam_domain2_line += d_output[g_name].domain2
                    if n < len(d_file[file_key]) - 1:
                        blast_relate += '; '
                        blast_length += '; '
                        pfam_pf_line += '; '
                        pfam_domain1_line += '; '
                        pfam_value_line += '; '
                        pfam_ipr_line += '; '
                        pfam_domain2_line += '; '
                # if not all([_ == "" for _ in pfam_pf_line.split('; ')]):
                f.write(file_key + '\t' + blast_relate + '\t' + blast_length + '\t' + find_type + '\t' + pfam_pf_line
                        + '\t' + pfam_domain1_line + '\t' + pfam_value_line + '\t' + pfam_ipr_line + '\t' +
                        pfam_domain2_line + '\n')
    return result_filename


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
