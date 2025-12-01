# Scripts Directory

This directory is reserved for future command-line utilities and automation tools.

## Purpose

The primary way to generate figures is through the Jupyter notebooks in the `notebooks/` directory.
This scripts directory can be used for:

- Batch processing workflows
- Command-line tools for common tasks
- Automation scripts
- Data preprocessing utilities

## Design Note

The codebase follows a modular design where:
- **Notebooks** (`notebooks/`) - Generate figures and demonstrate analyses
- **Python modules** (`HMMC/`, `*.py` files) - Provide reusable functions for HMM analysis and plotting
- **This directory** - For additional utilities as needed

The plotting functionality is already available in:
- `HMMC/plotting_tools.py` - Core plotting functions for compartment data
- `coolplots.py` - Hi-C heatmap visualization
- `triangular.py` - Triangular heatmap plotting
- `badtools.py` - BED file and genomic interval utilities

Notebooks import and use these modules to generate publication-quality figures.
