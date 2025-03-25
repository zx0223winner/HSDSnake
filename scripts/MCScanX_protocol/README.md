cd /path/to/MCScanX_protocol

#download from NCBI
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000001735.4/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCF_000001735.4.zip" -H "Accept: application/zip"
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_019202805.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_019202805.1.zip" -H "Accept: application/zip"
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_905216605.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_905216605.1.zip" -H "Accept: application/zip"
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_911865555.2/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_911865555.2.zip" -H "Accept: application/zip"
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000695525.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCF_000695525.1.zip" -H "Accept: application/zip"
curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_016771965.1/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_016771965.1.zip" -H "Accept: application/zip"




curl -OJX GET "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCA_900416815.2/download?include_annotation_type=GENOME_FASTA,GENOME_GFF,RNA_FASTA,CDS_FASTA,PROT_FASTA,SEQUENCE_REPORT&filename=GCA_900416815.2.zip" -H "Accept: application/zip"


#move zip files to "ncbi_donwload"
mkdir ncbi_download
mv *.zip ./ncbi_download/

#move decompressed files to "ncbi"
kdir ncbi
cd ./ncbi_download/
unzip GCF_000001735.4.zip
mv ncbi_dataset/data/GCF_000001735.4/cds_from_genomic.fna ../ncbi/at_cds_from_genomic.fna
mv ncbi_dataset/data/GCF_000001735.4/genomic.gff ../ncbi/at_genomic.gff
mv ncbi_dataset/data/GCF_000001735.4/protein.faa ../ncbi/at_protein.faa
rm -fr ncbi_dataset/ README.md
unzip GCA_019202805.1.zip
mv ncbi_dataset/data/GCA_019202805.1/cds_from_genomic.fna ../ncbi/as_cds_from_genomic.fna
mv ncbi_dataset/data/GCA_019202805.1/genomic.gff ../ncbi/as_genomic.gff
mv ncbi_dataset/data/GCA_019202805.1/protein.faa ../ncbi/as_protein.faa
rm -fr ncbi_dataset/ README.md
unzip GCA_905216605.1.zip
mv ncbi_dataset/data/GCA_905216605.1/cds_from_genomic.fna ../ncbi/aa_cds_from_genomic.fna
mv ncbi_dataset/data/GCA_905216605.1/genomic.gff ../ncbi/aa_genomic.gff
mv ncbi_dataset/data/GCA_905216605.1/protein.faa ../ncbi/aa_protein.faa
rm -fr ncbi_dataset/ README.md
unzip GCA_911865555.2.zip
mv ncbi_dataset/data/GCA_911865555.2/cds_from_genomic.fna ../ncbi/ta_cds_from_genomic.fna
mv ncbi_dataset/data/GCA_911865555.2/genomic.gff ../ncbi/ta_genomic.gff
mv ncbi_dataset/data/GCA_911865555.2/protein.faa ../ncbi/ta_protein.faa
rm -fr ncbi_dataset/ README.md
unzip GCF_000695525.1.zip
mv ncbi_dataset/data/GCF_000695525.1/cds_from_genomic.fna ../ncbi/bo_cds_from_genomic.fna
mv ncbi_dataset/data/GCF_000695525.1/genomic.gff ../ncbi/bo_genomic.gff
mv ncbi_dataset/data/GCF_000695525.1/protein.faa ../ncbi/bo_protein.faa
rm -fr ncbi_dataset/ README.md
unzip GCA_016771965.1.zip
mv ncbi_dataset/data/GCA_016771965.1/cds_from_genomic.fna ../ncbi/bc_cds_from_genomic.fna
mv ncbi_dataset/data/GCA_016771965.1/genomic.gff ../ncbi/bc_genomic.gff
mv ncbi_dataset/data/GCA_016771965.1/protein.faa ../ncbi/bc_protein.faa
rm -fr ncbi_dataset/ README.md
cd ..

#build blastp databases
mkdir ncbiDB
makeblastdb -in ncbi/at_protein.faa -out ncbiDB/at -dbtype prot
makeblastdb -in ncbi/as_protein.faa -out ncbiDB/as -dbtype prot
makeblastdb -in ncbi/aa_protein.faa -out ncbiDB/aa -dbtype prot
makeblastdb -in ncbi/ta_protein.faa -out ncbiDB/ta -dbtype prot
makeblastdb -in ncbi/bo_protein.faa -out ncbiDB/bo -dbtype prot
makeblastdb -in ncbi/bc_protein.faa -out ncbiDB/bc -dbtype prot

#generate gff inputs
mkdir intermediateData
perl mkGFF3.pl

#run blastp. Users may consider to parallelize the blasp runs using queue systems
sh runBLASTP.sh
mv *.blastp intermediateData/

#combine gff and blast files
mkdir 6species
cat intermediateData/at.gff intermediateData/as.gff intermediateData/aa.gff intermediateData/ta.gff intermediateData/bo.gff intermediateData/bc.gff >6species/6species.gff
cat intermediateData/at-as.blast intermediateData/as-at.blast intermediateData/as-aa.blast intermediateData/aa-as.blast intermediateData/aa-ta.blast intermediateData/ta-aa.blast intermediateData/ta-bo.blast intermediateData/bo-ta.blast intermediateData/bo-bc.blast intermediateData/bc-bo.blast intermediateData/at.blast intermediateData/as.blast intermediateData/aa.blast intermediateData/ta.blast intermediateData/bo.blast intermediateData/bc.blast >6species/6species.blast

