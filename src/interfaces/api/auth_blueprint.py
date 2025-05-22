from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager
from infrastructure.db import SessionLocal
from infrastructure.repositories.user_repository_sqlalchemy import UserRepository
from usecases.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    db = SessionLocal()
    data = request.get_json()
    username = data.get("usuario")
    password = data.get("clave")

    if not username or not password:
        return jsonify({"msg": "Faltan credenciales"}), 400

    service = AuthService(UserRepository(db))
    token = service.authenticate(username, password)

    if not token:
        return jsonify({"msg": "Credenciales inválidas"}), 401

    return jsonify({"access_token": token}), 200
