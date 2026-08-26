# HMMC

A Hidden Markov Model approach for segmenting 3D genome compartments from Hi-C datasets stored in the [cooler](https://github.com/open2c/cooler) format.

HMMC operates on eigenvectors computed [using cooltools](https://github.com/open2c/cooltools) in a pandas dataframe format as an input. HMMC has so far been applied to human and mouse coolers binned at 50kb-1Mb resolution.

## Installation

Install locally with pip (Python >= 3.10):

~~~
pip install -e ./
~~~

The current development environment reuses the `chromgp` conda environment
(Python 3.14; user-site packages in `~/.local/lib/python3.14`):

~~~
conda activate chromgp
pip install -e ./
~~~

The codebase is modernized for that stack: numpy 2.4 / pandas 3
(Copy-on-Write, string dtypes), bioframe 0.8, cooler 0.10, cooltools 0.7
(`cooltools.api.*` namespaces), hmmlearn 0.3, matplotlib 3.10. The
`pybedtools`/bedtools-CLI intersections were replaced with `bioframe.overlap`.

## CLI

The `hmmc` command runs the pipeline in stages, driven by a single YAML
config (see `configs/`):

~~~
hmmc run preprocess segment figures -c configs/GM12878/general.yaml
~~~

- `preprocess` — mcool → GC-phased cis eigenvectors
  (`outputs/<dataset>/preprocessed/compartment_track.tsv`)
- `segment` — HMM segmentations for the configured state list, BIC table
  and curve, BED export (`outputs/<dataset>/segmentation/`)
- `figures` — E1 tracks, segmaps and Hi-C overlay maps
  (`outputs/<dataset>/figures/`)

## Data

Raw mcools are not stored in the repo. Create a gitignored symlink to the
lab storage and reference coolers through it:

~~~
ln -s /gladstone/engelhardt/lab/lchumpitaz/hi-c/mcools mcools
~~~

Available: GM12878 (`4DNFIXP4QG5B`), K562 (`4DNFI18UHVRO`),
HUVEC (`4DNFIRMZ7QTE`), IMR90 (`4DNFIJTOIGOI`).
hg38 FASTA: `/gladstone/engelhardt/lab/lchumpitaz/hi-c/hg38.fa`.
Roadmap ChromHMM beds (E017/E116/etc. hg38lift mnemonics):
`/gladstone/engelhardt/lab/lchumpitaz/datasets/chromhmm/`.
`data/gencode.v37.annotation.gff3.gz` and
`data/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_median_tpm.gct.gz`
are gitignored public downloads used by the gene-expression notebooks.

## Notebooks

All paper-figure notebooks in `notebooks/` run end-to-end in the `chromgp`
env (executed 2026-08), except:

- `Figure3_signals_at_transitions.ipynb` — downloads ENCODE bigWigs on
  first run (modernized: pyBigWig + direct ENCODE URLs).
- `Compare_segmentations.ipynb` — needs hg19 distiller mcools under
  `../mcools/`.
- `Supplemental Figure 2- Chipseq.ipynb` — needs a local ENCODE
  ChIP-seq bed.gz directory.

In `extra_notebooks/`, everything runs except: `Compare_LADs.ipynb`
(needs the H9 cooler `4DNFIT5YVTLO` in `mcools/`), `Eigentranscontacts.ipynb`
and `Plot_Colortracks.ipynb` (missing csv / external drive), and
`Fig 2 tracks.ipynb` (needs pygenometracks/pygbrowse/bbi).

Notebook writes are redirected to `outputs/notebooks/` and `figs/` so the
committed `annotations/` stay untouched.
