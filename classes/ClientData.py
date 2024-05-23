from classes.ValidType import ValidType
from classes.Status import Status
from datetime import datetime
from decimal import Decimal


class ClientData:
    header = ValidType(str)
    device_id = ValidType(int)
    timestamp = ValidType(datetime)
    latitude = ValidType(Decimal)
    longitude = ValidType(Decimal)
    status = ValidType(Status)

    def __init__(self):
        self.up = False
        self.right = True

    def __str__(self):
        return (f"Header: {self.header} Device id: {self.device_id} Timestamp: {self.timestamp} "
                f"Latitude: {self.latitude:.4f} Longitude: {self.longitude:.4f} Status: {self.status.value}")

    def start_mocking(self):
        self.right = not self.right
        if self.right:
            self.latitude = self.latitude + Decimal(0.05)
        else:
            if self.up:
                self.longitude = self.longitude + Decimal(0.05)
            else:
                self.longitude = self.longitude + Decimal(-0.05)
        self.up = not self.up
