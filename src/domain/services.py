# src/domain/services.py

from typing import Optional
from domain.entities import Bike, User
import bcrypt


class DomainError(Exception):
    """Error de dominio genérico."""
    pass


class BikeLocker:
    """
    Servicio de bloqueo de bicis. Recibe un repositorio de bicis
    y un cliente GPS (con método lock_bike).
    """
    def __init__(self, bike_repo, gps_client):
        self.bike_repo = bike_repo
        self.gps = gps_client

    def lock(self, bike: Bike, motivo: str) -> Bike:
        if motivo_code == 2:        
            estado_id = 2
            novedad_id = 2
        elif motivo_code == 3:     
            estado_id = 3
            novedad_id = 2
        else:
            raise DomainError("Motivo no válido")

        # Llama al GPS
        success = self.gps.lock_bike(bike.id)
        if not success:
            raise DomainError("Fallo al contactar dispositivo GPS")

        # Actualiza en BD y devuelve la entidad actualizada
        updated = self.bike_repo.update_state(bike, estado_id, novedad_id)
        if not updated:
            raise DomainError("Bicicleta no encontrada al actualizar estado")
        return updated


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

        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None

        return user
