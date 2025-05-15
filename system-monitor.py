import json
import re
from pypresence import Presence
import time
import psutil
from datetime import datetime
import platform
import subprocess

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from file"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'client_id': '', 'large_image': 'logo', 'large_image_url': '', 'large_text': 'System Monitor'}

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def ask_for_image(config):
    """Ask the user for the image name from Discord Dev Portal"""
    print(f"\nCurrent image name: {config['large_image'] or 'none'}")
    if new_name := input("Enter the image name from Discord Dev Portal (press Enter to skip): ").strip():
        config.update({'large_image': new_name})
        save_config(config)
        print(f"\nUse this name in Discord Dev Portal: {new_name}")
    return config

def get_client_id(config):
    """Get Client ID from the user"""
    while True:
        if user_input := input(f"\nEnter Client ID [current: {config['client_id']}]: ").strip():
            config['client_id'] = user_input
            save_config(config)
            return user_input
        elif config['client_id']:
            return config['client_id']
        print("You must provide a Client ID!")

# Initialization
config = load_config()
config = ask_for_image(config)
client_id = get_client_id(config)
rpc = Presence(client_id)
rpc.connect()

# Time since January 1, 1970 (Unix epoch)
start_time = time.time()

def get_uptime():
    """Return time since January 1, 1970 in D:HH:MM:SS format"""
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}d {hours:02d}h {minutes:02d}m {seconds:02d}s"

def get_stats():
    """Get system stats with a short interval"""
    try:
        cpu = psutil.cpu_percent(interval=1.0)
        ram = psutil.virtual_memory().percent
        
        gpu = ""
        gpu_type = None
        try:
            import GPUtil
            if gpus := GPUtil.getGPUs():
                gpu_name = gpus[0].name.lower()
                if 'nvidia' in gpu_name:
                    gpu_type = 'nvidia'
                elif 'amd' in gpu_name or 'radeon' in gpu_name:
                    gpu_type = 'amd'
                elif 'intel' in gpu_name:
                    gpu_type = 'intel'
        except:
            try:
                subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                gpu_type = 'nvidia'
            except:
                pass
        
        if gpu_type:
            try:
                if gpu_type == 'nvidia':
                    result = subprocess.run(
                        ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader"],
                        capture_output=True, text=True, timeout=0.3
                    )
                    if result.returncode == 0:
                        gpu = f" | GPU: {result.stdout.strip()}"
                elif gpus := GPUtil.getGPUs():
                    gpu = f" | GPU: {gpus[0].load * 100:.0f}%"
            except:
                pass
        
        return f"CPU: {cpu}% | RAM: {ram}%{gpu}"
    except:
        return "Error reading stats"

# Main loop
try:
    while True:
        stats = get_stats()
        
        rpc.update(
            state="System Monitor",
            details=stats,
            large_image=config['large_image'],
            large_text=config['large_text'],
            start=start_time
        )
        
        time.sleep(10)  # Exactly every 10 seconds
        
except KeyboardInterrupt:
    print("\nShutting down system monitor...")
    rpc.close()
except Exception as e:
    print(f"Error: {e}")
    rpc.close()
