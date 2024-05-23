from classes.ClientData import ClientData
from classes.Status import Status
from datetime import datetime
from decimal import Decimal

client1 = ClientData()
client2 = ClientData()

# set clients mocks!
try:
    client1.header = "$GPRMC"
    client1.device_id = 123456789
    client1.timestamp = datetime.strptime("2024-05-21 14:32:10", '%Y-%m-%d %H:%M:%S')
    client1.latitude = Decimal(37.7749)
    client1.longitude = Decimal(-122.4194)
    client1.status = Status.first

    client2.header = "#TRACK"
    client2.device_id = 987654321
    client2.timestamp = datetime.strptime("2024-05-21 14:32:10", '%Y-%m-%d %H:%M:%S')
    client2.latitude = Decimal(34.0522)
    client2.longitude = Decimal(-118.2437)
    client2.status = Status.second

except ValueError as ex:
    print(ex)



