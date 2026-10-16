# Commands for read processing, assembly and BUSCO analysis

## Read processing

```bash
# basecalling
# dorado v1.0.1
dorado-1.0.1-osx-arm64/bin/dorado basecaller sup pod5/ > sample.bam
# samtools v1.22
samtools fastq sample.bam | gzip > sample.fastq.gz 

# filtering nanopore reads
# Nanofilt v2.8.0
gunzip -c sample.fastq.gz | NanoFilt -q 20 -l 1000 --maxlength 100000 --headcrop 40 --tailcrop 40 | gzip > sample.filtered.fastq.gz 

# downsampling nanopore reads
# rasusa v4.0.0
rasusa reads sample.filtered.fastq.gz -c 100 -g 11.5m -o sample.filtered.downsampled.fastq.gz

# Illumina read trimming
# Trimmomatic v0.39
java -jar trimmomatic-0.39.jar PE reads_1.fastq.gz reads_2.fastq.gz reads_1.paired.fastq.gz reads_1.unpaired.fastq.gz reads_2.paired.fastq.gz reads_2.unpaired.fastq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:keepBothReads LEADING:3 TRAILING:3 MINLEN:36
```

## Assembly and polishing

```
# genome assembly
# hifiasm v0.25.0-r726
hifiasm --ont -f0 -o sample -t 16 sample.filtered.downsampled.fastq.gz
awk '/^S/{print ">"$2"\n"$3}' sample_hifiasm.bp.p_ctg.gfa > sample_hifiasm.fasta

# assembly polishing with Illumina reads   
# pilon v1.24, bwa mem v0.7.19-r1273, samtools v1.22
# Round 1
bwa index sample_hifiasm.fasta
bwa mem -t 16 sample_hifiasm.fasta reads_1.paired.fastq.gz reads_2.paired.fastq.gz | samtools sort -@16 -o sample_hifiasm.mapping1.sorted.bam
samtools index sample_hifiasm.mapping1.sorted.bam
pilon -Xmx32G --genome sample_hifiasm.fasta --frags sample_hifiasm.mapping1.sorted.bam --output sample_hifiasm.pilon1 --fix all --changes
# Round 2
bwa index sample_hifiasm.pilon1
bwa mem -t 16 sample_hifiasm.pilon1 reads_1.paired.fastq.gz reads_2.paired.fastq.gz | samtools sort -@16 -o sample_hifiasm.mapping2.sorted.bam
samtools index sample_hifiasm.mapping2.sorted.bam
pilon -Xmx32G --genome sample_hifiasm.pilon1 --frags sample_hifiasm.mapping2.sorted.bam --output sample_hifiasm.pilon2 --fix all --changes
```

## mtDNA assembly and annotation

Circular mtDNA monomer was obtained as follows: trimmed Illumina reads were assembled using SPAdes 4.2.0 (REF1) with `--isolate` option:
```
spades.py --isolate -m 512 -t16 -1 reads_1.paired.fastq.gz -2 reads_2.paired.fastq.gz -o out_dir
```

A 46,466 bp long contig corresponding to mtDNA was identified by blastn (REF2) using the I. verbasci mtDNA (GB acc.no. [OK589855](https://www.ncbi.nlm.nih.gov/nuccore/OK589855)) as query. A 77-bp overlap was removed from the right end. The resulting contig was circularized and rotated to position 3787 to start with the gene nad2. Annotation was performed using MFannot (REF3).

The hifiasm assembly produced from nanopore reads as shown above contained a contig of length 290,284bp with over 6 tandem copies of mtDNA, as well as multiple mtDNA fragments.

REF1: Prjibelski, A., Antipov, D., Meleshko, D., Lapidus, A. and Korobeynikov, A., 2020. Using SPAdes de novo assembler. Current protocols in bioinformatics, 70(1), p.e102. doi: [10.1002/cpbi.102](https://doi.org/10.1002/cpbi.102)

REF2: Camacho C, Coulouris G, Avagyan V, Ma N, Papadopoulos J, Bealer K, Madden TL. BLAST+: architecture and applications. BMC Bioinformatics. 2009; 10:421. doi: [10.1186/1471-2105-10-421](https://doi.org/10.1186/1471-2105-10-421)

REF3: Lang BF, Beck N, Prince S, Sarrasin M, Rioux P, Burger G. Mitochondrial genome annotation with MFannot: a critical analysis of gene identification and gene model prediction. Front Plant Sci. 2023;14:1222186. doi: [10.3389/fpls.2023.1222186](https://doi.org/10.3389/fpls.2023.1222186)


## BUSCO analysis

```
# BUSCO v.5.1.2
docker run -u $(id -u) -v $(pwd):/busco_wd ezlabgva/busco:v5.1.2_cv1 busco -i assembly.fasta -o assembly_out -m genome -l saccharomycetes_odb10
# BUSCO_phylogenomics
BUSCO_phylogenomics.py -i BUSCO_results -o Tree -t 8 --supermatrix_only -psc 50

# FastTree v2.2.0
FastTree SUPERMATRIX.phylip > tree.nwk

# ggtree v4.2.0 in R v4.6.1
tree <- read.tree("tree.nwk")
ggtree(tree,, layout="rectangular", linewidth = 0.5) + geom_treescale(x=0, y=0, fontsize=2, linesize=0.5) + geom_tiplab(align = TRUE, offset = 0.02, fontface = "italic", family = "sans", size = 3.5) + geom_rootpoint(size = 2.5, color = 'black') + xlim_tree(2.5)
```

## List of accession numbers of assemblies used in the tree

* GCA_030582535.1 *Insectozyma bohioensis*
* GCA_030557115.1 *Insectozyma chauliodis*
* GCA_030565325.1 *Insectozyma coleopterorum*
* GCA_987538045.1 *Insectozyma corydali*
* GCA_030564645.1 *Insectozyma morakotiae*
* GCA_030565145.1 *Insectozyma parachauliodis*
* GCA_030569255.1 *Insectozyma sakaeoensis*
* GCA_947670415.1 *Insectozyma verbasci*
* GCA_030555925.1 *Insectozyma xiaguanensis*
* GCF_000182765.1 *Lodderomyces parapsilosis*