# HMMC: Hidden Markov Models for Hi-C Compartment Analysis

Analysis of Hi-C chromatin compartments using Hidden Markov Models with integration of ChIP-seq features.

## Project Overview

This repository contains code to reproduce all figures from the paper analyzing chromatin compartments using Hidden Markov Models (HMMs) applied to Hi-C data, with integration of ChIP-seq and genomic annotation data.

## Repository Structure

```
HMMC/
├── HMMC/                    # Main package directory
│   ├── HMMC.py             # Core HMM functions
│   ├── genome_tools.py     # Genome manipulation utilities
│   └── plotting_tools.py   # Plotting utilities
├── notebooks/               # Main figure generation notebooks
│   ├── Figure1 - plotmap.ipynb
│   ├── Figure2- Genomic features of compartments.ipynb
│   ├── Figure 2 - ChromHMM analysis.ipynb
│   ├── Figure3_signals_at_transitions.ipynb
│   ├── Figure 4 - Gene expression multicell.ipynb
│   ├── Figure4.ipynb
│   ├── SFig 1-Counts.ipynb
│   ├── Supplemental Figure 2- Chipseq.ipynb
│   └── call_compartments.ipynb
├── extra_notebooks/         # Additional analysis notebooks
├── scripts/                 # Figure generation scripts (in development)
├── figures/                 # Output directory for generated figures
├── plots/                   # Pre-generated plots
├── annotations/             # Genomic annotations (BED, TSV files)
├── data/                    # Data files directory (user-provided)
├── badtools.py             # BED file and bioframe utilities
├── coolplots.py            # Hi-C plotting utilities
├── fileprocessing.py       # File I/O utilities
├── multianalysis.py        # Multi-cell analysis utilities
├── numutils.py             # Numerical utilities
├── triangular.py           # Triangular heatmap plotting
├── requirements.txt        # Python dependencies
└── setup.py                # Package installation script
```

## Installation

### Prerequisites

- Python 3.7 or higher
- Conda or virtualenv (recommended)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd HMMC
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   conda create -n hmmc python=3.8
   conda activate hmmc
   ```

   Or using virtualenv:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install the HMMC package:**
   ```bash
   pip install -e .
   ```

## Data Requirements

### Required Data Files

The notebooks require the following types of data:

1. **Hi-C Data (.mcool files):**
   - Multi-resolution cooler files from 4DN or similar sources
   - Place in a directory and update paths in notebooks
   - Example sources:
     - 4DN Data Portal: https://data.4dnucleome.org/
     - Rao et al. 2014 datasets
     - Zhang et al. 2019 datasets

2. **Genomic Annotations:**
   - Already included in `annotations/` directory
   - Contains compartment calls, ChromHMM states, and other genomic features
   - Multiple cell lines: GM12878, IMR90, H9-hESC, etc.
   - Multiple resolutions: 10kb, 25kb, 50kb, 100kb, 250kb

3. **Reference Genome:**
   - FASTA files for GC content calculation
   - hg19 and hg38 assemblies

4. **ChIP-seq Data (for Figure 2):**
   - Processed ChIP-seq data from ENCODE
   - Peak files in BED format
   - Can be downloaded using notebooks in `extra_notebooks/`

### Data Configuration

Update data file paths in each notebook:
- Look for variables like `cooler_file`, `fasta_file`, `bed_dir`
- Update paths to match your local data storage

## Usage

### Running Notebooks

1. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

2. **Navigate to the `notebooks/` directory**

3. **Open and run the desired notebook:**
   - `Figure1 - plotmap.ipynb` - Main compartment visualization
   - `Figure2- Genomic features of compartments.ipynb` - Genomic features analysis
   - `Figure3_signals_at_transitions.ipynb` - Transition boundary analysis
   - `Figure4.ipynb` - Multi-cell gene expression comparison
   - `SFig 1-Counts.ipynb` - Supplemental counts analysis
   - `Supplemental Figure 2- Chipseq.ipynb` - ChIP-seq enrichment analysis

4. **Figures will be saved to the `figures/` directory**

### Figure Generation Workflow

Each main figure notebook follows this general workflow:

1. **Load Hi-C data** using cooler
2. **Load annotations** from `annotations/` directory
3. **Process data** using HMMC package functions
4. **Generate visualizations** using matplotlib and custom plotting functions
5. **Save figures** to `figures/` directory

### Example: Generate Figure 1

```python
# In Jupyter notebook or Python script
import sys
sys.path.append('..')

