# src/interfaces/device/gps_service_stub.py

from flask import Blueprint, request, jsonify
import time, random

# Blueprint con prefijo /api/device
device_bp = Blueprint("device", __name__, url_prefix="/api/device")

# Estado en memoria: { ebike_id: "locked" | "unlocked" }
_status_store = {}

def _simulate_delay():
    """Simula latencia de red entre 100–300 ms (opcional)."""
    time.sleep(random.uniform(0.1, 0.3))

def _maybe_fail():
    """10% de probabilidad de error (opcional)."""
    return random.random() < 0.1

@device_bp.route("/lock", methods=["POST"])
def simulate_lock():
    data = request.get_json() or {}
    ebike_id = data.get("ebike_id")
    if ebike_id is None:
        return jsonify({"success": False, "message": "Falta ebike_id"}), 400

    _simulate_delay()
    if _maybe_fail():
        return jsonify({
            "success": False,
            "ebike_id": ebike_id,
            "message": "Error de comunicación con GPS"
        }), 502

    _status_store[str(ebike_id)] = "locked"
    return jsonify({
        "success": True,
        "ebike_id": ebike_id,
        "status": "locked",
        "message": "Bloqueo simulado exitosamente"
    }), 200

@device_bp.route("/unlock", methods=["POST"])
def simulate_unlock():
    data = request.get_json() or {}
    ebike_id = data.get("ebike_id")
    if ebike_id is None:
        return jsonify({"success": False, "message": "Falta ebike_id"}), 400

    _simulate_delay()
    if _maybe_fail():
        return jsonify({
            "success": False,
            "ebike_id": ebike_id,
            "message": "Error de comunicación con GPS"
        }), 502

    _status_store[str(ebike_id)] = "unlocked"
    return jsonify({
        "success": True,
        "ebike_id": ebike_id,
        "status": "unlocked",
        "message": "Desbloqueo simulado exitosamente"
    }), 200

@device_bp.route("/status/<int:ebike_id>", methods=["GET"])
def get_status(ebike_id):
    status = _status_store.get(str(ebike_id), "unknown")
    return jsonify({
        "ebike_id": ebike_id,
        "status": status
    }), 200
