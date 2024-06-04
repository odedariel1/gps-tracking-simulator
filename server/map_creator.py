import os
import gmplot
from decimal import Decimal
from collections import defaultdict
import json


def show_map():
    # Define your latitude and longitude points
    points = []
    folder = "../data"
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                data = json.loads(file.read())
                points.append({"latitude": [Decimal(entry['latitude']) for entry in data],
                               "longitude": [Decimal(entry['longitude']) for entry in data],
                               "name": f"{file_name}"})
    # Calculate the center of the map
    avg_lat = sum(sum(point["latitude"]) for point in points) / sum(len(point["latitude"]) for point in points)
    avg_lon = sum(sum(point["longitude"]) for point in points) / sum(len(point["longitude"]) for point in points)

    # Create a gmplot object centered around the average latitude and longitude
    gmap = gmplot.GoogleMapPlotter(avg_lat, avg_lon, 5)

    # Group points by "name"
    points_by_name = defaultdict(list)
    for point in points:
        points_by_name[point["name"]].append(point)

    # Plot the points and routes by "name"
    for name, pts in points_by_name.items():
        latitudes = pts[0]["latitude"]
        longitudes = pts[0]["longitude"]

        # Scatter plot for the points
        gmap.scatter(latitudes, longitudes, color='maroon', size=50, marker=True)

        # Plot the route connecting the points
        gmap.plot(latitudes, longitudes, 'lightblue', edge_width=2.5)

    # Save the map to an HTML file
    gmap.draw(f'google_map.html')
