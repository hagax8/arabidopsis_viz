### Create plink files from 1001 Genomes Project
* Download [vcf file from the 1001 Genomes Project](https://1001genomes.org/data/GMI-MPI/releases/v3.1/1001genomes_snp-short-indel_only_ACGTN.vcf.gz).
* This project gathers 1135 Arabidopsis genomes
* Prune SNPs + apply genotyping rate and MAF filters:
```
plink --snps-only --geno 0.2 \\
--vcf 1001genomes_snp-short-indel_only_ACGTN.vcf.gz \\
--out 1001G --make-bed
```
```
plink --bfile 1001G --indep-pairwise 100 10 0.1 \\
--maf 0.05 --out 1001G_MAF0.05 \\
--set-missing-var-ids @:# --make-bed
```

## Create csv file for pruned SNPs: 
* Download [the imputed SNP matrix (h5py file) from the 1001 Genomes Project](https://1001genomes.org/data/GMI-MPI/releases/v3.1/SNP_matrix_imputed_hdf5/1001_SNP_MATRIX.tar.gz)  
* Python script to generate csv from pruned SNPs and the SNP matrix:
```
python h5_arabidopsis.py
```
* Output genotype csv file = 1001G_gen.csv
* Output SNP ids = 1001G_snpids.csv
* Final number of pruned SNPs in 1001G_gen.csv = 28775 


## Generate GTM, t-SNE and PCA coordinates for the 1135 genomes:
Using [runGTM.py](https://github.com/hagax8/ugtm/blob/master/bin/runGTM.py) programme (calls python package ugtm for GTM, sklearn for t-SNE):
* GTM (estimated priors option for imbalanced classes), output = out_gtm_matmeans.csv:
```
python runGTM.py --model GTM --data 1001G_gen.csv \\
--labels countrynames.csv --labeltype discrete \\
--out out_tsne \\
--pca --n_components 20 --grid_size 25 \\
--rbf_grid_size 5 \\
--random_state 8 \\
--verbose --prior estimated
```
* t-SNE, output = out_tsne.csv:
python runGTM.py --model t-SNE \\
--data 1001G_gen.csv --labels continents.csv --labeltype discrete \\
--out out --pca --n_components 20 \\
--random_state 8 --verbose 
* PCA, output = out_pca.csv:
python runGTM.py --model PCA --data 1001G_gen.csv \\
--labels country_groups --labeltype discrete \\
--out out --pca  --random_state 8

## Script to convert country codes to country names and continents:
python country_convert.py the_codes_to_convert

## Final pandas dataframe
* File name: dataframe_1001G.csv
* Variables:
```
accession
name
CS number
country code
latitude
longitude
collector
seq by
continent
country
admixed group
site
GTM axis 1
GTM axis 2
t-SNE axis 1
t-SNE axis 2
Principal component 1
Principal component 2   
```

## Generate interactive visualizations with world map:
worldmap_arabidopsis_admixed.py
worldmap_arabidopsis_countries.py
