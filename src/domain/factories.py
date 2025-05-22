from domain.entities import User, Bike
import base64
from datetime import datetime

class UserFactory:
    @staticmethod
    def create(data: dict) -> User:
        username = data["username"]
        password = base64.b64encode(data["password"].encode("utf-8")).decode("utf-8")
        role = data["role"]

        return User(username=username, password_base64=password, role=role)

class BikeFactory:
    @staticmethod
    def create(data: dict) -> Bike:
        return Bike(
            serial=data["serial"],
            owner_id=data.get("owner_id"),
            estado_id=data.get("estado_id", 1),
            novedad_id=data.get("novedad_id", 1),
            updated_at=datetime.utcnow()
        )
