[![Snakemake](https://img.shields.io/badge/snakemake-≥5.7.0-brightgreen.svg)](https://snakemake.readthedocs.io)
[![run with conda ](http://img.shields.io/badge/run%20with-conda%20-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)

## Introduction

**HSDSnake** is a [SnakeMake](https://snakemake.readthedocs.io) pipeline for comprehensive analysis of highly similar duplicates (HSDs) in genomes.

- Gene duplicates are categorized into different categories (e.g., dispersed (DD), proximal (PD), tandem (TD), transposed (TRD), and whole genome duplication (WGD))
- Perform the analysis with reliance on sequence similarity (diamond blast all-vs-all), structional annotation (.gff3) and functional annotation (InterPRO, Pfam, KEGG, etc.).
- Detected gene duplicates can be visualized within a KEGG functional pathway framework and the substitution rates (Ka, Ks, and their Ka/Ks ratio) can be analyzed for all the duplicate gene pairs. 
- The tools are shown in the Pipeline Flowchart with [Detailed Usage](./docs/Usage.md) for each step and their references are listed in [Citations.md](/docs/Citations.md).

*Zhang et al. "HSDSnake: a user-friendly SnakeMake pipeline for analysis of duplicate genes in eukaryotic genomes." Bioinformatics (2025): btaf325. https://doi.org/10.1093/bioinformatics/btaf325*
## 
> [!NOTE]
> **[Listing of historic resources](/docs/Citations.md)** 
2020. **HSDFinder** - an interative web tool for gene duplicates classification and visualization. *(Zhang et al. 2021, Frontiers in Bioinformatics)*  http://hsdfinder.com 
2. **HSDFinder protocol** - a hands-on protcol for the step-by-step guide using HSDFinder. *(Zhang et al. 2021, StarProtocols (Cell Press))*
3. **HSDatabase** - an online database for gene duplicates from around forty species in animal and plant genomes with built-in blast feature, NCBI genome browser, gene copy comparision in KEGG and Pfam. *(Zhang et al. 2022, Database (Oxford Press))* http://hsdfinder.com/database
4. **Review for the duplication tools** - A mini-review of online resources for intra-species detection of gene duplications. *(Zhang et al. 2022, Frontiers in Genetics)*
4. **HSDecipher** - an updated protocol for downstream analysis of gene duplicates. *(Zhang et al. 2023, StarProtocols (Cell Press))*
5. **HSDSnake** - a Snakemake pipeline tool for classifying duplicate pairs, computing Ka/Ks ratios and function comparison (such as PFAM, KEGG etc.) from inter- and intra-species. It not only integrates tools developed previously, namely the resources as described above, but also integrates scripts from other recently developed methods and tools, such as DupGen_finder and MCScanX. *(Zhang et al. 2025, Bioinformatics (Oxford Press))*




## [Pipeline Flowchart](resources/pipeline.md)
![](resources/HSDSnake_workflow.png)

## Usage

Refer to [Usage](./docs/Usage.md) documents for details.

> [!NOTE]
> If you are new to Snakmake, please refer to [this page](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html) on how to set-up SnakeMake. Make sure to test the example data below before running the workflow on your data.

```
# Test if you have successfully installed the SnakeMake
mamba activate snakemake
snakemake --help
```

> [!NOTE]
> Begin with a `config.yaml` file as below (detailed all the input files requested for hsdsnake).
> 
> For demonstration, NCBI assemblies of *A. thaliana* and *C. reinhardtii* are used as examples, please only substitute the species name to yours in the below config.yaml file, keep the input file format, such as Arabidopsis_thaliana.fa, Arabidopsis_thaliana.interproscan.tsv, Arabidopsis_thaliana.ko.txt.
>
> The outgroup species in the config.yaml file is useful for suggesting other types of duplicates.

## Arguments
**config.yaml**
```config.yaml
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
        feature_table: "data/ncbi_download/GCF_000001735.4_TAIR10.1_feature_table.txt.gz"
    Creinhardtii:
        ncbi_assembly: "data/ncbi_download/GCF_000002595.2.zip"
        assembly_id: "GCF_000002595.2"
        outgroup: "Athaliana"
        interproscan: "data/Creinhardtii.interproscan.tsv"
        KEGG: "data/Creinhardtii.ko.txt"
        feature_table: "data/ncbi_download/GCF_000002595.2_Chlamydomonas_reinhardtii_v5.5_feature_table.txt.gz"
```

> [!NOTE]
> Optional: To add new species, users can simply put extra lines of species name, ncbi_assembly id and required files in the `config.yaml` file as above.
>
> The ncbi_assembly (e.g., GCF_000001735.4.zip) contains the standard genomic files from NCBI such as gff3, cds, protein.fa. The other two files XX.interproscan.tsv and XX.ko.txt can be acquried from dependencies which was [detailed here in the usage](./docs/Usage.md).

> [!NOTE]
> Optional: To download extra ncbi assembly 'XX.zip' from NCBI, users can substitue the ncbi_assembly id (e.g., GCF_000001735.4) with yours in the command below:

```
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000001735.4/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCF_000001735.4.zip"

```
## Running

Now, you can run the pipeline using the following commands:

```
# Download the package
git clone https://github.com/zx0223winner/HSDSnake.git

# enter the working directory
cd HSDSnake
```
> [!NOTE]
>Due to the size of sample files (we have prepared users with the standard input files of NCBI genome assemblies for *A. thaliana* and *C. reinhardtii* ), please download the test data - `HSDSnake_data.tar.gz` through the Google drive [link](https://drive.google.com/file/d/12vn4PqowWs2ug9WWiUNkDI-vzYOUhEgt/view?usp=sharing)

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
#### [Snakemake_part 1](resources/snakemake_part1.png)
#### [Snakemake_part 2](resources/snakemake_part2.png)
#### [Snakemake_part 3](resources/snakemake_part3.png)

## Dependencies

    1. Data Processing: Diamond, InterProscan, KEGG_BlastKOALA, McScanX_protocol, DupGen_finder, McScanX, HSDFinder, HSDecipher
    2. Python modules: pandas v1.5.3, scikit-learn, scipy, matplotlib, numpy
    3. Perl modules: perl-bioperl v1.7.8

Test conda environment: diamond v2.1.11, mcscanx v1.0.0, HSDFinder v1.0, HSDecipher v1.0, bedops v2.4.39

### Links to the Dependencies:
 
 1. Pfam 37.0 (Sep 2024, 21,979 entries): https://pfam.xfam.org
 2. InterPro 101.0 (Jul 2024, 45,899 entries):http://www.ebi.ac.uk/interpro/
 3. KEGG Orthology Database: https://www.genome.jp/kegg/ko.html
 4. InterProscan: https://github.com/ebi-pf-team/interproscan
 5. KEGG : https://www.kegg.jp/kegg/
 6. Diamond: https://github.com/bbuchfink/diamond
 7. McScanX_protocol: http://bdx-consulting.com/mcscanx-protocol/
 8. DupGen_finder: https://github.com/qiao-xin/DupGen_finder/tree/master
 9. McScanX: https://github.com/wyp1125/MCScanX

> [!NOTE]
> Environment files (.yaml) have already been set up in directory: `workflow/envs/` except `InterProScan` and `KEGG`.

                        
## Stargazers over time
[![Stargazers over time](https://starchart.cc/zx0223winner/HSDSnake.svg?background=%23FFFFFF&axis=%23e7a41e&line=%23e76060)](https://starchart.cc/zx0223winner/HSDSnake)

                    


