"""Console script for zalando_classification."""
import h5py
import sys
import click

from densratio import densratio
from etudes.utils import load_hdf5

# Sensible defaults
ALPHA = 0.0
SEED = None


@click.command()
@click.argument("filename", type=click.Path(dir_okay=False))
@click.argument("dataset_filename", type=click.Path(exists=True, dir_okay=False))
@click.option("--alpha", default=ALPHA, type=float)
@click.option("-s", "--seed", default=SEED, type=int, help="Random seed")
def main(filename, dataset_filename, alpha, seed):

    (X_train, y_train), (X_test, y_test) = load_hdf5(dataset_filename)

    densratio_obj = densratio(X_test, X_train, alpha=alpha)
    importance_weights = densratio_obj.compute_density_ratio(X_train)

    with h5py.File(filename, 'w') as f:
        f.create_dataset("importance_weights", data=importance_weights)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
