from classes import client_a, client_b
from collections import defaultdict
from decimal import Decimal
from datetime import datetime, timedelta, timezone
import math
import json


def save_data_to_file(data):
    # Split the message by commas
    parts = data.split(',')

    # Check if the message has the expected format
    if len(parts) != 6:
        raise ValueError("Invalid message format")

    # Create a dictionary with appropriate keys
    data = {
        "header": parts[0],
        "device_id": parts[1],
        "timestamp": parts[2],
        "latitude": float(parts[3]),
        "longitude": float(parts[4]),
        "status": parts[5]
    }
    path = f"../data/{parts[1]}.json"
    data_list = json_reader(path)
    data_list.append(data)
    json_writer(path, data_list)


def json_writer(path, data):
    with open(path, 'w') as file:
        file.write(json.dumps(data, indent=4))


def json_reader(path):
    try:
        with open(path, 'r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return []


def parse_data(string_data) -> client_a or client_b:
    data = string_data.split(",")
    header = data[0]
    device_id = int(data[1])
    timestamp = datetime.datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S')
    latitude = Decimal(data[3])
    longitude = Decimal(data[4])
    status = data[5]
    if len(status) == 1:
        client = client_a(header, device_id, timestamp, latitude, longitude, status)
    else:
        client = client_b(header, device_id, timestamp, latitude, longitude, status)
    return client


def haversine(lat1, lon1, lat2, lon2) -> Decimal:
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(lambda x: round(math.radians(x), 5), [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    # Radius of Earth in kilometers. Use 3956 for miles.
    r = 6371
    # Calculate the distance
    distance = c * r
    return round(distance, 4)


def calc_routh(device_id) -> Decimal:
    routh = 0
    file_data = json_reader(f"../data/{device_id}.json")
    temp_2 = file_data[0]
    for data in file_data:
        routh += haversine(Decimal(data["latitude"]), Decimal(data["longitude"])
                               , Decimal(temp_2["latitude"]), Decimal(temp_2["longitude"]))
        temp_2 = data
    return routh


def distance_from_start(client) -> Decimal:
    file_data = json_reader(f"../data/{client["device_id"]}.json")
    temp_2 = file_data[0]
    return haversine(Decimal(client["latitude"]), Decimal(client["longitude"]),
                     Decimal(temp_2["latitude"]), Decimal(temp_2["longitude"]))


def count_same_latitude(client) -> int:
    count_dic = defaultdict(int)
    data = json_reader(f"../data/{client["device_id"]}.json")
    latitudes = [entry['latitude'] for entry in data]
    for lat in latitudes:
        count_dic[lat] += 1
    count = 0
    for value in count_dic.values():
        if value > 1:
            count += value
    return count


def show_all_point_from_last_minute(device_id) -> [dict]:
    file_data = json_reader(f"../data/{device_id}.json")
    # Convert timestamps to datetime objects
    for point in file_data:
        timestamp = datetime.strptime(point['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
        if point["status"] == '1':
            # Assuming status '1' indicates local time
            point['timestamp'] = timestamp.replace(tzinfo=timezone.utc)
        else:
            point['timestamp'] = timestamp.astimezone(timezone.utc)
    # Calculate the timestamp for the last minute
    current_time = datetime.now(timezone.utc)
    last_minute = current_time - timedelta(minutes=1)
    # Filter data points from the last minute
    filtered_data = [point for point in file_data if point['timestamp'] > last_minute]

    return filtered_data

