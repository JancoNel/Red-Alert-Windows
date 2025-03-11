# Emergency Alrt script for case of compromise on Windows

from softload import *

import threading
import os

# Block all connections in a separate thread
block_thread = threading.Thread(target=block_all)
block_thread.start()

from hardload import *

# Collect forensic data in a separate thread
data = {}
def collect_data():
    global data
    data = collect_forensic_data()
    kill_processes()  # Add process termination here
    # Write processes to processes.txt
    with open("processes.txt", "w") as f:
        for proc in data["processes"]:
            cmdline = ' '.join(proc['cmdline']) if isinstance(proc['cmdline'], (list, tuple)) else str(proc['cmdline'])
            f.write(f"PID: {proc['pid']}\nName: {proc['name']}\nUsername: {proc['username']}\nCommand Line: {cmdline}\n\n")

data_thread = threading.Thread(target=collect_data)
data_thread.start()

# Wait for both threads to complete
block_thread.join()
data_thread.join()

webhook = get_webhook()

# Allow all data to leave the computer
os.system("netsh advfirewall set allprofiles firewallpolicy allowinbound,allowoutbound")

# Send data to the webhook in a formatted message and @everyone ping
message = (
    "**🚨 Emergency Alert 🚨**\n"
    "@everyone\n"
    "**Hostname:** `{hostname}`\n"
    "**Username:** `{username}`\n"
    "**Date/Time:** `{datetime}`\n\n"
    "**Processes:** See attached file."
).format(
    hostname=data['hostname'],
    username=data['username'],
    datetime=data['datetime']
)

# Send the message in a separate thread
send_thread = threading.Thread(target=send_message, args=(webhook, message))
send_thread.start()
send_thread.join()

# Shutdown system immediately at high speed
os.system("shutdown /s /t 0 /f")
