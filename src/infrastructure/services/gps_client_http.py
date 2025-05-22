import requests

class GPSHttpClient:
    def __init__(self):
        self.base_url = "http://localhost:5000/api/device"

    def lock(self, bike_id: int):
        response = requests.post(f"{self.base_url}/lock", json={"ebike_id": bike_id})
        return response.json()

    def unlock(self, bike_id: int):
        response = requests.post(f"{self.base_url}/unlock", json={"ebike_id": bike_id})
        return response.json()