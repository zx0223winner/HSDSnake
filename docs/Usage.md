# HSDSnake: Usage<!-- omit in toc -->

## 1. [Config.yaml](../config.yaml) file 
You will need to edit the config.yaml file for your own usage. An [example config.yaml](../config.yaml) has been provided to test the pipeline.

> [!WARNING]
> please only substitute the species name to yours, keep the input file format, such as Arabidopsis_thaliana.fa, Arabidopsis_thaliana.interproscan.tsv, Arabidopsis_thaliana.ko.txt

``` conf.yaml
# Critical: input files for HSDSnake, please only substitute the species name to yours, keep the input file format, such as Athaliana.interproscan.tsv, Athaliana.ko.txt

ncbi_assemblies:
  - GCF_000001735.4
  - GCF_000002595.2

ncbi_genomes:
    Athaliana:
        ncbi_assembly: "data/ncbi_download/GCF_000001735.4.zip"
        assembly_id: "GCF_000001735.4"      
        outgroup: "Creinhardtii"
        interproscan: "data/Athaliana.interproscan.tsv"
        KEGG: "data/Athaliana.ko.txt"
#        feature_table: "data/Athaliana.feature_table.txt"
    
    Creinhardtii:
        ncbi_assembly: "data/ncbi_download/GCF_000002595.2.zip"
        assembly_id: "GCF_000002595.2"
        outgroup: "Athaliana"
        interproscan: "data/Creinhardtii.interproscan.tsv"
        KEGG: "data/Creinhardtii.ko.txt"
#        feature_table: "data/Creinhardtii.feature_table.txt"

#note:"XX.feature_table.txt" is an backup option to create fakegff


names:
  - Athaliana
  - Creinhardtii

dup_types:
  - tandem
  - dispersed
  - proximal
  - transposed
  - wgd
  - all

# Wang, Yupeng, et al. Nature Protocols 19.7 (2024): 2206-2229.
MCScanX_protocol:
 - "/scripts/MCScanX_protocol"
 - mkGFF3.pl
 - mkCD.pl
 - add_ka_and_ks_to_collinearity_Yn00.pl

# Qiao, Xin, et al. Genome biology 20 (2019): 1-23; Wang, Yupeng, et al. Nucleic acids research 40.7 (2012): e49-e49.
DupGen_finder:
 - "/scripts/DupGen_finder"
 - DupGen_finder-unique.pl
 - DupGen_finder.pl

# Qiao, Xin, et al. Genome biology 20 (2019): 1-23.
identify_Ks_peaks_by_fitting_GMM: 
  - "/scripts/identify_Ks_peaks_by_fitting_GMM/"
  - add_ka_ks_to_collinearity_file.pl
  - compute_ks_for_synteny_blocks.pl
  - plot_syntenic_blocks_ks_distri.py 

HSDFinder: 
  - "/scripts/hsdfinder/"


################Above are the directories for fasta, interproscan, ko result you shall modify ##########

HSD_identity:
- 90
- 80
- 70
- 60
- 50

HSD_variance:
- 100
- 70
- 50
- 30
- 10

HSDecipher: "/scripts/hsdecipher/"

########Feel free to modidy the heatmap hight and width depending on your dataset scale ###############

heatmap_hight: 20 

heatmap_width: 30

```

## 2. [Snakefile_part1](../workflow/Snakefile_part1)


### Download NCBI assemblies
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


### Preprocessing the naming of the NCBI assemblies
`Purpose`: Rename the NCBI genomic assembly to the format which mcscanx and Dupgen-finder can take.

