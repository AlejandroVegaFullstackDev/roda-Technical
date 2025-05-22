class DomainError(Exception): pass

class BikeLocker:
    def __init__(self, bike_repo, gps_client):
        self.bike_repo = bike_repo
        self.gps = gps_client

    def lock(self, bike, motivo: str):
        if motivo == "robo":
            estado_id = 2
            novedad_id = 2
        elif motivo == "mora":
            estado_id = 3
            novedad_id = 2
        else:
            raise DomainError("Motivo no válido")

        success = self.gps.lock_bike(bike.id)
        if not success:
            raise DomainError("Fallo al contactar dispositivo GPS")

        return self.bike_repo.update_state(bike, estado_id, novedad_id)

class RoleManager:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def assign_role(self, user_id: int, role_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise DomainError("Usuario no encontrado")
        return self.user_repo.update_role(user, role_id)

class Authenticator:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def authenticate(self, username: str, password: str):
        user = self.user_repo.get_by_username(username)
        if not user:
            return None

        import base64
        decoded_password = base64.b64decode(user.password_base64).decode("utf-8")
        if password != decoded_password:
            return None

        return user