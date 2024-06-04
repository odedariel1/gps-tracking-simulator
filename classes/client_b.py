from classes.base_client import BaseClient
from classes.valid_type import ValidType
from datetime import datetime
from decimal import Decimal


class ClientB(BaseClient):
    status = ValidType(str)

    def __init__(self, header, device_id, timestamp, latitude, longitude, status):
        super().__init__(header, device_id, timestamp, latitude, longitude)
        self.status = status

    def __str__(self):
        return super().__str__() + f",{self.status}"

    def __repr__(self):
        return super().__repr__() + f",{self.status}"

    def start_mocking(self, long_dist=0.05, lat_dist=0.1):
        self.right = not self.right
        if self.right:
            self.longitude = self.longitude + Decimal(long_dist)
        else:
            if self.up:
                self.latitude = self.latitude + Decimal(lat_dist)
            else:
                self.latitude = self.latitude - Decimal(lat_dist)
            self.up = not self.up
        self.timestamp = datetime.strptime(datetime.strftime(datetime.now(),
                                                             "%Y-%m-%dT%H:%M:%S.%f")[:-3], "%Y-%m-%dT%H:%M:%S.%f")