from abc import ABC, abstractmethod

class AbstractBikeRepository(ABC):
    @abstractmethod
    def get_by_id(self, bike_id: int): pass

    @abstractmethod
    def update_state(self, bike, estado_id: int, novedad_id: int): pass

    @abstractmethod
    def list_all(self): pass

    @abstractmethod
    def get_timeline(self, bike_id: int): pass

class AbstractUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int): pass

    @abstractmethod
    def get_by_username(self, username: str): pass

    @abstractmethod
    def update_role(self, user, new_role_id: int): pass
