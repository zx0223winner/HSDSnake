#index from different files by hash
#In order to set a general default value for all keys, you can use defaultdict:
#from collections import defaultdict 
#isoform2one - this script takes the alternative splicing transcripts to the # primary one and return with the primary protein sequence.

import sys
if len(sys.argv)!=3: #if the input arguments not 3, showing the usage.
	print("Please try this! Usage:python3 isoform2one.py <tabular_info_file> <trimmed_primary_protein> ")
	sys.exit()

from collections import defaultdict
my_dict=defaultdict(list)
my_dict1=defaultdict(list)

outfile=open(sys.argv[2],'w')
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.split("\t")[15] != "":
            if line != "" and line.split("\t")[0] == 'mRNA' and line.split("\t")[12] != "": 
                my_dict[line.split("\t")[15]].append(line) # hash 
        else:
            my_dict1[line.split("\t")[12]].append(line)
    #print(my_dict)

for key in my_dict.keys():
    if len(my_dict[key]) == 1:
        outfile.write(my_dict[key][0].split("\t")[12]+"\n")
    else:
        primary_line = ""
        length = 0
        for item in my_dict[key]:
            if int(item.split("\t")[17]) > length:
                primary_line = item
                length = int(item.split("\t")[17])
        outfile.write(primary_line.split("\t")[12]+"\n")

for key in my_dict1.keys():
    outfile.write(str(key) +"\n")
outfile.close()
