
### 1. HSDecipher
The pipeline has the custom Python scripts packages for the downstream comparative genomics analysis of highly similar duplicate genes

### 2. What's HSDecipher?
The software implementation was written in Python 3 using the following custom scripts and platforms: HSD_statistics.py, HSD_categories.py, HSD_add_on.py, HSD_batch_run.py and HSD_heatmap.py

```python3
# HSD_statistics.py
>python3 HSD_Statistics.py <path to HSD species folder> <format of HSD file. e.g., 'txt' or 'tsv'> <output file name. e,g. species_stat.tsv>
```
>HSD_statistics.py is a custom python script that calculating the statistics of HSDs via using a variety of HSDFinder thresholds. The output file will be written in a table with the header: File name; Candidate_HSDs#; Non-redundant_gene_copies#; Gene_copies#; True_HSDs# ;Space# ;Incomplete_HSDs#; Capturing_value; Performance_score;

```python3
#HSD_categories.py
>python3 HSD_categories.py <path to HSD species folder> <format of HSD file. e.g., 'txt' or 'tsv'> <output file name. e,g. species_groups.tsv>

```
>HSD_categories.py a custom python script that counts the number of HSD with two, three, and more than four categories, which is helpful to evaluate the distribution of groups in HSDs. 


```python3
#HSD_add_on.py
>python3 HSD_add_on.py  -i <inputfile> -a <adding_file> -o <output file>
```
>HSD_add_on.py can add the later HSD data on the former HSD, in this way, the HSD canadiate categories can be enlarged. For example, HSDs identified at a threshold of 90%_30aa were added on to those identified at a threshold of 90%_10aa (denoted as “ 90%_30aa+90%_10aa”); any redundant HSDs candidates picked out at this combination threshold were removed if the more relaxed threshold (i.e., 90%_30aa) had the identical genes or contained the same gene copies from the stricter cut-off (i.e., 90%_10aa).


```python3
#HSD_batch_run.py
>python3 batch_run.py -i <inputfolder>
```
> HSD_batch_run.py can do a series of combination thresholds at once. To minimize the redundancy and to acquire a larger dataset of HSD candidates, we processed each selected species with the following combination of thresholds: E + (D + (C + (B +A))). Any HSDs candidates pinpointed at the combination threshold (90%_30aa+90%_10aa) were removed if the minimum gene copy length was less than half of the maximum gene copy length for each HSD, or if HSD candidates had gene copies with incomplete conserved domains (i.e., different number of Pfam domains). After filtering the combination threshold at (90%_30aa+90%_10aa), we added on a more relaxed threshold 90%_50aa (i.e., 90%_50aa+(90%_30aa+90%_10aa)) and then carried out the same HSD candidate removal/filtering process.

>A = 90%_100aa+(90%_70aa+(90%_50aa+(90%_30aa+90%_10aa)))

>B = 80%_100aa+(80%_70aa+(80%_50aa+(80%_30aa+80%_10aa)))

>C = 70%_100aa+(70%_70aa+(70%_50aa+(70%_30aa+70%_10aa)))

>D = 60%_100aa+(60%_70aa+(60%_50aa+(60%_30aa+60%_10aa)))

>E = 50%_100aa+(50%_70aa+(50%_50aa+(50%_30aa+50%_10aa)))

```python3
#HSD_heatmap.py
>python3 HSD_heatmap.py -f <HSD file folder> -k <KO file folder> -r <width of output heatmap,e.g., 30 pixels> -c <height of output heatmap,e.g., 20 pixels>
```
HSD_heatmap.py is able to visualize the collected HSDs in a heatmap and compare the HSDs sharing the same pathway function. This can be done inta-specise and inter-speies heatmaps. Pleas find the example reuslts in the Heatmap Folder.

### 3. Example of HSDs folder file
--------------------------
HSDFinder generates one output files: 9-column spreadsheet integrating with the information of HSD identifier, gene copies number and Pfam domain.

