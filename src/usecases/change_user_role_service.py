from domain.services import RoleManager, DomainError

class ChangeUserRoleService:
    def __init__(self, user_repo):
        self.manager = RoleManager(user_repo)

    def change_role(self, user_id: int, new_role_id: int):
        try:
            return self.manager.assign_role(user_id, new_role_id)
        except DomainError as e:
            raise ValueError(str(e))