"""
Quickly view geospatial datasets in a web browser.

Usage:
    geoview (-h | --help)
    geoview [--quiet] [--epsg NUMBER] <dataset>...

Options:
    -h, --help          Show a brief usage summary.
    -q, --quiet         Only log errors and warnings.

    --epsg NUMBER       Set EPSG code for map projection.

One or more datasets are specified on the command line. A webserver is created
to serve the data in GeoJSON format and the system web browser is popped up
with a slippy map showing the data.

"""
from contextlib import contextmanager
import logging
import os
from shutil import rmtree
import sys
from tempfile import mkdtemp

from docopt import docopt
from flask import Flask
from osgeo import ogr

from .uiblueprint import ui
from .datasetsblueprint import datasets

LOG = logging.getLogger()

@contextmanager
def create_scratch_dir():
    dirname = mkdtemp(prefix='geoview.scratch.')
    LOG.info('Using "%s" as scratch directory', dirname)
    yield dirname
    LOG.info('Deleting %s', dirname)
    rmtree(dirname, True)

def main():
    """Main entry point."""
    # Parse command-line options
    opts = docopt(__doc__)

    # Configure logging
    logging.basicConfig(
        level=logging.WARN if opts['--quiet'] else logging.INFO,
        stream=sys.stderr, format='%(name)s:%(levelname)s:%(message)s'
    )

    # Create scratch dir holding datasets
    with create_scratch_dir() as scratch_dir:
        # Create webapp and run ti
        app = create_webapp(scratch_dir, opts)
        app.run()

def create_webapp(scratch_dir, opts):
    # Load each dataset in turn
    geojson_base = os.path.join(scratch_dir, 'geojson')
    os.makedirs(geojson_base)
    geojson_paths = []
    for ds_idx, ds in enumerate(opts['<dataset>']):
        LOG.info('Loading: %s', ds)
        geojson_path = os.path.join(geojson_base, 'dataset-{0}.geojson'.format(ds_idx))
        convert_to_geojson(ds, geojson_path)
        geojson_paths.append(geojson_path)
    LOG.info('Loaded %s dataset(s)', len(geojson_paths))

    app = Flask('geoview')
    app.config['SCRATCH_DIR'] = scratch_dir
    app.config['GEOJSON_BASE'] = geojson_base
    app.config['GEOJSON_PATHS'] = geojson_paths
    if opts['--epsg'] is not None:
        app.config['EPSG'] = opts['--epsg']

    app.register_blueprint(datasets, url_prefix='/datasets')
    app.register_blueprint(ui, url_prefix='/')

    return app

def convert_to_geojson(ds_path, output_path):
    # Use OGR to load a dataset, converting it to a GeoJSON representation.
    ds = ogr.Open(ds_path)
    if ds is None:
        LOG.error('Failed to open input dataset %s', ds_path)
        raise IOError()

    # Copy this dataset to an in-memory GeoJSON dataset.
    geojson_driver = ogr.GetDriverByName('GeoJSON')
    if geojson_driver is None:
        LOG.error('No GeoJSON OGR driver installed.')
        raise RuntimeError()

    geojson_driver.CopyDataSource(ds, output_path)

# Support running this module directly.
if __name__ == '__main__':
    main()
