from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Bike:
    id: int
    serial: str
    owner_id: int
    estado_id: int
    novedad_id: int
    updated_at: datetime
    owner_username: str
    owner_role: str
    owner_created_at: datetime

@dataclass
class TimelineEntry:
    estado_id: int
    estado_nombre: str
    estado_descripcion: str
    novedad_id: int
    novedad_nombre: str
    fecha: datetime
    actor_username: Optional[str] = None
    actor_role: Optional[str] = None

@dataclass
class User:
    id: int
    username: str
    role: str
    created_at: datetime


