from classes.valid_type import ValidType
from datetime import datetime
from decimal import Decimal


class BaseClient:
    header = ValidType(str)
    device_id = ValidType(int)
    timestamp = ValidType(datetime)
    latitude = ValidType(Decimal)
    longitude = ValidType(Decimal)

    def __init__(self, header, device_id, timestamp, latitude, longitude):
        self.header = header
        self.device_id = device_id
        self.timestamp = timestamp
        self.latitude = latitude
        self.longitude = longitude
        self.up = False
        self.right = True

    def __str__(self):
        return (f"{self.header},{self.device_id},{self.timestamp},{self.latitude:.4f},{self.longitude:.4f}")

    def __repr__(self):
        return (f"{self.header},{self.device_id},{self.timestamp},{self.latitude:.4f},{self.longitude:.4f}")


