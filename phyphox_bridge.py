import requests
import time

# 🚨 CHANGE THIS TO THE IP ADDRESS SHOWN ON YOUR PHONE 🚨
PHYPHOX_URL = "http://10.64.224.89:8080/get?lin_z="
FLASK_SYNC_URL = "http://localhost:5000/sync"

def run_bridge():
    print(f"📱 Connecting to Phyphox at {PHYPHOX_URL}...")
    print("📡 Forwarding live Z-axis data to Neura Connect Hub...")
    
    while True:
        try:
            # Get data from the phone
            response = requests.get(PHYPHOX_URL, timeout=2)
            data = response.json()
            
            # Extract the latest Z-axis reading
            if "buffer" in data and "lin_z" in data["buffer"]:
                z_values = data["buffer"]["lin_z"]["buffer"]
                if z_values:
                    latest_z = abs(z_values[-1])  # Get absolute magnitude
                    
                    # Forward to your Flask app
                    payload = {"value": latest_z}
                    requests.post(FLASK_SYNC_URL, json=payload)
                    print(f"🚀 Sent to Edge Hub: {latest_z:.3f}g")
                    
        except Exception as e:
            print(f"⚠️ Connection error: Make sure phone and laptop are on the same Wi-Fi. ({e})")
            
        time.sleep(0.5)  # Poll twice a second

if __name__ == "__main__":
    run_bridge()