`scripts`:
```
mkdir -p {params.dir2}{params.species_name}; \
unzip {params.dir1}{params.assembly_id}.zip -d {params.dir1}{params.species_name}; \
sleep 5s; \
cp {params.dir1}{params.species_name}/ncbi_dataset/data/{params.assembly_id}/cds_from_genomic.fna {params.dir2}{params.species_name}/{params.species_name}_cds_from_genomic.fna; \
cp {params.dir1}{params.species_name}/ncbi_dataset/data/{params.assembly_id}/genomic.gff {params.dir2}{params.species_name}/{params.species_name}_genomic.gff; \
cp {params.dir1}{params.species_name}/ncbi_dataset/data/{params.assembly_id}/protein.faa {params.dir2}{params.species_name}/{params.species_name}_protein.faa; \
rm -r {params.dir1}{params.species_name} \
```

`Output`: "data/ncbi/Athaliana/Athaliana_genomic.gff" ; 
"data/ncbi/Athaliana/Athaliana_protein.faa";
"data/ncbi/Athaliana/Athaliana_cds_from_genomic.fna".


### Preprocessing the gff file (default)
`Purpose`: Create a fakegff from the gff3 which can be recognize by McscanX

> [!NOTE]
> Since the input .gff file for mcscanx is nether gff3 nor bed file format, for simplity, call it fakegff file

> [!TIP]
> If the mkGFF3.pl does not work on your gff3 file due to the format of naming, there are other ways/options to generate the fakegff, check the next rules and substitue the fakegff for whichever works.

> [!WARNING]
> The mkGFF3.pl was adopted from MCScanX_protocol which is not exactly same (Wang, Yupeng, et al. Nature Protocols 19.7 (2024): 2206-2229.)

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Input`: data/ncbi/Athaliana/Athaliana_genomic.gff

```
##gff-version 3
#!gff-spec-version 1.21
#!processor NCBI annotwriter
#!genome-build TAIR10.1
#!genome-build-accession NCBI_Assembly:GCF_000001735.4
#!annotation-source TAIR and Araport 
##sequence-region NC_003070.9 1 30427671
##species https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=3702
NC_003070.9	RefSeq	region	1	30427671	.	+	.	ID=NC_003070.9:1..30427671;Dbxref=taxon:3702;Name=1;chromosome=1;ecotype=Columbia;gbkey=Src;genome=chromosome;mol_type=genomic DNA

```


`Output`: data/intermediateData/Athaliana/Athaliana.gff

```


```


### Preprocessing the gff (option one)
`Purpose`: This rule use the gff2bed tool to convert gff to bed for easier parsing (the fakegff file) 

> [!WARNING]
> To run this rule, user will need uncomment the lines in the snakefile_part1
```
	#	expand("data/intermediateData/{name}/{name}.gff-option_one",
	#		name = config['names']),
```

`scripts`:
```
cat {input.gff} \
| grep -v '^#' \
| awk '$3 == "gene"' \
| gff2bed \
| awk 'BEGIN {{OFS="\t"}} {{print $1,$4,$2,$3}}' \
> {output.fakegff} \
```

`Output`: data/intermediateData/Athaliana/Athaliana.gff-option_one



### Preprocessing the gff (option Two)
`Purpose`: This rule can make use of the XX.feature_table.txt from NCBI to generate the fakegff for McScanX as input file.

> [!NOTE]
> user will need to put the "XX.feature_table.txt" in the config.yaml file.
```
# Example of the XX.feature_table.txt:
link: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/002/595/GCF_000002595.2_Chlamydomonas_reinhardtii_v5.5/GCF_000002595.2_Chlamydomonas_reinhardtii_v5.5_feature_table.txt.gz
```
`scripts`:
```
sed 1d {input.feature_table} \
|grep 'mRNA' \
|awk -F'\t' '$13!=""{{print $7"\t"$13"\t"$8"\t"$9}}' \
> {output.fakegff} \
```

`Output`: data/intermediateData/Athaliana/Athaliana.gff-option_two

> [!WARNING]
> To run this rule, user will need uncomment the lines in the snakefile_part1
```
	# Other ways to yield the fakegff: featuretable_to_fakegff
	#	expand("data/intermediateData/{name}/{name}.gff-option_two",
	#		name = config['names']),

