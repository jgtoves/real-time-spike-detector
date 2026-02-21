import subprocess
import json
import time
import statistics
from datetime import datetime

# --- Configuration ---
WINDOW_SIZE = 10 
SPIKE_THRESHOLD = 15  # Alert if signal jumps by 15 dBm or more (e.g. -80 to -65)

rssi_history = []

def get_wifi_rssi():
    """Pulls WiFi Signal Strength using Termux API."""
    try:
        res = subprocess.check_output(['termux-wifi-connectioninfo'])
        data = json.loads(res)
        return data.get('rssi') # Returns a negative int (e.g. -65)
    except:
        return None

print("--- ANDROID SIGNAL SENTRY ACTIVE ---")
print("[*] Monitoring for Signal Addition/Summation...")

try:
    while True:
        current_rssi = get_wifi_rssi()
        
        if current_rssi is not None:
            # We use absolute value to make the math 'Square'
            val = abs(current_rssi)
            rssi_history.append(val)
            
            if len(rssi_history) > WINDOW_SIZE:
                rssi_history.pop(0)
            
            if len(rssi_history) == WINDOW_SIZE:
                avg_val = statistics.mean(rssi_history)
                
                # Logic: If current signal is significantly STRONGER (lower absolute value)
                if val < (avg_val - SPIKE_THRESHOLD):
                    print(f"\n[!!!] SIGNAL ADDITION DETECTED [!!!]")
                    print(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
                    print(f"SUDDEN JUMP: {current_rssi} dBm (Previous Avg: -{round(avg_val,1)})")
                    print("[*] Probable proximity device or 'Stingray' activation.")
                else:
                    print(f"Perimeter Clear | Current: {current_rssi} dBm | Avg: -{round(avg_val,1)}", end='\r')
        
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[!] Sentry Offline.")
