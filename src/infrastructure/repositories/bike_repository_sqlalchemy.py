from infrastructure.db.models import EBike, TimelineEBike, Usuario, Rol
from domain.entities import Bike, TimelineEntry
from domain.repositories import AbstractBikeRepository
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime


class BikeRepository(AbstractBikeRepository):
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        bikes = (
            self.db.query(EBike)
            .outerjoin(Usuario, EBike.owner_id == Usuario.id)
            .outerjoin(Rol, Usuario.role_id == Rol.id)
            .all()
        )

        return [
            Bike(
                id=b.id,
                serial=b.serial,
                owner_id=b.owner.id if b.owner else None,
                estado_id=b.estado_id,
                novedad_id=b.novedad_id,
                updated_at=b.updated_at,
                owner_username=b.owner.username if b.owner else None,
                owner_role=b.owner.rol.nombre if b.owner and b.owner.rol else None,
                owner_created_at=b.owner.created_at if b.owner else None
            )
            for b in bikes
        ]

    def get_by_id(self, bike_id: int) -> Bike:
        result = (
            self.db.query(EBike, Usuario, Rol)
            .outerjoin(Usuario, EBike.owner_id == Usuario.id)
            .outerjoin(Rol, Usuario.role_id == Rol.id)
            .filter(EBike.id == bike_id)
            .first()
        )

        if not result:
            raise ValueError("Bicicleta no encontrada")

        ebike, usuario, rol = result

        return Bike(
            id=ebike.id,
            serial=ebike.serial,
            estado_id=ebike.estado_id,
            novedad_id=ebike.novedad_id,
            updated_at=ebike.updated_at,
            owner_id=usuario.id if usuario else None,
            owner_username=usuario.username if usuario else None,
            owner_role=rol.nombre if rol else None,
            owner_created_at=usuario.created_at if usuario else None
        )

    def get_timeline(self, bike_id: int):
        query = (
            self.db.query(
                TimelineEBike,
                Usuario.username.label("actor_username"),
                Rol.nombre.label("actor_role")
            )
            .outerjoin(Usuario, TimelineEBike.actor_id == Usuario.id)
            .outerjoin(Rol, Usuario.role_id == Rol.id)
            .filter(TimelineEBike.ebike_id == bike_id)
            .order_by(TimelineEBike.change_ts.desc())  # Orden estricto por fecha
        )

        resultados = query.all()

        timeline = [
            TimelineEntry(
                estado_id=t.estado_id,
                estado_nombre=t.estado.nombre,
                estado_descripcion=t.estado.descripcion,
                novedad_id=t.novedad_id,
                novedad_nombre=t.novedad.nombre,
                fecha=t.change_ts,  # Ya viene con precisión de microsegundos desde PostgreSQL
                actor_username=actor_username,
                actor_role=actor_role
            )
            for t, actor_username, actor_role in resultados
        ]

        return timeline  # Ya ordenado desde el query

    def update_state(self, bike: Bike, estado_id: int, novedad_id: int):
        b = self.db.query(EBike).filter(EBike.id == bike.id).first()
        if not b:
            return None

        b.estado_id = estado_id
        b.novedad_id = novedad_id
        self.db.commit()

        # Reutiliza get_by_id para construir la entidad completa con campos extra
        return self.get_by_id(bike.id)

    def assign_owner(self, bike_id: int, owner_id: int, actor_id: int = None) -> Optional[Bike]:
        bike = self.db.query(EBike).filter(EBike.id == bike_id).first()
        if not bike:
            return None

        if bike.owner_id is not None:
            raise ValueError("La bicicleta ya tiene un propietario asignado.")

        bike.owner_id = owner_id
        self.db.commit()
        self.db.refresh(bike)

        # 👇 Insertar en timeline con auditoría
        timeline_entry = TimelineEBike(
            ebike_id=bike.id,
            estado_id=bike.estado_id,
            novedad_id=bike.novedad_id,
            change_ts=datetime.utcnow(),
            actor_id=actor_id,
            comentario=f"Asignada a usuario {owner_id}"
        )
        self.db.add(timeline_entry)
        self.db.commit()

        return Bike(  # 👈 ahora está correctamente indentado
            id=bike.id,
            serial=bike.serial,
            estado_id=bike.estado_id,
            novedad_id=bike.novedad_id,
            updated_at=bike.updated_at,
            owner_id=bike.owner_id
        )

    def add(self, bike: Bike, actor_id: int = None, comentario: Optional[str] = None) -> Bike:
        db_bike = EBike(
            serial=bike.serial,
            owner_id=bike.owner_id,
            estado_id=bike.estado_id,
            novedad_id=bike.novedad_id
        )
        self.db.add(db_bike)
        self.db.commit()
        self.db.refresh(db_bike)

        # ⬇ Insertar en timeline con actor y comentario
        timeline_entry = TimelineEBike(
            ebike_id=db_bike.id,
            estado_id=db_bike.estado_id,
            novedad_id=db_bike.novedad_id,
            change_ts=datetime.utcnow(),
            actor_id=actor_id,
            comentario=comentario
        )
        self.db.add(timeline_entry)
        self.db.commit()

        return self.get_by_id(db_bike.id)


        
    def save_changes(self):
        self.db.commit()
    
    def update(self, bike):
        self.db.merge(bike)
        self.db.commit()