import requests

class GPSHttpClient:
    def __init__(self):
        self.base_url = "http://localhost:5000/api/device"

    def lock(self, serial):
        response = requests.post(f"{self.base_url}/lock", json={"ebike_id": serial})
        return response.json()

    def unlock(self, serial):
        response = requests.post(f"{self.base_url}/unlock", json={"ebike_id": serial})
        return response.json()