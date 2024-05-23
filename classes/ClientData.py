from classes.ValidType import ValidType
from datetime import datetime
import decimal


class ClientData:
    id = ValidType(int)
    header = ValidType(str)
    timestamp = ValidType(datetime)
    latitude = ValidType(decimal)
    longitude = ValidType(decimal)
    status = ValidType(str)