*Example of the 9-column tab-delimited file:* e.g.,Chlamydomonas_reinhardtii.90_10.txt
```
HSD_identifier  gene_copies AA_length function_type function_identifier function_Description  E-value InterPro_identifier InterPro_description
NP_027422.1	NP_027422.1; NP_849661.1; NP_567636.1	303; 293; 291	Pfam	PF06454; PF06454; PF06454	Protein of unknown function (DUF1084); Protein of unknown function (DUF1084); Protein of unknown function (DUF1084)	5.5E-146; 1.1E-145; 2.1E-143	IPR009457; IPR009457; IPR009457	THH1/TOM1/TOM3 domain; THH1/TOM1/TOM3 domain; THH1/TOM1/TOM3 domain
NP_027543.2	NP_027543.2; NP_001322262.1; NP_001154475.1	606; 603; 684	Pfam	PF03141; PF03141; PF03141	Putative S-adenosyl-L-methionine-dependent methyltransferase; Putative S-adenosyl-L-methionine-dependent methyltransferase; Putative S-adenosyl-L-methionine-dependent methyltransferase	6.2E-75; 5.1E-132; 9.8E-139	IPR004159; IPR004159; IPR004159	Putative S-adenosyl-L-methionine-dependent methyltransferase; Putative S-adenosyl-L-methionine-dependent methyltransferase; Putative S-adenosyl-L-methionine-dependent methyltransferase
```
Column header explanation:
1. `HSD_identifier` Highly Similar Duplicates (HSDs) identifiers: The first gene model of the duplicate gene copies is used as the HSD identifers in default. (e.g. NP_027422.1)
2. `gene_copies` Duplicate gene copies (different genes are seperated by comma)(e.g. NP_027422.1; NP_849661.1; NP_567636.1)
3. `AA_length` Amino acid length of duplicate gene copies (aa)(e.g. 303; 293; 291)
4. `function_type` The protein functional type (e.g., Pfam / PRINTS / Gene3D)
5. `function_identifier` (e.g. PF06454; PF06454; PF06454)
6. `function_Description` (e.g. Protein of unknown function (DUF1084); Protein of unknown function (DUF1084); Protein of unknown function (DUF1084))
7. `E-value` (e.g., 5.5E-146; 1.1E-145; 2.1E-143)
8. `InterPro_identifier` InterPro Entry Identifier (e.g. IPR009457; IPR009457; IPR009457)
9. `InterPro_description` InterPro Entry Description (e.g. THH1/TOM1/TOM3 domain; THH1/TOM1/TOM3 domain; THH1/TOM1/TOM3 domain)
<a name="sec5"></a>

### 4.Limitation
There is a steep learning curve for researchers with limited knowledge of bioinformatics, especially those who are not familiar with the basic command lines and dash shell in a Linux/Unix environment. At the present time, a “one-click solution” does not exist because of the desire to retain flexibility in the usage of our scripts for different purposes. That said, our tool is comparatively easier to use at current stage. At present there are very few tools that can execute the downstream comparative genomics analysis of highly similar duplicate gene data. HSDecipher thus fills a need for the bioinformatics and genomics community.

Since there is no golden rule to distinguish partial duplicates from more complete ones, a combination of thresholds was used to acquire a larger dataset of HSD candidates. But due to the limitation of this strategy, it should be noted that there are some large groups of HSD candidates in the database that likely diverged in function from one another. Users should thus proceed with caution when working with these types of datasets.

### 5. Reference
1. Xi Zhang, Yining Hu, Zhenyu Cheng, John M. Archibald (2023). HSDecipher: A pipeline for comparative genomic analysis of highly similar duplicate genes in eukaryotic genomes. StarProtocols. doi:  doi: https://doi.org/10.1016/j.xpro.2022.102014 
2. Zhang, X., Hu, Y. & Smith, D. R. 2022. HSDatabase - a database of highly similar duplicate genes from plants, animals, and algae. Database, doi:http://doi.org/10.1093/database/baac086.
3. Zhang, X. & Smith, D. R. 2022. An overview of online resources for intra-species detection of gene duplications. Frontiers in Genetics, doi: http://doi.org/10.3389/fgene.2022.1012788.
4. Xi Zhang, Yining Hu, David Roy Smith. (2021). HSDFinder: a BLAST-based strategy to search for highly similar duplicated genes in eukaryotic genomes. Frontiers in Bioinformatics. doi: http://doi.org/10.3389/fbinf.2021.803176
5. Xi Zhang, Yining Hu, David Roy Smith. (2021). Protocol for HSDFinder: Identifying, annotating, categorizing, and visualizing duplicated genes in eukaryotic genomes DOI: https://doi.org/10.1016/j.xpro.2021.100619
6. Xi Zhang, et.al. David Roy Smith (2021). Draft genome sequence of the Antarctic green alga Chlamydomonas sp. UWO241 DOI:https://doi.org/10.1016/j.isci.2021.102084

