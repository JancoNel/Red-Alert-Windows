# Lockdown

> **Lockdown** is a Windows-focused emergency response tool that automates system isolation, forensic capture, and full shutdown the moment compromise is detected. Built to integrate with EDR tools or custom detection scripts, it reacts instantly and surgically.

---

## 🧠 Core Features

- 🔒 Blocks all network connections instantly
- 🧹 Terminates potentially dangerous or suspicious processes
- 📦 Captures detailed forensic info (processes, host/user/session)
- 📡 Sends alert + forensic dump via Discord webhook
- 💥 Immediately shuts down the system to stop further breach
- ⚙️ Designed to be called by EDR/XDR as an auto-response binary

---

## ⚙️ How It Works

1. **Network lockdown**: Blocks all traffic via `netsh`
2. **Forensic sweep**: Gathers host info and running processes
3. **Process purge**: Terminates risky or untrusted processes
4. **Webhook dispatch**: Sends formatted alert and attaches logs
5. **Self-release + shutdown**: Reopens network briefly for exfil, then forces shutdown

---

## 🛠️ Setup

1. Clone the repo
2. Set your Discord webhook inside the code (in `get_webhook()` or a config file)
3. Compile using PyInstaller:

```bash
pyinstaller --onefile --noconsole main.py
```

> You may optionally modify which processes to terminate inside `kill_processes()` in `hardload.py`

---

## 🚨 When to Use

This is not an antivirus. It’s a **"pull the plug" script**:
- Detected RAT or ransomware activity
- Attacker persistence confirmed
- Suspicious lateral movement
- Remote desktop breach suspected

Use it to **contain and alert**, not to recover.

---

## 🔐 Requirements

- **Administrator privileges** to run
- **Discord webhook** to receive alerts/logs

---

## 💬 Sample Alert

```
🚨 Emergency Alert 🚨
@everyone
Hostname: [REDACTED]
Username: [REDACTED]
Date/Time: [UTC]
Processes: See attached file.
```

---

## 🧑‍💻 Author

**JancoNel**

---

> **Disclaimer:** For educational, defensive, and incident response purposes only. Misuse is your responsibility. You break it, you buy it.

---
