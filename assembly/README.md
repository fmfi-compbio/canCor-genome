# Commands for read processing, assembly and BUSCO analysis

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

# genome assembly
# hifiasm v0.25.0-r726
hifiasm --ont -f0 -o sample -t 16 sample.filtered.downsampled.fastq.gz
awk '/^S/{print ">"$2"\n"$3}' sample_hifiasm.bp.p_ctg.gfa > sample_hifiasm.fasta

# Illumina read trimming
# Trimmomatic v0.39
java -jar trimmomatic-0.39.jar PE reads_1.fastq.gz reads_2.fastq.gz reads_1.paired.fastq.gz reads_1.unpaired.fastq.gz reads_2.paired.fastq.gz reads_2.unpaired.fastq.gz ILLUMINACLIP:TruSeq3-PE.fa:2:30:10:2:keepBothReads LEADING:3 TRAILING:3 MINLEN:36

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