```

### prepare the cds file for calculating the Ka/ks ratio
`Purpose`: This rule is preprocessing step for running the McScanX with input data from genomic cds

> [!WARNING]
> The mkCD.pl was adopted from MCScanX_protocol which is not exactly same (Wang, Yupeng, et al. Nature Protocols 19.7 (2024): 2206-2229.)


`scripts`:
```
perl {params.dir2}/mkCD.pl {params.dir3} {params.species_name} \
```

`Output`: data/intermediateData/Athaliana/Athaliana.cds

```
?????
```


### diamond_db_mcscanx
`Purpose`: This rule build diamond database for blasting the protein sequence 

`scripts`:
```
	mkdir -p {params.dir1}; \
	diamond makedb \
		--in {params.protein} \
		-d {params.db_name_dir} \
```

`Output`: data/ncbiDB/Athaliana.dmnd



### diamond_blast_mcscanx
`Purpose`: This rule run diamond blastp for the protein sequences against themselves (blastp all vs all)

> [!NOTE]
> --max-target-seqs parameter will impact how many candidate duplicates will be detected
`scripts`:
```
		diamond blastp \
		-d {params.db_name_dir} \
		-q {params.protein} \
		-o {output} \
		-e 1e-10 \
		-f 6 \
		-p {threads} \
		--sensitive \
		--max-target-seqs 5 \
```

`Output`: data/intermediateData/Athaliana/Athaliana.blast

```
????
```

### DupGen_finder_diamond_outgroup
`Purpose`: This rule runs diamond blastp for the species against the outgroup species

> [!NOTE]
> The outgroup species in the config.yaml file is used for cross-genome comparison, which is useful for suggesting other types of duplicates.
`scripts`:
```
		mkdir -p {params.dir}; \
		diamond blastp \
		-d {params.db_name_dir} \
		-q {params.protein} \
		-o {params.out_name} \
		-e 1e-10 \
		-f 6 \
		-p {threads} \
		--sensitive \
		--max-target-seqs 5 \
```

`Output`: directory("data/intermediateData/Athaliana_DupGen_finder/")

```
#Athaliana_Creinhardtii.blast
????

```


## 3. [Snakefile_part2](../workflow/Snakefile_part2)

### prepare the gff for DupGen_finder
`Purpose`: This rule merge the gff files from species and the outgroup species into one (e.g., Athaliana_Creinhardtii.gff)

`scripts`:
```
	cp {input.gff} {params.dir2}/{params.species_name}.gff; \
	cp {params.dir1}/{params.species_name}.blast {params.dir2}/{params.species_name}.blast; \
	cp {params.dir3}/{params.outgroup_name}.gff {params.dir2}/{params.outgroup_name}.gff; \
	cp {params.dir3}/{params.outgroup_name}.blast {params.dir2}/{params.outgroup_name}.blast; \
	cp {params.dir5}/{params.out_name}.blast {params.dir2}/{params.out_name}.blast; \
	cat {params.dir1}/{params.species_name}.gff {params.dir2}/{params.outgroup_name}.gff \
> {params.dir2}/{params.out_name}.gff \
```

`Output`: data/DupGen_finder/Athaliana_data/Athaliana_Creinhardtii.gff

```
?????
```


### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> #####detecting WGD > tandem > proximal > transposed > dispersed duplicates #######
> # identify the different modes of duplicated gene pairs, https://github.com/qiao-xin/DupGen_finder/blob/master/DupGen_finder.pl

> [!WARNING]
> The mkCD.pl was adopted from MCScanX_protocol which is not exactly same (Wang, Yupeng, et al. Nature Protocols 19.7 (2024): 2206-2229.)


`scripts`:
```
	mkdir -p {params.dir5}; \
	sleep 30s; \
	perl {params.dir4}/DupGen_finder.pl \
	-i {params.dir2} \
	-t {params.species_name} \
	-c {params.outgroup_name} \
	-o {params.dir5} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```



### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```



### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```

### DupGen_finder_diamond
`Purpose`: This rule provides a convenient way to download the standard input files from NCBI. 

> [!NOTE]
> To avoid repeatly download the ".zip" files with the example file we provided ('HSDSnake_data.tar.gz'), we commented the rule in the snakefile.

`scripts`:
```
mkdir -p {params.dir};\
curl -OJX \
GET "{params.link}"; \
mv {params.file} {params.dir} \
```

`Output`: data/ncbi_download/GCF_000001735.4.zip

```
# standard input files from NCBI 
XX.genomic.gff
XX.protein.faa
XX.cds_from_genomic.fna
```


`Purpose`: 

`scripts`:
```


```

`Output`:

```

```
> [!NOTE]
> Since

> [!TIP]
> It is


> [!WARNING]
> To make



## 4. [Snakefile_part3](../workflow/Snakefile_part3)

### preprocess fasta
`Purpose`: This step is to generate a protein fasta file with short header line.

`scripts`: shell script
```
	mkdir -p {params.dir}; \
	awk '{{print $1}}' {input} \
```

`Output`: data/preprocess_fasta/Athaliana_thaliana.fa

```
>NP_001030613.1
MLLSALLTSVGINLGLCFLFFTLYSILRKQPSNVTVYGPRLVKKDGKSQQSNEFNLERLLPTAGWVKRALEPTNDEILSN
LGLDALVFIRVFVFSIRVFSFASVVGIFILLPVNYMGTEFEEFFDLPKKSMDNFSISNVNDGSNKLWIHFCAIYIFTAVV
```

> [!NOTE]
> Since amino acid substitutions occur less frequently than nucleotide substitutions, the sequence alignments are thereby generally evaluated by amino acid sequences instead of nucleotides, which allows a greater sensitivity (Koonin and Galperin, 2002). 

### diamond_db


`Purpose`: This step is to generate the local Diamond database

`scripts`: shell script
```
	diamond makedb \
		--in {input} \
		-d {params.db_name_dir} \
```

`Output`: results/Athaliana_thaliana/Athaliana_thaliana.dmnd

### diamond blastp
`Purpose`: This step is to generate local Diamond blastp all-against-all search which is quicker than BLAST.

`scripts`: shell script
```
		diamond blastp \
		-d {params.db_name_dir} \
		-q {input.protein} \
		-o {output} \
		-e 1e-10 \
		-f 6 \
		-p {threads} \
		--sensitive \
```

`Output`: results/Athaliana_thaliana/diamond/Athaliana_thaliana.txt

> [!NOTE]
> So we chose the protein sequence to do the Diamond blastp all-against-all search (Buchfink et al., 2015) (defaulted parameters: E-value cut-off ≤ 10-5, blastp -outfmt 6 etc.).

## interproscan
`Purpose`: This step is to generate the protein annotaion file by running interproscan search.

`scripts`: shell script
```
/interproscan.sh -i proteins_of_your_genome.fasta -f tsv -dp

```
`Output` : data/Athaliana_thaliana.interproscan.tsv

> [!Note]
> The InterProScan (Quevillon et al., 2005, Mitchell et al., 2019) and KEGG (Kanehisa and Goto, 2000b) are the only two dependencies without integrating into the HSDSnake pipeline due to the lack of Conda environment (the latest InterProScan Conda package of 5.59 fails in SnakeMake) and the limitation to web-only access in KEGG, such as BlastKOALA (Kanehisa et al., 2016)).

