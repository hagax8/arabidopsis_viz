import h5py
import numpy
import numpy as np


# this is the imputed SNP matrix provided by the 1001G project
f = h5py.File('1001_SNP_MATRIX/imputed_snps_binary.hdf5', 'r')

# this is the list of SNPs after filters
# (genotyping rate 0.2 and
# pruning/MAF settings = --indep-pairwise 100 10 0.1 --maf 0.05)
listofsnps = np.genfromtxt('1001G_MAF0.05.prune.in', dtype="str")

# Get all SNP positions for all chromosomes
positions = f['positions'][:]
snps = f['snps'][:]
print(positions.shape)

# Array of tuples with start/stop indices for each chromosome
chr_regions = f['positions'].attrs['chr_regions']

# Initialize arrays to hold indices and positions
chrs = [1, 2, 3, 4, 5]
indices = []
positions_chr = []
positions_all = []
genotypes = []
position = []
ix = []

# The positions in the h5py files are NOT associated with chromosome number
# so we need to retrieve the indices to delimit the 5 chromosomes
for i in chrs:
    indices.append(chr_regions[i-1])

# Convert positions to chr:position format so we can find the intersection
# with the pruned list
count = 0
for i in chrs:
    positions_chr = [str(i)+":"+str(position)
                     for position in
                     positions[indices[i-1][0]:indices[i-1][1]]]
    if count == 0:
        positions_all = positions_chr
    else:
        positions_all = np.append(positions_all, positions_chr)
    count += 1

ix = numpy.where(numpy.isin(positions_all, listofsnps))

# Save genotype of selected snps
ix = np.array(ix, dtype=int)
count = 0

for i in ix:
    if count == 0:
        genotypes = snps[i]
    else:
        genotypes = np.vstack((genotypes, snps[i]))
    count += 1

# Save SNP names (final number of variables =
# intersection between provided list of snps and the snps in the h5 matrix)
count = 0
for i in ix:
    if count == 0:
        position = positions_all[i]
    else:
        position = np.vstack((position, positions_all[i]))
    count += 1

# Save final genotype matrix
np.savetxt("1001G_gen.csv", np.transpose(genotypes), delimiter=',', fmt="%s")

# Save final SNP ids
np.savetxt("1001G_snpids.csv", np.transpose(position), delimiter=',', fmt="%s")
