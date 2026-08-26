"""CLI entry point for HMMC using Click."""

import click

STAGE_ORDER = ["preprocess", "segment", "figures"]


def _run_stage(stage, config):
    """Import and run a single pipeline stage."""
    if stage == "preprocess":
        from .commands import preprocess as cmd
        cmd.run(config)
    elif stage == "segment":
        from .commands import segment as cmd
        cmd.run(config)
    elif stage == "figures":
        from .commands import figures as cmd
        cmd.run(config)
    else:
        raise click.BadParameter(f"Unknown stage: {stage}")


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """HMM segmentation of Hi-C compartments."""
    pass


@cli.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Path to config YAML")
def preprocess(config):
    """Compute compartment eigenvectors (E1..En) from an mcool.

    Loads the cooler at the configured resolution, computes a GC track
    from the FASTA for phasing, and runs cis eigendecomposition.

    \b
    Example:
        hmmc preprocess -c configs/GM12878/general.yaml
    """
    from .commands import preprocess as prep_cmd
    prep_cmd.run(config)


@cli.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Path to config YAML")
def segment(config):
    """Fit HMM segmentations on the preprocessed compartment track.

    Runs HMMC.get_segmentation for the configured state list, records BIC
    per state, and exports the track plus BED files.

    \b
    Example:
        hmmc segment -c configs/GM12878/general.yaml
    """
    from .commands import segment as seg_cmd
    seg_cmd.run(config)


@cli.command()
@click.option("--config", "-c", required=True, type=click.Path(exists=True), help="Path to config YAML")
def figures(config):
    """Generate publication figures (E1 tracks, segmaps, Hi-C overlay maps).

    \b
    Example:
        hmmc figures -c configs/GM12878/general.yaml
    """
    from .commands import figures as fig_cmd
    fig_cmd.run(config)


@cli.command()
@click.argument("stages", nargs=-1, required=True)
@click.option("--config", "-c", required=True, type=click.Path(exists=True),
              help="Path to config YAML")
def run(stages, config):
    """Run pipeline stages sequentially.

    \b
    STAGES:
        preprocess, segment, figures  - Run specific stages in order

    \b
    EXAMPLES:
        hmmc run preprocess segment figures -c configs/GM12878/general.yaml
        hmmc run figures -c configs/GM12878/general.yaml
    """
    stages = [s.lower() for s in stages]

    valid = set(STAGE_ORDER)
    invalid = set(stages) - valid
    if invalid:
        raise click.BadParameter(
            f"Unknown stage(s): {', '.join(invalid)}. Valid: {', '.join(STAGE_ORDER)}"
        )

    ordered = [s for s in STAGE_ORDER if s in stages]
    click.echo(f"Running stages: {' → '.join(ordered)}")

    for stage in ordered:
        click.echo(f"\n{'='*60}")
        click.echo(f"  Stage: {stage}")
        click.echo(f"{'='*60}\n")
        _run_stage(stage, config)

    click.echo(f"\nAll stages complete.")
