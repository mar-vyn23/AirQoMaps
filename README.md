# AirQoMaps

AirQoMaps is a web application that visualizes air quality data using interactive maps. 
It provides real-time information about the PM2.5 air quality index (AQI) for different parishes.

Features

* Dynamic map rendering using D3.js and D3-GeoProjection.
* Interactive tooltips that display additional information about each parish.
* Color-coded legend indicating the PM2.5 AQI ranges.
* Zoom functionality for a more detailed view of the map.
* Caching mechanism implemented using Flask-Caching and Redis.
* Data retrieval from a PostgreSQL database.

Installation
Clone the repository:

`git clone https://github.com/your-username/AirQoMaps.git`

Install the required dependencies:

`pip install -r requirements.txt`

Set up the environment variables by creating a .env file and filling in the necessary values:

`DB_HOST=your-database-host`
`DB_PORT=your-database-port`
`DB_NAME=your-database-name`
`DB_USER=your-database-username`
`DB_PASSWORD=your-database-password`

Start the application:

python app.py

`Access the application in your web browser at http://localhost:5000.`

Usage

Once the application is running, you can access the map view by visiting the home page. The map will display colored polygons representing different parishes, with each color indicating a specific range of PM2.5 AQI. Hovering over a parish will show a tooltip with detailed information about that location's air quality.

You can zoom in or out of the map by clicking the respective buttons or using the scroll wheel.
Contributing

Contributions are welcome! If you have any ideas, improvements, or bug fixes, please submit a pull request. 
Make sure to follow the existing coding style and include relevant tests and documentation.
License

This project is licensed under the MIT License.
Acknowledgements

* D3.js - JavaScript library for data visualization.
* Bootstrap - CSS framework for responsive web design.
* Flask - Web framework for Python.
* PostgreSQL - Open-source relational database system.
* Redis - In-memory data structure store used for caching.
