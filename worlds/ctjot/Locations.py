import json
from typing import NamedTuple


class LocationData(NamedTuple):
    """
    Store the data associated with a Chrono Trigger treasure location
    """
    name: str
    code: int


class CTJoTLocationManager:
    """
    Manage location data.
    """
    _location_data = {}
    _LOCATION_ID_START = 5000

    def __init__(self):
        """
        Read the location_data file and populate the location DB
        """
        import pkgutil
        locations = json.loads(pkgutil.get_data(__name__, "data/location_data.json").decode())
        for key, value in locations.items():
            self._location_data[key] = LocationData(key, value + self._LOCATION_ID_START)

    def get_location_name_to_id_mapping(self) -> dict[str, int]:
        """
        Get a dictionary mapping location names to IDs.
        """
        return {name: location.code for name, location in self._location_data.items()}

    # TODO: Add a get_location method that handles the location ID offset
