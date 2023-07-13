import os
import time

import geojson
import psycopg2
import shapely.geometry as geometry
import shapely.wkb as wkb
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

app = Flask(__name__)
load_dotenv()


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
            if i < 10:
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
                print(feature)
                time.sleep(4)
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
