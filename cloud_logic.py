"""Cloud bridge layer for Neura Connect integrations."""

from __future__ import annotations

import json
import os
from typing import Any

import requests

FEATHERLESS_API_KEY = os.getenv("FEATHERLESS_API_KEY")
FEATHERLESS_URL = os.getenv(
    "FEATHERLESS_URL", "https://api.featherless.ai/v1/chat/completions"
)


def fetch_environment() -> dict[str, Any]:
    """
    Simulate a Bright Data scrape result for environmental stressors.

    Returns a deterministic high-heat / poor-AQI payload for demo flow.
    """
    return {
        "source": "bright_data_simulated",
        "location": "Hyderabad",
        "temperature_c": 42,
        "aqi": 178,
        "summary": "Extreme heat with poor air quality",
    }


def _extract_json_object(text: str) -> dict[str, Any]:
    """Extract and parse the first JSON object from model output."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def _fallback_decision(variance: float, env_data: dict[str, Any], reason: str) -> dict[str, str]:
    return {
        "severity": "HIGH" if variance >= 2.5 else "MODERATE",
        "audio_instruction": "Please stop moving, sit down in shade, and hydrate now.",
        "clinical_reasoning": (
            f"Fallback triage: variance={variance:.3f}, temp={env_data.get('temperature_c')}, "
            f"aqi={env_data.get('aqi')}; reason={reason}"
        ),
    }


def get_triage_decision(variance: float, env_data: dict[str, Any]) -> dict[str, str]:
    """
    Ask Featherless (Llama-3-8B) for triage and enforce pure JSON response.

    Output schema:
    - severity
    - audio_instruction
    - clinical_reasoning
    """
    if not FEATHERLESS_API_KEY:
        return _fallback_decision(variance, env_data, "FEATHERLESS_API_KEY missing")

    system_prompt = (
        "You are Neura Connect's clinical triage model. "
        "Return ONLY a valid JSON object. No markdown. No prose."
    )
    user_prompt = (
        "Given telemetry and environment, classify urgency and give one spoken instruction.\n"
        f"variance: {variance:.5f}\n"
        f"environment: {json.dumps(env_data, separators=(',', ':'))}\n"
        "Respond with EXACT keys only: "
        '{"severity":"LOW|MODERATE|HIGH|CRITICAL","audio_instruction":"...","clinical_reasoning":"..."}'
    )

    headers = {
        "Authorization": f"Bearer {FEATHERLESS_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        response = requests.post(FEATHERLESS_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        parsed = _extract_json_object(content)
        required_keys = {"severity", "audio_instruction", "clinical_reasoning"}
        if not required_keys.issubset(parsed.keys()):
            missing = sorted(required_keys - set(parsed.keys()))
            return _fallback_decision(variance, env_data, f"missing keys: {missing}")
        return {
            "severity": str(parsed["severity"]),
            "audio_instruction": str(parsed["audio_instruction"]),
            "clinical_reasoning": str(parsed["clinical_reasoning"]),
        }
    except Exception as exc:
        return _fallback_decision(variance, env_data, str(exc))


def sync_device_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """
    Entry point used by backend app when anomaly events are triggered.
    """
    variance_value = float(payload.get("value", 0.0))
    env_data = fetch_environment()
    triage = get_triage_decision(variance_value, env_data)
    return {
        "status": "processed",
        "environment": env_data,
        "triage": triage,
        "event": payload,
    }