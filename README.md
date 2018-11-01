## Clustering of Arabidopsis genomes using t-SNE and GTM (Generative Topographic Mapping)

### Requirements
The following python packages are required:
* ugtm 
* sklearn
* altair
* pycountry
* matplotlib
* h5py
* numpy
* pandas

### Files in directory
* country_convert.py: Python script, converts country codes to country names
* worldmap_arabidopsis_admixed.py: Python script, creates interactive GTM and t-SNE maps with Admixed groups
* worldmap_arabidopsis_admixed.py: Python script, creates interactive GTM and t-SNE maps with countries 
* h5_arabidopsis.py: Python script, selects filtered genotypes from h5py imputed SNP matrix
* runGTM.py: runs GTM (using ugtm package) or t-SNE (using sklearn)
* output_viz: directory, contains html visualizations of worldmap_arabidopsis_admixed.py and worldmap_arabidopsis_admixed.py
* data: directory, contains csv data files 
* data/1001G_gen.csv: csv file, selected pruned genotypes from 1001G Project data (MAF 0.05) 
* data/1001G_snpids.csv: csv file, selected pruned SNPs from 1001G Project data (MAF 0.05)
* data/dataframe_1001G.csv: csv file, 1001G project dataframe with corresponding t-SNE and GTM coordinates 

### Create plink files from 1001 Genomes Project
* Download [1001genomes_snp-short-indel_only_ACGTN.vcf.gz](https://1001genomes.org/data/GMI-MPI/releases/v3.1/1001genomes_snp-short-indel_only_ACGTN.vcf.gz), the 1135 Arabidopsis thaliana genomes rom the 1001 Genomes Project.
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
* Download the imputed SNP matrix (h5py file) from the 1001 Genomes Project [1001genomes_snp-short-indel_only_ACGTN.vcf.gz](https://1001genomes.org/data/GMI-MPI/releases/v3.1/SNP_matrix_imputed_hdf5/1001_SNP_MATRIX.tar.gz)  
* Python script to generate csv from pruned SNPs and the SNP matrix:
```
python h5_arabidopsis.py
```
* Output genotype csv file = 1001G_gen.csv
* Output SNP ids = 1001G_snpids.csv
* Final number of pruned SNPs in 1001G_gen.csv = 28775 


## Generate GTM, t-SNE and PCA coordinates for the 1135 genomes:
Our runGTM.py script requires python packages [ugtm](https://github.com/hagax8/ugtm) (GTM implementation) and sklearn (t-SNE implementation).
* GTM (with "estimated priors" option for imbalanced classes), output = out_gtm_matmeans.csv:
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
```
python runGTM.py --model t-SNE \\
--data 1001G_gen.csv --labels continents.csv --labeltype discrete \\
--out out --pca --n_components 20 \\
--random_state 8 --verbose 
```
* PCA, output = out_pca.csv:
```
python runGTM.py --model PCA --data 1001G_gen.csv \\
--labels country_groups --labeltype discrete \\
--out out --pca  --random_state 8
```

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
t-SNE and GTM maps coloured by admixed group (result in output_viz folder):
```
python worldmap_arabidopsis_admixed.py data/dataframe_1001G.csv outputname 
```
t-SNE and GTM maps coloured by countries (result in output_viz folder):
```
python worldmap_arabidopsis_countries.py data/dataframe_1001G.csv outputname
```
