# src/domain/services.py

from typing import Optional
from domain.entities import Bike, User
import bcrypt

class DomainError(Exception):
    """Error de dominio genérico."""
    pass

class BikeLocker:
    def __init__(self, bike_repo, gps_client):
        self.bike_repo = bike_repo
        self.gps        = gps_client

    def lock(self, bike, motivo: str) -> Bike:
        motivo = (motivo or "").strip().lower()
        # 1) Validar motivo
        if motivo not in ("robo", "mora"):
            raise ValueError("Motivo inválido. Usa 'robo' o 'mora'.")
        # 2) Validar que no esté ya bloqueada
        if bike.estado_id in (2, 3):
            raise DomainError("La bicicleta ya está bloqueada.")
        # 3) Invocar al GPS mock
        resp = self.gps.lock(bike.id)
        if not resp.get("success", False):
            raise DomainError(f"Error de comunicación con GPS: {resp.get('message')}")
        # 4) Mapear IDs según motivo
        estado_id  = 2 if motivo == "robo" else 3
        novedad_id = 2  # “No Disponible”
        # 5) Actualizar en BD
        return self.bike_repo.update_state(
            bike,
            estado_id=estado_id,
            novedad_id=novedad_id
        )

    def unlock(self, bike) -> Bike:
        # 1) Validar que esté bloqueada
        if bike.estado_id == 1:
            raise ValueError("La bicicleta ya está desbloqueada.")
        # 2) Invocar al GPS mock
        resp = self.gps.unlock(bike.id)
        if not resp.get("success", False):
            raise DomainError(f"Error de comunicación con GPS: {resp.get('message')}")
        # 3) Estado “Disponible” / novedad “Disponible”
        return self.bike_repo.update_state(
            bike,
            estado_id=1,
            novedad_id=1
        )

class RoleManager:
    """
    Servicio para asignar roles a un usuario.
    """
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def assign_role(self, user_id: int, role_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise DomainError("Usuario no encontrado")
        updated = self.user_repo.update_role(user, role_id)
        if not updated:
            raise DomainError("Error al asignar rol al usuario")
        return updated

class Authenticator:
    """
    Servicio de autenticación que compara contraseñas bcrypt.
    """
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_username(username)
        if not user:
            return None
        # Comprueba el hash bcrypt almacenado en user.password_hash
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None
        return user
