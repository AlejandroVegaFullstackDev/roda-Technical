# src/interfaces/api/users_blueprint.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from interfaces.api.decorators import roles_required
from infrastructure.db import SessionLocal
from infrastructure.repositories.user_repository_sqlalchemy import UserRepository
from usecases.change_user_role_service import ChangeUserRoleService

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/<int:user_id>/role", methods=["POST"])
@jwt_required()
@roles_required("admin")
def set_user_role(user_id):
    db = SessionLocal()
    data = request.get_json()
    role_id = data.get("role_id")

    if not role_id:
        return jsonify({"msg": "Falta 'role_id'"}), 400

    try:
        service = ChangeUserRoleService(UserRepository(db))
        user = service.change_role(user_id, role_id)
        return jsonify({
            "msg": "Rol actualizado",
            "user_id": user.id,
            "nuevo_rol_id": user.role_id,
            "nuevo_rol_nombre": user.rol.nombre if hasattr(user, 'rol') else ""
        }), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500