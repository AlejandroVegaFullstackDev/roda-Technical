# src/interfaces/api/register_blueprint.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from infrastructure.db import SessionLocal
from infrastructure.repositories.user_repository_sqlalchemy import UserRepository
from infrastructure.repositories.bike_repository_sqlalchemy import BikeRepository
from usecases.register_service import RegisterService
from interfaces.api.decorators import roles_required

register_bp = Blueprint("register", __name__)

@register_bp.route("/users/register", methods=["POST"])
@jwt_required()
@roles_required("admin", "operador")
def register_user():
    data = request.get_json()
    actor_id = int(get_jwt_identity())
    repo = UserRepository(SessionLocal())
    service = RegisterService(user_repo=repo)

    try:
        service.register_user(data, actor_id)
        return jsonify({"msg": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@register_bp.route("/ebikes/register", methods=["POST"])
@jwt_required()
@roles_required("admin", "operador")
def register_bike():
    data = request.get_json()
    actor_id = int(get_jwt_identity())

    repo = BikeRepository(SessionLocal())
    service = RegisterService(bike_repo=repo)

    try:
        bike = service.register_bike(data, actor_id)

        return jsonify({
            "msg": "Bicicleta registrada exitosamente",
            "bike": {
                "id": bike.id,
                "serial": bike.serial,
                "estado_id": bike.estado_id,
                "novedad_id": bike.novedad_id,
                "updated_at": bike.updated_at.isoformat(),
                "owner": {
                    "id": bike.owner_id,
                    "username": bike.owner_username,
                    "role": bike.owner_role,
                    "created_at": bike.owner_created_at.isoformat() if bike.owner_created_at else None
                } if bike.owner_id else None
            }
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


@register_bp.route("/ebikes/assign-owner/<int:bike_id>", methods=["PATCH"])
@jwt_required()
@roles_required("admin", "operador")
def assign_bike_owner(bike_id):
    db = SessionLocal()
    data = request.get_json()
    owner_id = data.get("owner_id")
    actor_id = int(get_jwt_identity())

    if not owner_id:
        return jsonify({"msg": "Falta 'owner_id'"}), 400

    try:
        bike_repo = BikeRepository(db)
        bike_repo.assign_owner(bike_id, owner_id, actor_id=actor_id)

        # 🔄 Recargar bici con joins actualizados
        bike = bike_repo.get_by_id(bike_id)

        return jsonify({
            "msg": f"Bici {bike_id} asignada a usuario {owner_id}",
            "bike": {
                "id": bike.id,
                "serial": bike.serial,
                "owner": {
                    "id": bike.owner_id,
                    "username": bike.owner_username,
                    "role": bike.owner_role,
                    "created_at": bike.owner_created_at.isoformat()
                }
            }
        }), 200
    except ValueError as ve:
        return jsonify({"msg": str(ve)}), 400
    except Exception as e:
        return jsonify({"msg": f"Error: {str(e)}"}), 500
