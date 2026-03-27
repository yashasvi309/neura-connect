"""Flask backend for Neura Connect telemetry processing."""

from __future__ import annotations

import threading
from typing import Any

import pyttsx3
from flask import Flask, jsonify, request

from cloud_logic import sync_device_payload

app = Flask(__name__)

# EWMV/TRM parameters
ALPHA = 0.2
VARIANCE_THRESHOLD = 2.5

# Recursive state for z-axis stream
trm_state = {
    "initialized": False,
    "ew_mean": 0.0,
    "ew_variance": 0.0,
}


def update_ewmv(sample_z: float, alpha: float = ALPHA) -> tuple[float, float]:
    """
    Update exponentially weighted moving mean and variance recursively.

    Variance update:
      var_t = (1 - alpha) * (var_{t-1} + alpha * (x_t - mean_{t-1})^2)
    """
    if not trm_state["initialized"]:
        trm_state["initialized"] = True
        trm_state["ew_mean"] = sample_z
        trm_state["ew_variance"] = 0.0
        return trm_state["ew_mean"], trm_state["ew_variance"]

    prev_mean = trm_state["ew_mean"]
    prev_var = trm_state["ew_variance"]

    ew_mean = alpha * sample_z + (1.0 - alpha) * prev_mean
    ew_variance = (1.0 - alpha) * (prev_var + alpha * (sample_z - prev_mean) ** 2)

    trm_state["ew_mean"] = ew_mean
    trm_state["ew_variance"] = ew_variance
    return ew_mean, ew_variance


def speak_warning_async(message: str) -> None:
    """Speak a warning without blocking request handling."""

    def _speak() -> None:
        try:
            engine = pyttsx3.init()
            engine.say(message)
            engine.runAndWait()
        except Exception:
            # Keep telemetry pipeline resilient if TTS fails.
            pass

    threading.Thread(target=_speak, daemon=True).start()


def _extract_z(payload: dict[str, Any]) -> float:
    """Extract z value from supported telemetry payload formats."""
    if "z" in payload:
        return float(payload["z"])

    accel = payload.get("accelerometer")
    if isinstance(accel, dict) and "z" in accel:
        return float(accel["z"])

    raise ValueError("Missing z-axis accelerometer value.")


@app.post("/data")
def ingest_data():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid or missing JSON body."}), 400

    try:
        z_value = _extract_z(payload)
    except (TypeError, ValueError) as exc:
        return jsonify({"error": str(exc)}), 400

    mean, variance = update_ewmv(z_value)
    anomaly = variance > VARIANCE_THRESHOLD

    cloud_response: dict[str, Any] | None = None
    if anomaly:
        event_payload = {
            "event": "anomaly_detected",
            "metric": "z_axis_ewmv",
            "threshold": VARIANCE_THRESHOLD,
            "value": variance,
            "telemetry": payload,
        }
        cloud_response = sync_device_payload(event_payload)
        speak_warning_async("Warning. Neura Connect detected an anomaly.")

    return jsonify(
        {
            "status": "ok",
            "z": z_value,
            "ew_mean": mean,
            "ew_variance": variance,
            "threshold": VARIANCE_THRESHOLD,
            "anomaly": anomaly,
            "cloud_response": cloud_response,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
