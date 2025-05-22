from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    usuarios = db.relationship("Usuario", back_populates="rol")

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_base64 = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now())

    rol = db.relationship("Rol", back_populates="usuarios")
    ebikes = db.relationship("EBike", back_populates="owner")

class Estado(db.Model):
    __tablename__ = 'estados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

class Novedad(db.Model):
    __tablename__ = 'novedades'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

class EBike(db.Model):
    __tablename__ = 'ebikes'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(100), unique=True, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete="CASCADE"), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    novedad_id = db.Column(db.Integer, db.ForeignKey('novedades.id'), nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    owner = db.relationship("Usuario", back_populates="ebikes")

class TimelineEBike(db.Model):
    __tablename__ = 'timeline_ebikes'
    id = db.Column(db.Integer, primary_key=True)
    ebike_id = db.Column(db.Integer, db.ForeignKey('ebikes.id', ondelete="CASCADE"), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estados.id'), nullable=False)
    novedad_id = db.Column(db.Integer, db.ForeignKey('novedades.id'), nullable=False)
    change_ts = db.Column(db.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    actor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    comentario = db.Column(db.Text, nullable=True)

    estado = db.relationship("Estado", lazy="joined")
    novedad = db.relationship("Novedad", lazy="joined")
