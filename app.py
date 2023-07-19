# Import necessary libraries
import os
import time
import geojson
import psycopg2
import shapely.wkb as wkb
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_caching import Cache

# Create a Flask app
app = Flask(__name__)
load_dotenv()

# Configure database connection parameters using environment variables
db_config = {
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'database': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
}

# Configure Flask app to use Redis for caching
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
cache = Cache(app=app)

# Function to convert database records to GeoJSON format
def to_geojson(parish, pm2_5, wkb_string, id):
    geo_coordinates = wkb.loads(wkb_string)
    feature = geojson.Feature(id=str(id), geometry=geo_coordinates, properties={"parish": parish, "pm2_5": pm2_5})
    return feature

# Global variable to track the offset for pagination
offset = 0

# Route to access geo data from the database
@app.route('/geo')
@cache.cached(timeout=1800, key_prefix='geo_cache')  # Cache the response for 1800 seconds (1/2 an hour)
def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)  # Connect to the PostgreSQL database
    except psycopg2.Error as e:
        print(f'Error establishing connection to db : {e}')
    else:
        global offset
        chunk_size = 50
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM public."Prediction"')
        total_rows = cursor.fetchone()[0]

        # Check if there are more rows to fetch based on the current offset
        if offset < total_rows:
            # Fetch a chunk of records from the database using LIMIT and OFFSET clauses
            cursor.execute(f'SELECT parish, pm2_5, geometry FROM public."Prediction" LIMIT {chunk_size} OFFSET {offset}')
            rows = cursor.fetchall()

            # Convert each row to GeoJSON feature using the 'to_geojson' function and build a FeatureCollection
            features = [to_geojson(row[0], round(row[1]), row[2], id=i + offset) for i, row in enumerate(rows)]
            feature_collection = geojson.FeatureCollection(features)

            # Increment the offset for the next chunk
            offset = offset + chunk_size

            # Wait for 2 seconds before fetching another batch
            time.sleep(1)
        else:
            # If no more rows to fetch, return an empty FeatureCollection
            feature_collection = geojson.FeatureCollection([])

        cursor.close()
        connection.close()
        return jsonify(feature_collection)  # Return the GeoJSON data as a JSON response

# Route to display the map
@app.route('/')
def home():
    return render_template('map.html')

# Run the Flask app on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
