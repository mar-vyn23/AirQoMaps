from flask import Flask
from flask import render_template
import psycopg2
import geojson
import os
from dotenv import load_dotenv
import shapely.wkb as wkb
import shapely.geometry as geometry

app = Flask(__name__)

# load the .env file
load_dotenv()

db_config = {
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
}

try:
    connection = psycopg2.connect(**db_config)
except psycopg2.Error as connection_error:
    print('Unable to establish connection to the database', connection_error)

else:
    # Create a cursor object -> session to the database
    cursor = connection.cursor()
    # Retrieve 3 columns from the database
    cursor.execute('SELECT parish,pm2_5,geometry FROM public."Prediction"')
    # Return all rows of the 3 columns above
    data = cursor.fetchall()
    # close connection after fetching data from db
    cursor.close()


# Transform the data into a geojson
def transform_to_geojson():
    features = []
    for row in data:
        # convert the geometry from hex to bytes
        wkb_geometry = bytes.fromhex(row[2])
        # convert the wkb geometry to a shapely object
        geometry_object = wkb.loads(wkb_geometry)
        # now convert the geometry to a geojson
        geometry_geojson = geometry.mapping(geometry_object)
        properties = {
            'parish': row[0],
            'pm2_5': row[1]
        }
        feature = geojson.Feature(geometry=geometry_geojson, properties=properties)
        features.append(feature)
    feature_collection = geojson.FeatureCollection(features)
    json_dump = geojson.dumps(feature_collection)
    return json_dump


@app.route('/')
def postgres_connection():
    results = transform_to_geojson()
    return render_template('map.html', results=results)


app.run(debug=False)
