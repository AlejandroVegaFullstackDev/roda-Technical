from domain.entities import User, Bike
from domain.factories import UserFactory, BikeFactory
from domain.services import DomainError
from infrastructure.db.models import Rol  # ✅ aquí adentro

class RegisterService:
    def __init__(self, user_repo=None, bike_repo=None):
        self.user_repo = user_repo
        self.bike_repo = bike_repo

    def register_user(self, data: dict, current_user: dict):
        requester_role = current_user["role"]

        if "role_id" not in data:
            raise DomainError("Falta el campo obligatorio 'role_id'")

        role_id = data["role_id"]

        role_map = {
            1: "admin",
            2: "operador",
            3: "cliente"
        }

        role_name = role_map.get(role_id)
        if not role_name:
            raise DomainError("El role_id proporcionado no existe")

        if requester_role == "operador" and role_name == "operador":
            raise DomainError("Los operadores no pueden registrar otros operadores")
        if requester_role == "cliente":
            raise DomainError("Los clientes no pueden registrar usuarios")

        user = UserFactory.create(data)
        self.user_repo.add(user)


    def register_bike(self, data: dict, actor_id: int):
        if "id" in data and "owner_id" in data and len(data.keys()) == 2:
            self.bike_repo.assign_owner(data["id"], data["owner_id"], actor_id=actor_id)
        else:
            comentario = data.get("comentario")  
            bike = BikeFactory.create(data)
            return self.bike_repo.add(bike, actor_id=actor_id, comentario=comentario)


