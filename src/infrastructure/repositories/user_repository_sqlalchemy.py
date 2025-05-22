from infrastructure.db.models import Usuario
from sqlalchemy.orm import Session
from domain.entities import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str):
        return self.db.query(Usuario).filter(Usuario.username == username).first()

    def get_by_id(self, user_id: int):
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()

    def update_role(self, user, new_role_id: int):
        user.role_id = new_role_id
        self.db.commit()
        self.db.refresh(user)
        return user


        
    def add(self, user: User):
        rol = self.db.query(Rol).filter(Rol.nombre == user.role).first()
        if not rol:
            raise ValueError("Rol inválido")

        nuevo_usuario = Usuario(
            username=user.username,
            password_base64=user.password_base64,
            role_id=rol.id
        )
        self.db.add(nuevo_usuario)
        self.db.commit()

    def get_by_id(self, user_id: int):
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()