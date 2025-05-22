# src/infrastructure/services/gps_client_http.py

import requests

class GPSHttpClient:
    def __init__(self):
        self.base_url = "http://localhost:5000/api/device"

    def lock(self, bike_id: int):
        resp = requests.post(f"{self.base_url}/lock", json={"ebike_id": bike_id}, timeout=3)
        resp.raise_for_status()
        return resp.json()

    def unlock(self, bike_id: int):
        resp = requests.post(f"{self.base_url}/unlock", json={"ebike_id": bike_id}, timeout=3)
        resp.raise_for_status()
        return resp.json()

    def status(self, bike_id: int):
        resp = requests.get(f"{self.base_url}/status/{bike_id}", timeout=3)
        resp.raise_for_status()
        return resp.json()
