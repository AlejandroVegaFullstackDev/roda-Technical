from flask_jwt_extended import get_jwt
from functools import wraps
from flask import jsonify

def roles_required(*allowed_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")

            if role not in allowed_roles:
                return jsonify({"msg": f"Acceso denegado: se requiere uno de {allowed_roles}"}), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper
