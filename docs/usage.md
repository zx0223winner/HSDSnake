# HSDSnake: Usage<!-- omit in toc -->

## 1. [Config.yaml](../config.yaml) file 
You will need to edit the config.yaml file for your own usage. An [example config,yaml](../config.yaml) has been provided to test the pipeline.

> [!WARNING]
> please only substitute the species name to yours, keep the input file format, such as Arabidopsis_thaliana.fa, Arabidopsis_thaliana.interproscan.tsv, Arabidopsis_thaliana.ko.txt

``` conf.yaml
###### Here are the directories for fasta, interproscan, ko result you shall modify ######
samples:
  - Arabidopsis_thaliana
  - Chlamydomonas_reinhardtii

genomes:
  Arabidopsis_thaliana:
    proteins: "data/Arabidopsis_thaliana.fa"
    interproscan: "data/Arabidopsis_thaliana.interproscan.tsv"
    KEGG: "data/Arabidopsis_thaliana.ko.txt"

  Chlamydomonas_reinhardtii:
    proteins: "data/Chlamydomonas_reinhardtii.fa"
    interproscan: "data/Chlamydomonas_reinhardtii.interproscan.tsv"
    KEGG: "data/Chlamydomonas_reinhardtii.ko.txt"

####### Here are the directories for the custom scripts and parameters which do not need to modify #######
HSDFinder: 
  - "/scripts/hsdfinder/"

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

####### Feel free to tune these numbers for the heatmap hight and width #######

heatmap_hight: 20 
heatmap_width: 30

```

## 2. [Snakefile](../workflow/Snakefile)
### preprocess fasta
`Purpose`: This step is to generate 

`Example`: data/preprocess_fasta/Arabidopsis_thaliana.fa


### diamond_db
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/Arabidopsis_thaliana.dmnd

### diamond blastp
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/diamond/Arabidopsis_thaliana.txt

## interproscan
data/Arabidopsis_thaliana.interproscan.tsv

## kegg blastkoala

data/Arabidopsis_thaliana.ko.txt
 
## HSDfinder preprocess
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/diamond/Arabidopsis_thaliana.preprocess.txt
	
## hsdfinder
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdfinder/Arabidopsis_thaliana.90_10.txt

## kegg category
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/kegg/Arabidopsis_thaliana.90_10.kegg.txt
	
## hsdecipher statistcs
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdecipher/stats/Arabidopsis_thaliana.stat.txt
	
## hsdecipher category
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdecipher/stats/Arabidopsis_thaliana.category.txt
	
## hsdecipher merge statistics
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdecipher/stats/Arabidopsis_thaliana.complete.stats.txt
	
## hsdecipher batch run
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdecipher/batch_run/Arabidopsis_thaliana.batch_run.txt
	
## hsdecipher heatmap intra species
`Purpose`: This step is to generate 

`Example`: results/Arabidopsis_thaliana/hsdecipher/heatmap/Arabidopsis_thaliana.output_heatmap.eps
			
## hsdecipher heatmap inter species	
`Purpose`: This step is to generate 

`Example`: results/heatmap_inter/HSD/HSD.output_heatmap.eps



> [!WARNING]
> PLOTSR performs a sequence-wise (preferably chromosome-wise) synteny analysis. The order of the sequences for each assembly is inferred from its `synteny_labels` file and the order of sequences in the FASTA file is ignored. As all the assemblies are included in a single plot and the number of sequences from each assembly should be same, sequences after the common minimum number are excluded. Afterwards, the sequences are marked sequentially as `Chr1`, `Chr2`, `Chr3`,... If a label other than `Chr` is desirable, it can be configured with the `synteny_plotsr_seq_label` parameter.

> [!TIP]
> If you wish to share such profile (such as upload as supplementary material for academic publications), make sure to NOT include cluster specific paths to files, nor institutional specific profiles.

## Core Nextflow arguments

> [!NOTE]
> These options are part of Nextflow and use a _single_ hyphen (pipeline parameters use a double-hyphen).