from HMMC import HMMC
import cooler
import pandas as pd
import matplotlib.pyplot as plt

# Load data
cooler_file = '/path/to/your/data.mcool'
c = cooler.Cooler(f'{cooler_file}::resolutions/50000')

# Load compartment annotations
hmm_track = pd.read_csv('../annotations/GM12878_hg38_25kb.tsv', sep='\t')

# Generate figure (see notebook for full code)
# ...

plt.savefig('../figures/figure1.pdf')
```

## Main Modules

### HMMC Package (`HMMC/`)

- **HMMC.py**: Core Hidden Markov Model functions for compartment calling
  - `call_compartments()` - Main HMM compartment calling function
  - `_make_transmat()` - Transition matrix generation
  - Supports 3, 4, 5, and 6-state models

- **genome_tools.py**: Genome data manipulation utilities

- **plotting_tools.py**: Specialized plotting functions for compartment data

### Utility Modules

- **badtools.py**: BED file operations and bioframe integration
  - `bedtools_intersect()` - Intersection of genomic intervals
  - `chip_intersect()` - ChIP-seq peak processing
  - `fold_score()` - Enrichment calculations

- **coolplots.py**: Hi-C heatmap visualization utilities

- **triangular.py**: Triangular Hi-C heatmap plotting

- **multianalysis.py**: Multi-cell comparative analysis

- **numutils.py**: Numerical utilities for data processing

## Cell Lines and Assemblies

The analysis includes data from multiple cell lines:

- **GM12878** (lymphoblastoid cell line) - hg19, hg38
- **IMR90** (lung fibroblast) - hg19, hg38
- **H9-hESC** (embryonic stem cells) - hg38
- **H1-hESC** (embryonic stem cells) - hg38
- **K562** (myelogenous leukemia) - hg19, hg38
- **HUVEC** (endothelial cells)
- **NHEK** (keratinocytes)

## Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure HMMC package is installed: `pip install -e .`
   - Check that all dependencies are installed: `pip install -r requirements.txt`

2. **Data file not found:**
   - Update file paths in notebooks to match your local data storage
   - Ensure data files are downloaded and accessible

3. **Memory errors:**
   - Hi-C data analysis can be memory-intensive
   - Consider using lower resolutions (e.g., 100kb instead of 10kb)
   - Close other applications to free up memory

4. **Cooler/Bioframe version issues:**
   - Some functions have changed between versions
   - Check `badtools.py` for correct import statements for your version

## Development Roadmap

### Current Status
- ✅ All notebooks integrated and organized
- ✅ Dependency management (requirements.txt)
- ✅ Package structure (HMMC/)
- ✅ Annotation files included

### Future Work
- 🚧 Refactor notebook code into standalone scripts (`scripts/` directory)
- 🚧 Create command-line interface for figure generation
- 🚧 Add unit tests
- 🚧 Optimize memory usage for large datasets
- 🚧 Add comprehensive documentation
- 🚧 Create example data subset for quick testing

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Citation

If you use this code in your research, please cite:

```
[Citation information to be added]
```

## License

[License information to be added]

## Contact

For questions or issues, please:
- Open an issue on GitHub
- Contact: [contact information]

## Acknowledgments

This work uses data from:
- 4DN Data Portal
- ENCODE Project
- Rao et al. 2014 Hi-C datasets
