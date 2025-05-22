from domain.services import Authenticator
from flask_jwt_extended import create_access_token

class AuthService:
    def __init__(self, user_repo):
        self.authenticator = Authenticator(user_repo)

    def authenticate(self, username: str, password: str):
        user = self.authenticator.authenticate(username, password)
        if not user:
            return None

        # identity DEBE ser string → usamos el ID como string
        # los demás datos se van en additional_claims
        return create_access_token(
            identity=str(user.id),
            additional_claims={
                "username": user.username,
                "role": user.rol.nombre
            }
        )
