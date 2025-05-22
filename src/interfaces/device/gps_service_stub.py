from flask import Blueprint, request, jsonify

device_bp = Blueprint("device", __name__)

@device_bp.route("/lock", methods=["POST"])
def simulate_lock():
    data = request.get_json()
    ebike_id = data.get("ebike_id")

    if not ebike_id:
        return jsonify({"success": False, "message": "Falta ebike_id"}), 400

    # Simulación del autolock: siempre retorna éxito
    return jsonify({
        "success": True,
        "ebike_id": ebike_id,
        "message": "Bloqueo simulado exitosamente"
    }), 200

@device_bp.route("/unlock", methods=["POST"])
def simulate_unlock():
    data = request.get_json()
    ebike_id = data.get("ebike_id")

    if not ebike_id:
        return jsonify({"success": False, "message": "Falta ebike_id"}), 400

    return jsonify({
        "success": True,
        "ebike_id": ebike_id,
        "message": "Desbloqueo simulado exitosamente"
    }), 200
