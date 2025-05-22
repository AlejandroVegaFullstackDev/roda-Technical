from domain.entities import User, Bike
from domain.factories import UserFactory, BikeFactory
from domain.services import DomainError

class RegisterService:
    def __init__(self, user_repo=None, bike_repo=None):
        self.user_repo = user_repo
        self.bike_repo = bike_repo

    def register_user(self, data: dict, current_user: dict):
        requester_role = current_user["role"]
        target_role = data.get("role")

        if requester_role == "operador" and target_role == "operador":
            raise DomainError("Los operadores no pueden registrar otros operadores")
        if requester_role == "cliente":
            raise DomainError("Los clientes no pueden registrar usuarios")

        user = UserFactory.create(data)
        self.user_repo.add(user)

    def register_bike(self, data: dict):
        if "id" in data and "owner_id" in data and len(data.keys()) == 2:
            self.bike_repo.assign_owner(data["id"], data["owner_id"])
        else:
            bike = BikeFactory.create(data)
            self.bike_repo.add(bike)
