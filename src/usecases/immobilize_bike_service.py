from domain.services import BikeLocker, DomainError
from infrastructure.services.gps_client_http import GPSHttpClient
from infrastructure.repositories.bike_repository_sqlalchemy import BikeRepository
from domain.entities import Bike

class ImmobilizeBikeService:
    def __init__(self, bike_repo: BikeRepository, gps_client: GPSHttpClient):
        self.bike_repo = bike_repo
        self.gps_client = gps_client
        self.locker = BikeLocker(bike_repo, gps_client)

    def lock_bike(self, bike: Bike, motivo: str) -> Bike:
        try:
            return self.locker.lock(bike, motivo)
        except DomainError as e:
            raise RuntimeError(str(e))

    def unlock_bike(self, bike: Bike) -> Bike:
        if bike.estado_id == 1:
            raise ValueError("La bicicleta ya está desbloqueada.")

        # Intentar desbloquear por GPS primero
        response = self.gps_client.unlock(bike.id)
        if not response.get("success"):
            raise RuntimeError("No se pudo desbloquear la bici vía GPS")

        # Actualizar estado y novedad a "Disponible" (1)
        updated_bike = self.bike_repo.update_state(bike, estado_id=1, novedad_id=1)
        return updated_bike
