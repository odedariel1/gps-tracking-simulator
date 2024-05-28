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
    count_clients = 1

    def __init__(self):
        self.id = self.count_clients
        ClientData.count_clients += 1
        self.up = False
        self.right = True

    def __str__(self):
        return (f"header: {self.header} device_id: {self.device_id} timestamp: {self.timestamp} "
                f"latitude: {self.latitude:.4f} longitude: {self.longitude:.4f} status: {self.status.value}")

    def __repr__(self):
        return (f"header: {self.header} device_id: {self.device_id} timestamp: {self.timestamp} "
                f"latitude: {self.latitude:.4f} longitude: {self.longitude:.4f} status: {self.status.value}")

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
        self.timestamp = datetime.now()

