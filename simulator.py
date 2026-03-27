import requests
import time
import random
import math
import threading
import sys

# The exact URL of your Neura Connect Flask Hub
TARGET_URL = "http://127.0.0.1:5000/data"

current_mode = "BASELINE"

def display_menu():
    """CLI to toggle the Virtual Watch state."""
    global current_mode
    while True:
        print("\n=== NEURA CONNECT: VIRTUAL WATCH ===")
        print(f"Current Mode: [{current_mode}]")
        print("1. Set to BASELINE (Resting/Normal)")
        print("2. Set to TREMOR (High Frequency Anomaly)")
        print("0. Quit")
        choice = input("Select command: ")
        
        if choice == '1':
            current_mode = "BASELINE"
        elif choice == '2':
            current_mode = "TREMOR"
        elif choice == '0':
            print("Shutting down simulator...")
            sys.exit(0)

def generate_z_value():
    """Generates synthetic physics data for the wrist's Z-axis."""
    t = time.time()
    if current_mode == "BASELINE":
        # Simulates resting wrist (Gravity 9.8 + slight natural sway)
        return 9.8 + (math.sin(t) * 0.1) + random.uniform(-0.05, 0.05)
    elif current_mode == "TREMOR":
        # Simulates violent, rapid wrist shaking
        return 9.8 + random.uniform(-8.0, 8.0)

def run_telemetry_loop():
    """Blasts JSON data to the Flask Hub at 10 packets per second."""
    print(f"📡 Transmitter online. Blasting telemetry to {TARGET_URL}")
    while True:
        z = generate_z_value()
        
        # The exact JSON structure your app.py is looking for
        payload = {
            "payload": [
                {
                    "name": "accelerometer",
                    "values": {"x": 0.0, "y": 0.0, "z": z}
                }
            ]
        }
        
        try:
            requests.post(TARGET_URL, json=payload, timeout=0.5)
        except requests.exceptions.RequestException:
            pass # Ignore connection drops
            
        time.sleep(0.1)

if __name__ == "__main__":
    # Start the data blaster in the background
    threading.Thread(target=run_telemetry_loop, daemon=True).start()
    # Show the menu in the foreground
    display_menu()