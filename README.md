[![Snakemake](https://img.shields.io/badge/snakemake-≥5.7.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![run with conda ](http://img.shields.io/badge/run%20with-conda%20-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)

## Introduction

**HSDSnake** is a [SnakeMake](https://snakemake.readthedocs.io) pipeline for comprehensive analysis of highly similar duplicates in genomes. The tools are shown in the [Pipeline Flowchart](#pipeline-flowchart) and their references are listed in [Citations.md](/docs/Citations.md).

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
  
  PREPARE((PREPARE)) ==> preprocess_fasta[preprocess_fasta]
  PREPARE ==> diamond_db[diamond_db]
  PREPARE ==> diamond[ diamond]
  PREPARE ==> KEGG[KEGG]

  preprocess_fasta ==> DETECT
  diamond_db ==> DETECT
  diamond ==> DETECT


  DETECT((DETECT)) ==> HSDFinder_preprocess[HSDFinder_preprocess]
  DETECT ==> HSDFinder[HSDFinder]
  

  HSDFinder_preprocess ==> CURATE
  HSDFinder ==> CURATE
  
  subgraph Automatically_combined
   CURATE((CURATE)) ==> HSDecipher_batch_run[HSDecipher_batch_run]
  end
  HSDecipher_batch_run ==> STATISTICS

  STATISTICS((STATISTICS)) ==> HSDecipher_statistics[HSDecipher_statistics]
  STATISTICS ==> HSDecipher_category[HSDecipher_category]
  STATISTICS ==> merge_stastics[merge_statistics]

  HSDecipher_statistics ==> VISUALIZE_and_COMPARE
  HSDecipher_category ==> VISUALIZE_and_COMPARE
  merge_statistics ==> VISUALIZE_and_COMPARE

  VISUALIZE_and_COMPARE ==> HSDecipher_heatmap_inter_species_prepare[heatmap_inter_species]
  VISUALIZE_and_COMPARE ==> HSDecipher_heatmap_intra_species[heatmap_intra_species]



```

## Usage

Refer to [usage](./docs/usage.md), [parameters](./docs/parameters.md) and [output](./docs/output.md) documents for details.

> [!NOTE]
> If you are new to Snakmake, please refer to [this page](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) on how to set-up SnakeMake. Make sure to test the sample data below before running the workflow on actual data.

```
# Test if you have successfully installed the SnakeMake
mamba activate snakemake
snakemake --help
```


Prepare an `config.yaml` file with following columns representing input files for HSDSnake, please only substitute the species name to yours, keep the input file format, such as Arabidopsis_thaliana.fa, Arabidopsis_thaliana.interproscan.tsv, Arabidopsis_thaliana.ko.txt.

```
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
```

Now, you can run the pipeline using the following commands:

```
# Download the package
git clone https://github.com/zx0223winner/HSDSnake.git

# enter the working directory
cd HSDSnake
```
> [!NOTE]
>Due to the size of sample files, please download the test data - `HSDSnake_data.tar.gz` through the [link](https://drive.google.com/file/d/15jGPsKRUn_SzXmaIAdXEQcxrychX-d9a/view?usp=sharing)

```
# Then decompress the file HSDSnake_data.tar.gz under the HSDSnake directory,
# This will bring you a data folder with test files ready 
tar -xvzf HSDSnake_data.tar.gz

# Then you can give a dry run by the following command.
snakemake --use-conda --cores all -n

# If everthing is OK, then you can test the pipeline by running:
snakemake --use-conda --cores all
```

![image](resources/snakemake_screenshot.png)




