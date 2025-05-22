from domain.services import Authenticator
from flask_jwt_extended import create_access_token

class AuthService:
    def __init__(self, user_repo):
        self.authenticator = Authenticator(user_repo)

    def authenticate(self, username: str, password: str):
        user = self.authenticator.authenticate(username, password)
        if not user:
            return None

        return create_access_token(identity={
            "id": user.id,
            "username": user.username,
            "role": user.rol.nombre
        })
