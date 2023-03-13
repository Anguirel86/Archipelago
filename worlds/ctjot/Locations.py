import json
import os
from pathlib import Path
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

    def __init__(self):
        """
        Read the location_data file and populate the location DB
        """
        base_path = Path(__file__).parent
        file_path = os.path.join(base_path, "data", "location_data.json")
        with open(file_path) as file:
            locations = json.load(file)
            for key, value in locations.items():
                self._location_data[key] = LocationData(key, value)

    def get_location_name_to_id_mapping(self) -> dict[str, int]:
        """
        Get a dictionary mapping location names to IDs.
        """
        return {name: location.code for name, location in self._location_data.items()}
