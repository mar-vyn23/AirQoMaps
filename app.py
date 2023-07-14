import os
import geojson
import psycopg2
import shapely.geometry as geometry
import shapely.wkb as wkb
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_caching import Cache

app = Flask(__name__)
load_dotenv()

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app=app)


@cache.cached(timeout=3600, key_prefix='geo_data')
def connect_to_db():
    db_config = {
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
    }

    try:
        connection = psycopg2.connect(**db_config)
    except psycopg2.Error as e:
        print(f'Error establishing connection to db : {e}')
    else:
        cursor = connection.cursor()
        cursor.execute('SELECT parish, pm2_5, geometry FROM public."Prediction"')
        i = 0
        for row in cursor:
            if i < 16863:
                wkb_geometry = bytes.fromhex(row[2])
                geometry_object = wkb.loads(wkb_geometry)
                geometry_geojson = geometry.mapping(geometry_object)
                properties = {
                    'parish': row[0],
                    'pm2_5': round(row[1], 2)
                }
                i += 1
                feature = geojson.Feature(geometry=geometry_geojson, properties=properties)
                yield feature
        cursor.close()
        connection.close()


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/geo')
def get_geo_data():
    feature_generator = connect_to_db()
    feature_list = list(feature_generator)
    feature_collection = geojson.FeatureCollection(feature_list)
    return jsonify(feature_collection)


if __name__ == "__main__":
    app.run(debug=True)
