"""Configuration system for HMMC experiments.

Mirrors the ChromGP config pattern: a single YAML drives every pipeline
stage (preprocess, segment, figures), and stages pass data through files
under ``output_dir/<dataset>/``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class Config:
    """Experiment configuration.

    Attributes:
        name: Experiment name
        seed: Random seed
        dataset: Dataset name used as the output subdirectory
            (e.g. 'GM12878_hg38_25kb', matching the annotations/ convention)
        preprocessing: Cooler/eigenvector parameters (mcool path, resolution,
            fasta for GC phasing, chromosomes, n_eigs, ...)
        segmentation: HMM segmentation parameters (state_list, ...)
        figures: Figure parameters (annotation_type, regions, ...)
        output_dir: Output directory path
    """

    name: str
    seed: int = 67
    dataset: str = "GM12878_hg38_25kb"

    # Preprocessing config (compartment eigenvectors)
    preprocessing: Dict[str, Any] = field(default_factory=lambda: {
        "mcool_path": None,
        "resolution": 25000,
        "fasta_path": None,       # GC content track for phasing eigenvectors
        "chromosomes": None,      # list of chroms; None = all autosomes
        "n_eigs": 3,
        "clip_percentile": 99,
        "ignore_diags": 2,
    })

    # Segmentation config (HMM on E1)
    segmentation: Dict[str, Any] = field(default_factory=lambda: {
        "state_list": ["binary", "HMM2", "HMM3", "HMM3P", "HMM4", "HMM5"],
        "constrain_transmat": False,
        "bed_states": ["HMM3P"],  # states exported as BED tracks
    })

    # Figures config
    figures: Dict[str, Any] = field(default_factory=lambda: {
        "annotation_type": "HMM3P",
        "regions": ["chr19:31,000,000-35,000,000"],
        "figure_width": 5,
    })

    # Output config
    output_dir: str = "outputs"

    @property
    def dataset_dir(self) -> Path:
        """Directory holding all artifacts for this dataset."""
        return Path(self.output_dir) / self.dataset

    @property
    def preprocessed_dir(self) -> Path:
        return self.dataset_dir / "preprocessed"

    @property
    def segmentation_dir(self) -> Path:
        return self.dataset_dir / "segmentation"

    @property
    def figures_dir(self) -> Path:
        return self.dataset_dir / "figures"

    @property
    def track_path(self) -> Path:
        return self.preprocessed_dir / "compartment_track.tsv"

    @property
    def seg_track_path(self) -> Path:
        return self.segmentation_dir / "seg_track.tsv"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        return cls(
            name=data["name"],
            seed=data.get("seed", 67),
            dataset=data.get("dataset", "GM12878_hg38_25kb"),
            preprocessing=data.get("preprocessing", {}),
            segmentation=data.get("segmentation", {}),
            figures=data.get("figures", {}),
            output_dir=data.get("output_dir", "outputs"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "name": self.name,
            "seed": self.seed,
            "dataset": self.dataset,
            "preprocessing": self.preprocessing,
            "segmentation": self.segmentation,
            "figures": self.figures,
            "output_dir": self.output_dir,
        }

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Config":
        """Load configuration from a YAML file."""
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def save_yaml(self, path: str | Path) -> None:
        """Save configuration to a YAML file with blank lines between sections."""
        d = self.to_dict()
        with open(path, "w") as f:
            f.write(f"name: {d['name']}\n")
            f.write(f"seed: {d['seed']}\n")
            f.write(f"dataset: {d['dataset']}\n")
            f.write(f"output_dir: {d['output_dir']}\n")

            for key in ["preprocessing", "segmentation", "figures"]:
                f.write(f"\n{key}:\n")
                content = yaml.dump(d[key], default_flow_style=False, sort_keys=False)
                for line in content.strip().split('\n'):
                    f.write(f"  {line}\n")
