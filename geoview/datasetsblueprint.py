from flask import Blueprint, current_app, send_file, abort

datasets = Blueprint('datasets', __name__)

@datasets.route('/<idx>.json')
def dataset(idx):
    paths = current_app.config.get('GEOJSON_PATHS', None)
    if paths is None:
        return abort(500)

    try:
        geojson_path = paths[int(idx)]
    except (ValueError, IndexError):
        return abort(404)

    return send_file(geojson_path, mimetype='application/vnd.geo+json')
