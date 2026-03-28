import subprocess
import time
import webbrowser
import os
import sys

print("🚀 Initiating Neura Connect V2.0 Launch Sequence...\n")

# 1. Open the UI Dashboard in your default browser
ui_path = os.path.abspath(os.path.join("frontend", "index.html"))
print(f"🖥️  Opening Dashboard: {ui_path}")
webbrowser.open(f"file://{ui_path}")

# 2. Start the Edge Hub (Flask)
print("🧠 Starting Edge Hub (app.py)...")
# Using sys.executable ensures it uses your current Python environment
hub_process = subprocess.Popen([sys.executable, "app.py"])

# Give Flask 2 seconds to fully boot up before sending data to it
time.sleep(2) 

# 3. Start the Hardware Bridge (Phyphox)
print("📱 Starting Phyphox Bridge...")
bridge_process = subprocess.Popen([sys.executable, "phyphox_bridge.py"])

print("\n✅ SYSTEM ONLINE AND LISTENING FOR ANOMALIES.")
print("⚠️  Keep this terminal open! Press Ctrl+C here to safely shut down everything.\n")

try:
    # Keeps the launcher running so it holds the other processes alive
    hub_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Emergency Stop detected. Shutting down Neura Connect...")
    hub_process.terminate()
    bridge_process.terminate()
    print("Done. Go crush the pitch!")