> [!TIP]
> It is straightforward to generate the InterProScan output by either checking the respective [ReadMe file](https://interproscan-docs.readthedocs.io/en/latest/) or following the [protocol](https://www.sciencedirect.com/science/article/pii/S2666166721003269) at Step 6-9.

> [!WARNING]
> To make sure the protein sequecne is consistent under different analysis, please use the preprocessed fasta to submit for the InterProScan search, i.e., the file under the directory: data/preprocess_fasta/Athaliana_thaliana.fa

## kegg blastkoala

`Purpose`: This step is to generate a KEGG functional category file.

`scripts`: local submission

`Output` :data/Athaliana_thaliana.ko.txt

> [!TIP]
> It is straightforward to generate the kegg blastkoala output by either checking the respective [website](https://www.kegg.jp/blastkoala/) or following the [protocol](https://www.sciencedirect.com/science/article/pii/S2666166721003269) at Step 17-20.

> [!WARNING]
> To make sure the protein sequecne is consistent under different analysis, please use the preprocessed fasta to submit for the KEGG Blastkoala search, i.e., the file under the directory: data/preprocess_fasta/Athaliana_thaliana.fa
 
## HSDfinder preprocess
`Purpose`: This step is to [debug the previous raised potential issue with using HSDFinder](https://github.com/zx0223winner/HSDFinder?tab=readme-ov-file#how-to-deal-with-error-require-length-of-gene-)

`scripts`: shell script
```
	(awk '/^>/{{if (l!="") print l; print; l=0; next}}{{l+=length($0)}}END{{print l}}' \
		{input.protein} \
		|paste - - \
		|sed 's/>//g' \
		|awk -F'\t' '{{print $1"\t"$1"\t"100"\t"$2}}' \
		|cat ;\
		cat {input.tabular}) \
		|cat \

```

`Output`: results/Athaliana_thaliana/diamond/Athaliana_thaliana.preprocess.txt
	
## hsdfinder
`Purpose`: This step is the main script to generate  HSDs with different thresholds. 

`scripts`: shell script
```
	hsdfinder \
		-i {input.tabular} \
		-p {params.identity} \
		-l {params.variance} \
		-f {input.Interproscan} \
		-t Pfam \
		-o {output} \

```

`Output`: [results/Athaliana_thaliana/hsdfinder/Athaliana_thaliana.90_10.txt](../results/Athaliana_thaliana/hsdfinder/Athaliana_thaliana.90_10.txt)

> [!TIP]
> [For the specific usage of HSDFinder tool, please find here](https://github.com/zx0223winner/HSDFinder?tab=readme-ov-file#3-running-hsdfinder)

## kegg category
`Purpose`: This step is to apply KEGG functional category on the detected HSDs. 

`scripts`: shell script
```
	python3 $PWD{params.dir}HSD_to_KEGG.py \
		-i {input.HSD_result} \
		-k {input.KEGG} \
		-n {params.species_name}\
		-o {output} \

```

`Output`: [results/Athaliana_thaliana/kegg/Athaliana_thaliana.90_10.kegg.txt](../results/Athaliana_thaliana/kegg/Athaliana_thaliana.90_10.kegg.txt)

> [!TIP]
> [For the specific usage of HSD_to_KEGG.py, please read here](https://github.com/zx0223winner/HSDSnake/blob/main/docs/Readme-2.md#5-creating-heatmap)
 
## hsdecipher statistcs

`Purpose`: This step is to calculate the statistics of HSDs via using a variety of HSDFinder thresholds.
https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher

`scripts`: shell script
```
	python3 $PWD{params.dir}HSD_statistics.py \
		{params.HSD_dir} \
		{params.HSD_file_format} \
		{output} \

```


`Output`: [results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.stat.txt](../results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.stat.txt)

> [!TIP]
> [For the specific usage of HSD_statistics.py, please read here](https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher)
 
## hsdecipher category
`Purpose`: This step is to count the number of HSD with two, three, and more than four categories, which is helpful to evaluate the distribution of groups in HSDs.

`scripts`: shell script
```
	python3 $PWD{params.dir}HSD_categories.py \
		{params.HSD_dir} \
		{params.HSD_file_format} \
		{output} \

```


`Output`: [results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.category.txt](../results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.category.txt)

> [!TIP]
> [For the specific usage of HSD_categories.py, please read here](https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher)
 
## hsdecipher merge statistics
`Purpose`: This step is to merge the above analysis.

`scripts`: shell script
```
	paste -d"\t" \
	{input.stat} \
	{input.category} \
	> {output} \

```

`Output`: [results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.complete.stats.txt](../results/Athaliana_thaliana/hsdecipher/stats/Athaliana_thaliana.complete.stats.txt)

 
## hsdecipher batch run
`Purpose`: This step can do a series of combination thresholds at once. To minimize the redundancy and to acquire a larger dataset of HSD candidates

`scripts`: shell script
```
	mkdir -p {params.HSD_batch_run_dir}/{params.species_name}; \
	cp {params.HSD_dir}/* {params.HSD_batch_run_dir}/{params.species_name}/; \
	python3 $PWD{params.dir}HSD_batch_run.py \
		-i {params.HSD_batch_run_dir}; \
	rm -r {params.HSD_batch_run_dir}/{params.species_name} \

```

`Output`: [results/Athaliana_thaliana/hsdecipher/batch_run/Athaliana_thaliana.batch_run.txt](../results/Athaliana_thaliana/hsdecipher/batch_run/Athaliana_thaliana.batch_run.txt)

> [!TIP]
> [For the specific usage of HSD_batch_run, please read here](https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher)
 
## hsdecipher heatmap intra species
`Purpose`: This step is able to visualize the collected HSDs in a heatmap and compare the HSDs sharing the same pathway function. This can be done inta-specise and inter-speies heatmaps.

`scripts`: shell script
```
	mkdir -p {params.HSD_heatmap_dir}/{params.species_name}; \
	mkdir -p {params.ko_dir}; \
	sleep 60s; \
	cp {input.KEGG} {params.ko_dir}/; \
	cp {params.HSD_dir}/* {params.HSD_heatmap_dir}/{params.species_name}/; \
	cp {params.batch_run} {params.HSD_heatmap_dir}/{params.species_name}/; \
	hsdecipher \
	-f {params.HSD_heatmap_dir}/{params.species_name} \
	-k {params.ko_dir} \
	-r {params.r} \
	-c {params.c}; \
	rm -r {params.ko_dir}; \
	rm -r {params.HSD_heatmap_dir}/{params.species_name}; \
	mv {params.heatmap} {params.HSD_heatmap_dir}; \
	mv {params.tabular} {params.HSD_heatmap_dir}; \

```

`Output`: results/Athaliana_thaliana/hsdecipher/heatmap/Athaliana_thaliana.output_heatmap.eps
![image](../results/Athaliana_thaliana/hsdecipher/heatmap/Athaliana_thaliana.output_heatmap.jpg)

> [!TIP]
> [For the specific usage of HSD_heatmap.py (i.e., hsdecipher), please read here](https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher)
			
## hsdecipher heatmap inter species	
`Purpose`: This step is able to visualize the collected HSDs in a heatmap and compare the HSDs sharing the same pathway function. This can be done inta-specise and inter-speies heatmaps.

`scripts`: shell script
```
		mkdir -p {params.HSD_heatmap_dir}; \
		mkdir -p {params.ko_heatmap_dir}; \
		sleep 30s; \
		cp {params.batch_run} {params.HSD_heatmap_dir}; \
		cp {input.KEGG} {params.ko_heatmap_dir}; \
		hsdecipher \
		-f {params.HSD_heatmap_dir}\
		-k {params.ko_heatmap_dir} \
		-r {params.r} \
		-c {params.c}; \
		mv {params.heatmap} {params.HSD_heatmap}||true; \
		mv {params.tabular} {params.HSD_heatmap}||true; \

```

`Output`: results/heatmap_inter/HSD/HSD.output_heatmap.eps
![image](../results/heatmap_inter/HSD.output_heatmap.jpg)

> [!TIP]
> [For the specific usage of HSD_heatmap.py (i.e., hsdecipher), please read here](https://github.com/zx0223winner/HSDecipher#2-whats-hsdecipher)

