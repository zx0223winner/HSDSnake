[![Snakemake](https://img.shields.io/badge/snakemake-≥5.7.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![run with conda ](http://img.shields.io/badge/run%20with-conda%20-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)

### HSDSnake - a pipeline for comprehensive analysis of highly similar duplicates in genomes

```


#- Usage: snakemake --profile default all
# fastqc
# trim-cutadapt
# fastqc
# align-samtools, star, bedtools,
# mark duplicates - picard

#snakemake --profile default all
#snakemake --use-conda --cores all
#/storage/proj/expr_train
#/storage/proj/pea_genome/cram/analyses/proseq_02

#snakemake commom errors: 
#1. wild card not for all in a rule, 
#2. the output name doesnot match 
#3. symbols error e.g., missing , 
#4 the requirement of the resources are not enough 
#5.the input file is wrong


# configfile: "Metru-A17-Leaflet_config.yaml"

```

![HSDSnake Flowchart](https://github.com/zx0223winner/HSDSnake/blob/main/resources/dag.jpg)

Data folder: https://drive.google.com/file/d/15jGPsKRUn_SzXmaIAdXEQcxrychX-d9a/view?usp=sharing
