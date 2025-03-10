[![Snakemake](https://img.shields.io/badge/snakemake-≥5.7.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![run with conda ](http://img.shields.io/badge/run%20with-conda%20-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)

## Introduction

**HSDSnake** is a [SnakeMake](https://snakemake.readthedocs.io) pipeline for comprehensive analysis of highly similar duplicates (HSDs) in genomes. The tools are shown in the [Pipeline Flowchart](#pipeline-flowchart) and their references are listed in [Citations.md](/docs/Citations.md).

## Pipeline Flowchart

```mermaid
%%{init: {
    'theme': 'base',
    'themeVariables': {
    'fontSize': '18px",
    'primaryColor': '#9A6421',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#9A6421',
    'lineColor': '#B180A8',
    'secondaryColor': '#455C58',
    'tertiaryColor': '#ffffff'
  }
}}%%
flowchart TD

subgraph SnakeMake_Part_1-2
  PREPARE((PREPARE)) ==> McScanX[McScanX]
  PREPARE ==> diamond_db[diamond_db]
  PREPARE ==> diamond[diamond]
  PREPARE ==> Data_preprocessing[Data_preprocessing]
  PREPARE ==> KEGG[KEGG]

  McScanX ==> DupGen_finder
  diamond_db ==> DupGen_finder
  diamond ==> DupGen_finder
  Data_preprocessing ==> DupGen_finder


  DupGen_finder((DupGen_finder)) ==> HSDFinder_preprocess[HSDFinder_preprocess]
  DupGen_finder ==> HSDFinder[HSDFinder]

end  

subgraph SnakeMake_Part_3
  HSDFinder_preprocess ==> CURATE
  HSDFinder ==> CURATE
  

  CURATE((CURATE)) ==> HSDecipher_batch_run[HSDecipher_batch_run]
 
  HSDecipher_batch_run ==> STATISTICS

  STATISTICS((STATISTICS)) ==> HSDecipher_statistics[HSDecipher_statistics]
  STATISTICS ==> HSDecipher_category[HSDecipher_category]
  STATISTICS ==> merge_stastics[merge_statistics]

  HSDecipher_statistics ==> VISUALIZE_and_COMPARE
  HSDecipher_category ==> VISUALIZE_and_COMPARE
  merge_statistics ==> VISUALIZE_and_COMPARE

  VISUALIZE_and_COMPARE ==> HSDecipher_heatmap_inter_species_prepare[heatmap_inter_species]
  VISUALIZE_and_COMPARE ==> HSDecipher_heatmap_intra_species[heatmap_intra_species]
end


```

## Usage

Refer to [Usage](./docs/Usage.md) documents for details.

> [!NOTE]
> If you are new to Snakmake, please refer to [this page](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) on how to set-up SnakeMake. Make sure to test the sample data below before running the workflow on actual data.

```
# Test if you have successfully installed the SnakeMake
mamba activate snakemake
snakemake --help
```


Prepare an `config.yaml` file with following columns representing input files for HSDSnake. For demonstration, NCBI data of *A. thaliana* and *C. reinhardtii* have been used as examples, please only substitute the species name to yours, keep the input file format, such as Arabidopsis_thaliana.fa, Arabidopsis_thaliana.interproscan.tsv, Arabidopsis_thaliana.ko.txt. Note: The outgroup species in the config.yaml file is used for cross-genome comparison.

```
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
    
    Creinhardtii:
        ncbi_assembly: "data/ncbi_download/GCF_000002595.2.zip"
        assembly_id: "GCF_000002595.2"
        outgroup: "Athaliana"
        interproscan: "data/Creinhardtii.interproscan.tsv"
        KEGG: "data/Creinhardtii.ko.txt"

```

Now, you can run the pipeline using the following commands:

```
# Download the package
git clone https://github.com/zx0223winner/HSDSnake.git

# enter the working directory
cd HSDSnake
```
> [!NOTE]
>Due to the size of sample files, please download the test data - `HSDSnake_data.tar.gz` through the Google drive [link](https://drive.google.com/file/d/1d-yYkrp4Ce-zN9_s8VGpOO35hpkiu69w/view?usp=sharing)

```
# Then decompress the file HSDSnake_data.tar.gz under the HSDSnake directory,
# This will bring you a data folder with test files ready 
tar -xvzf HSDSnake_data.tar.gz

# Then you can give a dry run by the following command.
snakemake --use-conda --cores all -s workflow/Snakefile_part1 -n

# If everthing is OK, then you can test the pipeline by running one after another:
snakemake --use-conda --cores all -s workflow/Snakefile_part1
snakemake --use-conda --cores all -s workflow/Snakefile_part2
snakemake --use-conda --cores all -s workflow/Snakefile_part3
```
#### Snakemake_part 1-2
![image](resources/snakemake_part1-2.png)
#### Snakemake_part3
![image](resources/snakemake_part3.png)


