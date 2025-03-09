# This script is part of HSDFinder, which shall be put in the same directory with HSDFinder.py 



from collections import defaultdict
import sys
import getopt
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

HSD_file = ''
ko_file = ''
s_name = ''
out_file = 'output.txt'
argv = sys.argv[1:]
try:
	opts, args = getopt.getopt(argv, "hi:k:n:o:", ["input_file=", "ko_file=", "species_name=", "output_file="])
except getopt.GetoptError as e:
	print(str(e) + '. Use KEGG.py -h to see argument options')
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print('KEGG.py -i <HSD file> -k <Gene list file with KO annotation> -n <species name> -o <output file name>')
		print('or use KEGG.py --input_file=<HSD file> --ko_file=<Gene list file with KO annotation> --species_name=<species name> --output_file <output file name>')
		sys.exit()
	elif opt in ("-i", "--input_file"):
		HSD_file = arg
	elif opt in ("-k", "--ko_file"):
		ko_file = arg
	elif opt in ("-n", "--species_name"):
		s_name = arg
	elif opt in ("-o", "--output_file"):
		out_file = arg
if HSD_file == '':
	print("no HSD file.")
	sys.exit(2)
elif ko_file == '':
	print("no ko file. Use -h to see argument options")
	sys.exit(2)
elif s_name == '':
	print("spieces name cannot be empty.")
	sys.exit(2)
else:
	infile=open(os.path.join(__location__,'KO_database.keg'),'r')
	lines = infile.readlines()
	c_dic = defaultdict(list)
	o_dic = defaultdict(list)
	c = ""
	o = ""
	k = ""
	llist = []
	for line in lines:
		line = line.strip('\n')
		if not line == "":
			if line.startswith('B'):
				line = line.replace('B', '')
				if not line == '':
					line = line.replace('  ', '')
					c = line
					llist.append(c)
			elif line.startswith('C'):
				line = line.replace('C', '')
				if not line == '':
					line = line.replace('  ', '')
					o = line
					c_dic[c].append(o)
			elif line.startswith('D'):
				line = line.replace('D', '')
				if not line == '':
					line = line.replace('      ', '')
					ks = line.split('  ')
					k = ks[0] + '\t' +' '.join(ks[1:])
					o_dic[o].append(k)

	infile2=open(ko_file,'r')
	lines2 = infile2.readlines()
	g_dic = defaultdict(list)
	for line2 in lines2:
		line2 = line2.strip('\n')
		if not line2 == "":
			items = line2.split('\t')
			if len(items) > 1:
				g_dic[items[1]].append(items[0])

	infile3 = open(HSD_file, 'r')
	lines3 = infile3.readlines()
	hsd_dic = defaultdict(list)
	for line3 in lines3:
		line3 = line3.strip('\n')
		if not line3 == '':
			aaa = line3.split('\t')
			if len(aaa) > 1:
				bbb = aaa[1].split('; ')
				for b in bbb:
					hsd_dic[b].append(aaa[0])

	outfile = open(out_file,'w')
	cc = ""
	oo = ""
	kk = ""
	removed = []
	for l in llist:
		cc = l
		for start_o in c_dic[l]:
			oo = start_o
			for start_k in o_dic[oo]:
				k_items = start_k.split('\t')
				k_name = k_items[0]
				if k_name in g_dic.keys() and k_name not in removed:
					removed.append(k_name)
					temp = []
					name_list = []
					for genes in g_dic[k_name]:
						if genes in hsd_dic.keys():
							temp+=hsd_dic[genes]
							name_list.append(genes)
					temp = list(set(temp))
					if len(temp)>0:
						outfile.write(cc + '\t' + oo + '\t' + start_k + '\t' + ', '.join(name_list) + '\t' + s_name + '\t' + ', '.join(temp) + '\t' + str(len(temp)) +'\n')
	outfile.close()
