"""Preprocess stage: mcool -> binned compartment eigenvector track.

Ported from notebooks/call_compartments.ipynb: load the cooler at the
configured resolution, compute a GC track from the FASTA to phase
eigenvectors, and run cis eigendecomposition with cooltools.
"""

from pathlib import Path

import click
import cooler
import pandas as pd

from ..config import Config


def _autosomes(chromsizes):
    """Keep standard autosomes (chr1..chrN)."""
    return [c for c in chromsizes.index if c.replace("chr", "").isdigit()]


def _make_viewframe(chroms, chromsizes):
    regions = [(c, 0, int(chromsizes[c])) for c in chroms]
    view = pd.DataFrame(regions, columns=["chrom", "start", "end"])
    view["name"] = view["chrom"]
    return view


def run(config_path):
    cfg = Config.from_yaml(config_path)
    prep = cfg.preprocessing

    mcool_path = Path(prep["mcool_path"]).expanduser()
    if not mcool_path.exists():
        raise click.ClickException(f"mcool not found: {mcool_path}")
    resolution = prep.get("resolution", 25000)

    clr = cooler.Cooler(f"{mcool_path}::/resolutions/{resolution}")
    chromsizes = clr.chromsizes

    chroms = prep.get("chromosomes") or _autosomes(chromsizes)
    click.echo(f"Dataset: {cfg.dataset}")
    click.echo(f"mcool: {mcool_path} at {resolution} bp")
    click.echo(f"Chromosomes: {', '.join(chroms)}")

    # GC track for phasing eigenvectors (sign of E1 tracks open/closed)
    fasta_path = prep.get("fasta_path")
    phasing_track = None
    if fasta_path:
        import bioframe

        fasta_path = Path(fasta_path).expanduser()
        if not fasta_path.exists():
            raise click.ClickException(f"FASTA not found: {fasta_path}")
        click.echo(f"Computing GC track from {fasta_path}")
        bins = clr.bins()[:]
        bins = bins[bins.chrom.isin(chroms)]
        fasta_records = bioframe.load_fasta(str(fasta_path))
        phasing_track = bioframe.frac_gc(bins, fasta_records)
        # cooltools takes columns[:4] as the value column; hand it a clean
        # chrom/start/end/GC track (bins tables carry extra weight columns)
        phasing_track = phasing_track[["chrom", "start", "end", "GC"]]
    else:
        click.echo("No fasta_path given: eigenvectors will not be GC-phased")

    # Cis eigendecomposition (cooltools >= 0.5 API)
    from cooltools.api.eigdecomp import eigs_cis

    n_eigs = prep.get("n_eigs", 3)
    click.echo(f"Running cis eigendecomposition (n_eigs={n_eigs})")
    eigvals, eigvecs = eigs_cis(
        clr,
        phasing_track=phasing_track,
        view_df=_make_viewframe(chroms, chromsizes),
        n_eigs=n_eigs,
        clip_percentile=prep.get("clip_percentile", 99),
        ignore_diags=prep.get("ignore_diags", 2),
    )

    track = eigvecs[eigvecs.chrom.isin(chroms)].reset_index(drop=True)

    out_dir = cfg.preprocessed_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    track_path = out_dir / "compartment_track.tsv"
    track.to_csv(track_path, sep="\t", index=False)

    n_bins = len(track)
    n_valid = int(track.E1.notna().sum())
    click.echo(f"Wrote {track_path} ({n_bins} bins, {n_valid} with valid E1)")
    return track
