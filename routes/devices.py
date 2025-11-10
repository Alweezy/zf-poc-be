from flask import Blueprint, jsonify, request
from services.device_service import fetch_device_readings

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/devices/<device_id>/readings", methods=["GET"])
def get_device_readings(device_id):
    """Proxy endpoint to fetch readings for a given device."""
    start_time = request.args.get("startTime")
    end_time = request.args.get("endTime")
    resolution = request.args.get("resolution")
    measurement = request.args.get("measurement")

    missing = [p for p, v in {
        "startTime": start_time,
        "endTime": end_time,
        "resolution": resolution,
        "measurement": measurement,
    }.items() if not v]

    if missing:
        return jsonify({"error": f"Missing required query params: {', '.join(missing)}"}), 400

    data, error = fetch_device_readings(device_id, start_time, end_time, resolution, measurement)
    if error:
        return jsonify({"error": error}), 502

    return jsonify(data)
