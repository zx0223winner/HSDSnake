def main():

    import sys
    if len(sys.argv)!=4: #if the input arguments not 4, showing the usage.
        print("Usage:python3 index_header_to_seq.py <coding_sequence.fasta> <list_of_header_name.txt> <outfile_header_to_sequence.fasta>")
        sys.exit()

    from collections import defaultdict # High-performance container datatypes,  a Python dictionary throws a KeyError if you try to get an item with a key that is not currently in the dictionary
    handle=open(sys.argv[1],'r') 
    dic = defaultdict(list) # The defaultdict will simply create any items that you try to access
    handle2=open(sys.argv[2],'r')
    for line in handle: #loop line in file [1]
        if line.startswith('>'): #index the sequence name 
            header =line.strip('>') #strip the '>', so as to index name  
        else:
            dic[header].append(line) #if not the header name, then it is sequence, append function() is used to not erase former seq lines.

    outfile=open(sys.argv[3],'w')
    for line2 in handle2: #loop the lines in file [2]
        if line2 in dic.keys(): #if the each line name match the keys 
            outfile.write('>'+line2+''.join(dic[line2]))  #write out the file[3], together with seq and header name. join those seqs.

    handle2.close()
    outfile.close()
if __name__=='__main__':
    main()
