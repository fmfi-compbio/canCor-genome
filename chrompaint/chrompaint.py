import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

columns = ['score', 'strand', 'name1', 'len1', 'start1', 'end1',
           'name2', 'len2', 'start2', 'end2', 'pid']
columns2 = ['name', 'length']
paf = pd.read_csv("aln.paf.view2", sep="\t",  names=columns)
sizes = pd.read_csv("aln.sizes", sep="\t",  names=columns2)

names2 = sorted(list(paf['name2'].unique()))

pal = sns.color_palette("tab10")
colors = dict()
for (i,name) in enumerate(names2):
  colors[name] = pal[i]

def get_num(name, sizes):
  for (idx, row) in sizes.iterrows():
    if name == row.loc["name"]:
      return idx
  print(name, sizes)
  return None

# for chr
def get_y(idx):
  return -idx


figure, axes = plt.subplots(1, 1,
                            figsize=(8, 3.2))
axes.axis('off')
axes.set_xlim(0,2.7e6)
axes.set_ylim(-7,1)

for (idx, row) in paf.iterrows():
  idx = get_num(row.loc["name1"], sizes)
  width = row.loc["end1"]-row.loc["start1"]
  color = colors[row.loc["name2"]]
  axes.add_patch(plt.Rectangle((row["start1"], get_y(idx)), width, 0.8, fc=color, ec="None"))

# chromosomes
for (idx, chr) in sizes.iterrows():
  size = chr.loc['length']
  y = get_y(idx)
  name = chr.loc['name'] + f" {size/1e6:.1f}Mbp"
  axes.add_patch(plt.Rectangle((0, y), size, 0.8, ec="black", fill=False))
  axes.text(-1e5, y+0.4, name, ha='right', va='center')

# for legend
def get_new_y(idx):
  return -2.35+get_y(idx)*0.75

axes.text(2.1e6, -1.7, "C. verbasci", ha='left', va='bottom', style='italic')

# legend
for (idx, chr) in enumerate(names2):
  color = colors[chr]
  y = get_new_y(idx)
  axes.add_patch(plt.Rectangle((2.1e6, y), 0.15e6, 0.55,
                                fc=color, ec="None"))
  axes.text(2.3e6, y+0.2, chr, ha='left', va='center')

  
figure.savefig('chrompaint.pdf', bbox_inches='tight')
