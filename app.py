from flask import Flask, jsonify
from flask import render_template
import psycopg2
import os
from dotenv import load_dotenv
import shapely.wkb as wkb
import shapely.geometry as geometry
import geojson
import time

app = Flask(__name__)
load_dotenv()
app.template_folder = 'templates'


@app.route('/')
def home():
    return render_template('map.html')


@app.route('/geo')
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
        limit = 100
        offset = 0
        data = []
        while True:
            # get first 100 records
            cursor = connection.cursor()
            cursor.execute('SELECT parish,pm2_5,geometry FROM public."Prediction" OFFSET %s LIMIT %s', (offset, limit))
            rows = cursor.fetchall()
            for row in rows:
                wkb_geometry = bytes.fromhex(row[2])
                geometry_object = wkb.loads(wkb_geometry)
                geometry_geojson = geometry.mapping(geometry_object)
                properties = {
                    'parish': row[0],
                    'pm2_5': row[1]
                }
                feature = geojson.Feature(geometry=geometry_geojson, properties=properties)
                geo_json = geojson.dumps(feature)
                # print(geo_json)
                # print("\n\n")
                data.append(geo_json)
                time.sleep(10)
            offset += limit
            if len(rows) < limit:
                break
        return data


if __name__ == "__main__":
    app.run(debug=True)
