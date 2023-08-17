# AirQoMaps - Real-Time Air Quality Visualization

AirQoMaps is a powerful web application that offers real-time visualizations of air quality data through interactive maps. It provides valuable insights into the PM2.5 air quality index (AQI) for different parishes, helping users stay informed about air quality conditions in their area.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

Air pollution is a critical environmental issue affecting millions of people worldwide. AirQoMaps aims to address this concern by presenting air quality data in a user-friendly and interactive manner. The application leverages Python's Flask framework, D3.js, D3-GeoProjection, and PostgreSQL to create dynamic maps that display air quality information for various parishes.

## Features

- **Dynamic Map Rendering:** AirQoMaps uses D3.js and D3-GeoProjection to generate interactive maps with colored polygons representing different parishes. The map initially loads the parish where the user is located currently. When the user moves the map , other parishes are progressively loaded. The map leverages OpenStreetMaps API to plot the parishes and PM2.5 values on it.
- **Interactive Tooltips:** The application offers tooltips that provide additional information about each parish, including its name and the corresponding PM2.5 AQI level. You just have to hover over any loaded area and the name of the parish and the corresponding PM2.5 value will be shown.
- **Color-Coded Legend:** A color-coded legend accompanies the map, providing a clear visualization of PM2.5 AQI ranges. Each color represents a specific AQI level.
- **Zoom Functionality:** Users can zoom in and out of the map to get a more detailed view of the air quality data.
- **Caching Mechanism:** AirQoMaps implements Flask-Caching with Redis to enhance performance by caching responses.
- **Data Retrieval from PostgreSQL:** The application fetches air quality data from a PostgreSQL database, ensuring real-time updates.


## Installation

1. Clone the repository:

`git clone https://github.com/your-username/AirQoMaps.git`

2. Install the required dependencies:

`pip install -r requirements.txt`


3. Set up the environment variables by creating a `.env` file and providing the necessary values:

`DB_HOST=your-database-host`

`DB_PORT=your-database-port`

`DB_NAME=your-database-name`

`DB_USER=your-database-username`

`DB_PASSWORD=your-database-password`

The dataset used can be downloaded here "https://drive.google.com/file/d/1auwMvMeqeUQ_8Im16k5tVT6NlHw4COXT/view?usp=drive_link" 


4. Start the application:

python app.py

5. Access the application in your web browser at http://localhost:5000.

## Usage

Upon launching AirQoMaps, the home page displays the interactive map. Colored polygons on the map represent different parishes, with each color indicating a specific range of PM2.5 AQI. Hovering over a parish will trigger a tooltip, providing detailed air quality information for that location.

Users can zoom in or out of the map using the provided buttons or the scroll wheel.

## Contributing

Contributions to AirQoMaps are highly welcome! If you have any ideas, improvements, or bug fixes, please submit a pull request. Make sure to adhere to the existing coding style, include relevant tests, and update the documentation accordingly.

## License

This project is licensed under the MIT License.

## Acknowledgements

AirQoMaps utilizes various technologies and libraries to deliver its functionality:

- D3.js - JavaScript library for data visualization.
- Bootstrap - CSS framework for responsive web design.
- Flask - Web framework for Python.
- PostgreSQL - Open-source relational database system.
- Redis - In-memory data structure store used for caching.

We are grateful to the developers and maintainers of these tools for their invaluable contributions to the project.

![AirQoMaps Screenshot](static/airqo_maps.png)
![AirQoMaps Screenshot](static/Maps.png)
![AirQoMaps Screenshot](static/progress.png)
<video width="640" height="360" controls>
    <source src="static/map.webm" type="video/webm">
    Your browser does not support the video tag.
</video>


