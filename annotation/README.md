# Protein gene annotation of *Insectozyma corydali* genome

## Files and folders

### Augustus parameters

* `annot-canVer1`: Augustus parameters for *Insectozyma verbasci* genome, created as described in [Brejová et al., 2023](https://doi.org/10.1128/mra.00005-23)
* `au-2-train`: Augustus parameters after training on supported genes from `au-1-p.gtf`
* `au-3-train`: Augustus parameters after training on supported genes from `au-2-p.gtf`

### Configuration files

* `au-1.cfg`
* `au-2.cfg`
* `au-3.cfg`

The first line contains species name within Augustus parameter folder, the second line contains the path to the Augustus parameter folder, and the third line contains the filename used for training (if applicable).

### Augustus predictions

* `au-1-p.gtf`: obtained using `annot-canVer1` parameters and protein hints from *I. verbasci*
* `au-2-p.gtf`: obtained using `au-2-train` parameters and protein hints
* `au-3-p.gtf`: obtained using `au-3-train` parameters and protein hints

### Lists of supported genes used for training

* `au-1-p-supProt.list`: subset of genes from `au-1-p.gtf` supported by *I. verbasci* proteins
* `au-2-p-supProt.list`: subset of genes from `au-2-p.gtf` supported by *I. verbasci* proteins

### Augustus training logs

* `au-2-train.log`
* `au-3-train.log`

### Protein hints for Augustus

* `miniprot.hints-prot.fa`: alias for *I. verbasci* proteins used for Augustus hints
* `miniprot.hints-prot.gtf`: *I. verbasci* proteins aligned to the genome using miniprot
* `miniprot.hints.gff`: GFF3 file with hints for Augustus obtained from `miniprot.hints-prot.gtf`

### Proteins used for selecting supported genes

* `other-prot.fa`: alias for *I. verbasci* proteins used for Augustus hints

### Final gene set used for submission

This set was obtained from `au-3-p.gtf` after renaming, omitting genes from `omit-genes1.list` and adding mitochondrial genes from Genbank sequence KC993198.

* `genes1-prot.fa`: final set of proteins 
* `genes1.gtf`: final set of genes 
* `omit-genes1.list`: contains IDs of genes from `au-3-p.gtf` that were omitted. % genes because of in0frame stop codons and 5 genes encoded by mitochondrial DNA, as Augustus model is not trained for mitochondrial genomes. 

## Commands used

```bash
# prepare protein hints by miniprot alignment
assembly-scripts/annot miniprot.hints.gff
# run Augustus with protein hints and I. verbascii parameters
assembly-scripts/annot au-1-p-prot.fa --config GENETIC_CODE=12
# prepare training dataset with supported genes
assembly-scripts/annot au-1-p-supProt-single.train.gb 
# run Augustus training
assembly-scripts/annot au-2-train
# run Augustus with protein hints and au-2-train parameters
assembly-scripts/annot au-2-p-prot.fa --config GENETIC_CODE=12
# prepare training dataset with supported genes
assembly-scripts/annot au-2-p-supProt-single.train.gb 
# run Augustus training
assembly-scripts/annot au-3-train
# run Augustus with protein hints and au-3-train parameters
assembly-scripts/annot au-3-p-prot.fa --config GENETIC_CODE=12
```