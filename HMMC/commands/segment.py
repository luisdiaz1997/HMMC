"""Segment stage: compartment track -> HMM segmentations.

Runs HMMC.get_segmentation over the configured state list, records the
BIC per state, and exports the segmented track plus BED files.
"""

import click

from ..config import Config
from ..HMMC import get_segmentation
from ..plotting_tools import track_to_bed


def run(config_path):
    cfg = Config.from_yaml(config_path)
    seg = cfg.segmentation

    if not cfg.track_path.exists():
        raise click.ClickException(
            f"Preprocessed track not found: {cfg.track_path}. Run `hmmc preprocess` first."
        )

    import pandas as pd

    track = pd.read_csv(cfg.track_path, sep="\t")
    state_list = seg.get("state_list", ["binary", "HMM2", "HMM3", "HMM3P", "HMM4", "HMM5"])
    click.echo(f"Segmenting {track.chrom.nunique()} chromosomes with states: {', '.join(state_list)}")

    seg_track, bic_dict = get_segmentation(
        track,
        state_list=state_list,
        constrain_transmat=seg.get("constrain_transmat", False),
        return_BIC_dict=True,
        verbose=True,
    )

    out_dir = cfg.segmentation_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    seg_path = out_dir / "seg_track.tsv"
    seg_track.to_csv(seg_path, sep="\t", index=False)
    click.echo(f"Wrote {seg_path}")

    # BIC table + curve
    if bic_dict:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        states = sorted(bic_dict, key=lambda s: int("".join(filter(str.isdigit, s))))
        bic_path = out_dir / "bic.csv"
        pd.DataFrame({"state": states, "BIC": [bic_dict[s] for s in states]}).to_csv(
            bic_path, index=False
        )
        click.echo(f"Wrote {bic_path}")

        fig, ax = plt.subplots(figsize=(4, 3))
        n_states = [int("".join(filter(str.isdigit, s))) for s in states]
        ax.plot(n_states, [bic_dict[s] for s in states], marker="o")
        ax.set_xlabel("number of HMM states")
        ax.set_ylabel("BIC")
        fig.savefig(out_dir / "bic_curve.png", dpi=150, bbox_inches="tight")
        plt.close(fig)

    # BED exports
    for state in seg.get("bed_states", ["HMM3P"]):
        if state not in seg_track.columns:
            click.echo(f"Skipping BED export for {state} (not in state_list)")
            continue
        bed_df = track_to_bed(seg_track, state)
        bed_path = out_dir / f"{cfg.dataset}_{state}.bed"
        bed_df.to_csv(bed_path, sep="\t", index=False, header=False)
        click.echo(f"Wrote {bed_path}")

    return seg_track
