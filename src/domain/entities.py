from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Bike:
    serial: str
    estado_id: int
    novedad_id: int
    updated_at: datetime

    owner_id: Optional[int] = None
    id: Optional[int] = None
    owner_username: Optional[str] = None
    owner_role: Optional[str] = None
    owner_created_at: Optional[datetime] = None

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
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""  
    role: str = ""  
    created_at: Optional[datetime] = None