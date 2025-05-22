from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from infrastructure.db import SessionLocal
from infrastructure.repositories.bike_repository_sqlalchemy import BikeRepository
from usecases.immobilize_bike_service import ImmobilizeBikeService
from infrastructure.services.gps_client_http import GPSHttpClient
from interfaces.api.decorators import roles_required
import traceback

events_bp = Blueprint("events", __name__)

@events_bp.route("/events/immobilize", methods=["POST"])
@jwt_required()
@roles_required("admin", "operador", "cliente")
def recibir_evento():
    db = SessionLocal()
    data = request.get_json()
    bike_id = data.get("ebike_id")
    motivo = data.get("motivo", "").lower()

    if not bike_id or motivo not in ["mora", "robo"]:
        return jsonify({"msg": "Falta 'ebike_id' o 'motivo' inválido"}), 400

    repo = BikeRepository(db)
    gps = GPSHttpClient()
    service = ImmobilizeBikeService(repo, gps)

    try:
        bike = repo.get_by_id(bike_id)
        if not bike:
            return jsonify({"msg": "Bici no encontrada"}), 404

        user = get_jwt_identity()
        if motivo == "mora" and user.get("role") == "cliente":
            return jsonify({"msg": "Clientes no pueden reportar mora"}), 403

        service.lock_bike(bike, motivo)
        return jsonify({"msg": f"Bici {bike_id} bloqueada por {motivo}"}), 200

    except Exception as e:
        print("🔴 Error en /events/immobilize:", str(e))
        traceback.print_exc()
        return jsonify({"msg": f"Error al bloquear: {str(e)}"}), 500
