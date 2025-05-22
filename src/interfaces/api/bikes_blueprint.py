# src/interfaces/api/bikes.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from infrastructure.db import SessionLocal
from infrastructure.repositories.bike_repository_sqlalchemy import BikeRepository
from usecases.immobilize_bike_service import ImmobilizeBikeService
from infrastructure.services.gps_client_http import GPSHttpClient
from interfaces.api.decorators import roles_required

bikes_bp = Blueprint("bikes", __name__)

@bikes_bp.route("/ebikes", methods=["GET"])
@jwt_required()
def list_bikes():
    db = SessionLocal()
    repo = BikeRepository(db)
    bikes = repo.list_all()

    return jsonify([
        {
            "id": b.id,
            "serial": b.serial,
            "estado_id": b.estado_id,
            "novedad_id": b.novedad_id,
            "updated_at": b.updated_at.isoformat(),
            "owner": {
                "id": b.owner_id,
                "username": b.owner_username,
                "role": b.owner_role,
                "created_at": b.owner_created_at.isoformat() if b.owner_created_at else None
            } if b.owner_id else None
        }
        for b in bikes
    ]), 200


@bikes_bp.route("/ebikes/timeline/<int:bike_id>", methods=["GET"])
@jwt_required()
def get_bike(bike_id):
    db = SessionLocal()
    repo = BikeRepository(db)
    bike = repo.get_by_id(bike_id)
    if not bike:
        return jsonify({"msg": "Bicicleta no encontrada"}), 404

    timeline = repo.get_timeline(bike_id)

    return jsonify({
        "id": bike.id,
        "serial": bike.serial,
        "estado_id": bike.estado_id,
        "novedad_id": bike.novedad_id,
        "owner": {
            "id": bike.owner_id,
            "username": bike.owner_username,
            "role": bike.owner_role,
            "created_at": bike.owner_created_at.isoformat()
        },
        "timeline": [{
            "estado_id": t.estado_id,
            "estado_nombre": t.estado_nombre,
            "estado_descripcion": t.estado_descripcion,
            "novedad_id": t.novedad_id,
            "novedad_nombre": t.novedad_nombre,
            "fecha": t.fecha.isoformat(),
            "actor": {
                "username": t.actor_username,
                "role": t.actor_role
            } if t.actor_username else None
        } for t in timeline]
    }), 200


@bikes_bp.route("/ebikes/<int:bike_id>/lock", methods=["POST"])
@jwt_required()
@roles_required("admin", "operador")
def lock_bike(bike_id):
    db = SessionLocal()
    bike_repo  = BikeRepository(db)
    gps_client = GPSHttpClient()
    bike       = bike_repo.get_by_id(bike_id)

    if not bike:
        return jsonify({"msg": "Bicicleta no encontrada"}), 404

    data   = request.get_json() or {}
    motivo = data.get("motivo", "").lower()

    try:
        service = ImmobilizeBikeService(bike_repo, gps_client)
        updated = service.lock_bike(bike, motivo)
        return jsonify({
            "msg": "Bloqueo solicitado y ejecutado",
            "estado_id": updated.estado_id,
            "novedad_id": updated.novedad_id
        }), 202

    except ValueError:
        # motivo inválido
        return jsonify({"msg": "Motivo inválido. Usa 'mora' o 'robo'"}), 400

    except RuntimeError as err:
        # errores de negocio (ya bloqueada, fallo GPS) devuelven 400
        return jsonify({"msg": str(err)}), 400


@bikes_bp.route("/ebikes/<int:bike_id>/unlock", methods=["POST"])
@jwt_required()
@roles_required("admin", "operador")
def unlock_bike(bike_id):
    db = SessionLocal()
    bike_repo  = BikeRepository(db)
    gps_client = GPSHttpClient()
    bike       = bike_repo.get_by_id(bike_id)

    if not bike:
        return jsonify({"msg": "Bicicleta no encontrada"}), 404

    try:
        service = ImmobilizeBikeService(bike_repo, gps_client)
        updated = service.unlock_bike(bike)
        return jsonify({
            "msg": "Desbloqueo ejecutado exitosamente",
            "estado_id": updated.estado_id,
            "novedad_id": updated.novedad_id
        }), 200

    except ValueError as err:
        # ya estaba desbloqueada
        return jsonify({"msg": str(err)}), 400

    except RuntimeError as err:
        # fallo GPS u otro error de negocio
        return jsonify({"msg": str(err)}), 400
