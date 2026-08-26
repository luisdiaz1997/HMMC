"""Figures stage: publication figures from a segmentation.

Produces Figure1-style outputs for each configured region: an E1 line
plot, a colored segmentation track (segmap), and a Hi-C contact map with
segmentation overlay (via HMMC.plotmap).
"""

from pathlib import Path

import click

import matplotlib

matplotlib.use("Agg")

import bioframe as bf
import cooler
import matplotlib.pyplot as plt
import numpy as np

from ..config import Config
from ..plotting_tools import cmap, names, pallete, plotmap, track_to_bed, track_to_mat


def _slug(region):
    return region.replace(",", "")


def run(config_path):
    cfg = Config.from_yaml(config_path)
    fig_cfg = cfg.figures

    if not cfg.seg_track_path.exists():
        raise click.ClickException(
            f"Segmented track not found: {cfg.seg_track_path}. Run `hmmc segment` first."
        )

    import pandas as pd

    seg_track = pd.read_csv(cfg.seg_track_path, sep="\t")
    annotation_type = fig_cfg.get("annotation_type", "HMM3P")
    if annotation_type not in seg_track.columns:
        raise click.ClickException(
            f"annotation_type '{annotation_type}' not in segmentation columns "
            f"{list(seg_track.columns)}"
        )

    mcool_path = Path(cfg.preprocessing["mcool_path"]).expanduser()
    resolution = cfg.preprocessing.get("resolution", 25000)
    clr = cooler.Cooler(f"{mcool_path}::/resolutions/{resolution}")

    figure_width = fig_cfg.get("figure_width", 5)
    # inkscape-friendly svg text
    matplotlib.rcParams["svg.fonttype"] = "none"

    out_dir = cfg.figures_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    for region in fig_cfg.get("regions", []):
        slug = _slug(region)
        click.echo(f"Figures for {region}")

        # E1 line plot
        plt.figure(figsize=(figure_width, figure_width / 10))
        e1 = bf.select(seg_track, region)["E1"].to_numpy(copy=True)
        plt.plot(e1, color=[0, 0, 0], lw=0.5)
        plt.ylim([-2, 2])
        plt.grid(True)
        plt.yticks([-2, 0, 2])
        plt.xlim([0, len(e1)])
        ax = plt.gca()
        _, start, _ = bf.parse_region(region)
        xticklabels = ((ax.xaxis.get_ticklocs() * resolution / 1e3) + start / 1e3).astype(int)
        ax.xaxis.set_ticklabels(xticklabels)
        plt.savefig(out_dir / f"e1_{slug}.svg", bbox_inches="tight")
        plt.close()

        # Colored segmentation track
        plt.figure(figsize=(figure_width, figure_width / 10))
        mat_c = track_to_mat(seg_track, region, annotation_type, pallete, horizontal=True)
        plt.imshow(mat_c, cmap=matplotlib.colors.ListedColormap(cmap), vmin=0, vmax=5, aspect="auto")
        plt.axis("off")
        plt.savefig(out_dir / f"segmap_{slug}_{annotation_type}.svg", bbox_inches="tight")
        plt.close()

        # Hi-C map with segmentation overlay
        bed_track = track_to_bed(seg_track, annotation_type)
        fig = plotmap(clr, bed_track, region, region, figure_width=figure_width)
        fig.savefig(out_dir / f"hicseg_{slug}_{annotation_type}.svg", bbox_inches="tight")
        plt.close(fig)

    click.echo(f"Wrote figures to {out_dir}")