#run MCScanX
MCScanX 6species/6species

#visualize synteny using MCScanX tools
mkdir plots
cd /path/to/MCScanX/downstream_analyses/
java dual_synteny_plotter -g /path/to/MCScanX-protocol/6species/6species.gff -s /path/to/MCScanX-protocol/6species/6species.collinearity -c /path/to/MCScanX-protocol/6species/at-as.ctl -o /path/to/MCScanX-protocol/plots/at-as_synteny.png
java dot_plotter -g /path/to/MCScanX-protocol/6species/6species.gff -s /path/to/MCScanX-protocol/6species/6species.collinearity -c /path/to/MCScanX-protocol/6species/at-as.ctl -o /path/to/MCScanX-protocol/plots/at-as_dot.png
java circle_plotter -g /path/to/MCScanX-protocol/6species/6species.gff -s /path/to/MCScanX-protocol/6species/6species.collinearity -c /path/to/MCScanX-protocol/6species/at-as_circle.ctl -o /path/to/MCScanX-protocol/plots/at-as_circle.png
java bar_plotter -g /path/to/MCScanX-protocol/6species/6species.gff -s /path/to/MCScanX-protocol/6species/6species.collinearity -c /path/to/MCScanX-protocol/6species/at-as_bar.ctl -o /path/to/MCScanX-protocol/plots/at-as_bar.png

#make CIRCOS inputs
perl mkCircosInputs.pl 6species/6species.gff 6species/6species.collinearity

mkdir circosInput
mv 6species/6species.links circosInput/
mv 6species/6species.karyotype circosInput/

#classify gene duplication modes
duplicate_gene_classifier intermediateData/at

#calculate ka and ks
perl mkCD.pl
cat intermediateData/at.cds intermediateData/aa.cds intermediateData/bo.cds intermediateData/ta.cds intermediateData/bc.cds intermediateData/as.cds >6species/6species.cds
perl add_ka_and_ks_to_collinearity_Yn00.pl -i 6species/6species.collinearity -d 6species/6species.cds -o 6species/6species.kaks

#MCScanX-transposed
cd transposed

#download from https://phytozome-next.jgi.doe.gov
curl --cookie jgi_session=/api/sessions/2efaee06fc3c79d063b8993011ae57d0 --output download.20230814.142540.zip -d "{\"ids\":{\"Phytozome-673\":[\"605b8464a272c2ee75ae19dd\",\"605b8464a272c2ee75ae19db\",\"605b8465a272c2ee75ae19e0\"],\"Phytozome-523\":[\"5cf92242ee2d26b76f02476e\",\"5cf9223fee2d26b76f024766\",\"5cf92243ee2d26b76f024771\"],\"Phytozome-550\":[\"5d94206fc0d65a87debc85ab\",\"5d94206fc0d65a87debc85a9\",\"5d94206fc0d65a87debc85a4\"]}}" -H "Content-Type: application/json" https://files.jgi.doe.gov/filedownload/

unzip download.20230814.142735.zip

rm download.20230814.142735.zip Download_569772_File_Manifest.csv

rm -fr Phytozome/PhytozomeV13/

gunzip Phytozome/*.gz

mv Phytozome/Cdentata_673_v1.1.cds.fa cd_cds_from_genomic.fna
mv Phytozome/Cdentata_673_v1.1.gene.gff3 cd_genomic.gff
mv Phytozome/Cdentata_673_v1.1.protein.fa cd_protein.faa
mv Phytozome/Dalata_550_v2.1.cds.fa da_cds_from_genomic.fna
mv Phytozome/Dalata_550_v2.1.gene.gff3 da_genomic.gff
mv Phytozome/Dalata_550_v2.1.protein.fa da_protein.faa
mv Phytozome/Tcacao_523_v2.1.cds.fa tc_cds_from_genomic.fna
mv Phytozome/Tcacao_523_v2.1.gene.gff3 tc_genomic.gff
mv Phytozome/Tcacao_523_v2.1.protein.fa tc_protein.faa

mkdir PhytozomeDB

makeblastdb -in Phytozome/cd_protein.faa -out PhytozomeDB/cd -dbtype prot
makeblastdb -in Phytozome/da_protein.faa -out PhytozomeDB/da -dbtype prot
makeblastdb -in Phytozome/tc_protein.faa -out PhytozomeDB/tc -dbtype prot

perl mkGFF3.pl 

mkdir intermediateData
mv *.gff intermediateData/

mkdir input
cat intermediateData/tc.gff intermediateData/cd.gff >input/tc_cd.gff
cat intermediateData/tc.gff intermediateData/da.gff >input/tc_da.gff

sh runP.sh

mv *.blastp intermediateData/

cat intermediateData/tc-cd.blastp intermediateData/cd-tc.blastp >input/tc_cd.blast
cat intermediateData/tc-da.blastp intermediateData/da-tc.blastp >input/tc_da.blast
cp intermediateData/tc-tc.blastp input/tc.blast
cp intermediateData/tc.gff input/

perl /path/to/MCScanX-transposed/MCScanX-transposed.pl -i input -t tc -c cd,da -x 2 -o output

