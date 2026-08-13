# Chromosome painting of *Insectozyma corydali* genome

## Overview

The genomes of *I. corydali* and *I. verbasci* were aligned using minimap2 v.2.24-r1122 with sensitive parameters listed below. Only alignments with at least 200 matches were kept. Alignents were visualized using a custom script provided below based on seaborn and matplotlib libraries.

## Files

* `canCor3.fa` and `canVerA1.fa`: input genomes of *Insectozyma corydali* and *I. verbasci*
* `aln.sizes`: sizes of *Insectozyma corydali* chromosomes
* `aln.paf`: minimap2 alignments of *I. corydali* and *I. verbasci* genomes
* `aln.paf.view2`: reformatted and filtered alignments
* `chrompaint.py`: script for chromosome painting
* `chrompaint.pdf`: the result of the script

## Commands used

```bash
# alignment with more sensitive settings
minimap2 -x asm20 -f 0.5 -p 0 -w 5 -k 17 -B 3 -c canVerA1.fa canCor3.fa > aln.paf
# reformatting
perl -lane '$id=sprintf("%.1f", $F[9]*100/$F[10]); print join("\t", @F[9,4,0..3,5..8],$id)' aln.paf > aln.paf.view

# filtering only alignments with at least 200 matching nucleotides
# and skipping mtDNA
perl -lane 'print if $F[0]>=200' aln.paf.view | grep -v mtDNA > aln.paf.view2

# visualization
python3 chrompaint.py
```