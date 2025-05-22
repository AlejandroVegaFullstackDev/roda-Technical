from domain.entities import User, Bike
import base64
from datetime import datetime

class UserFactory:
    @staticmethod
    def create(data: dict) -> User:
        username = data.get("username")
        password = data.get("password")  # ← ahora se espera este campo plano
        role_id = data.get("role_id")

        if not username or not password or not role_id:
            raise DomainError("Faltan campos obligatorios: 'username', 'password' o 'role_id'")

        role_map = {
            1: "admin",
            2: "operador",
            3: "cliente"
        }

        role_name = role_map.get(role_id)
        if not role_name:
            raise DomainError("El role_id proporcionado no existe")

        password_b64 = base64.b64encode(password.encode("utf-8")).decode("utf-8")

        return User(
            username=username,
            password_base64=password_b64,
            role=role_name
        )

class BikeFactory:
    @staticmethod
    def create(data: dict) -> Bike:
        return Bike(
            serial=data["serial"],
            owner_id=data.get("owner_id"),
            estado_id=data.get("estado_id", 1),
            novedad_id=data.get("novedad_id", 1),
            updated_at=datetime.utcnow(),
            owner_username=None,
            owner_role=None,
            owner_created_at=None
        )  
