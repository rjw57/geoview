from flask import Blueprint, current_app, render_template, url_for

ui = Blueprint('ui', __name__, static_url_path='/static')

@ui.route('/')
def index():
    datasets = {}
    epsg = current_app.config.get('EPSG', 4326)
    for idx in range(len(current_app.config['GEOJSON_PATHS'])):
        name = 'dataset {0}'.format(idx+1)
        datasets[name] = url_for('datasets.dataset', idx=idx)
    return render_template('index.html', datasets=datasets, epsg=epsg)
