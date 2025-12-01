# Figure Generation Scripts

This directory contains standalone Python scripts to generate each figure in the paper.

## Structure

- `figure1.py` - Generates Figure 1 (compartment visualization)
- `figure2.py` - Generates Figure 2 (genomic features and ChromHMM analysis)
- `figure3.py` - Generates Figure 3 (signals at transitions)
- `figure4.py` - Generates Figure 4 (gene expression multi-cell comparison)
- `sfigure1.py` - Generates Supplemental Figure 1 (counts)
- `sfigure2.py` - Generates Supplemental Figure 2 (ChIP-seq)
- `utils.py` - Shared utility functions for figure generation

## Usage

Each script can be run independently:

```bash
python scripts/figure1.py --output figures/figure1.pdf
```

Or imported in notebooks:

```python
from scripts import figure1
figure1.generate_figure(output_path='figures/figure1.pdf')
```

## Requirements

All scripts require:
- Hi-C data files (.mcool format)
- Annotation files (in `annotations/` directory)
- Required Python packages (see `requirements.txt`)

See the main README for data file locations and setup instructions.
