# Phone-Based Interaction Guide for ZERO_SPLOIT_USB v6.0

ZERO_SPLOIT_USB v6.0 "The Singularity Edition" includes a powerful "Live Watch" feature, allowing you to monitor and interact with your C2 sessions directly from your mobile device (smartphone or tablet). This guide will walk you through the process.

## 📱 Prerequisites

Before you begin, ensure you have the following:

1.  **ZERO_SPLOIT_USB v6.0 C2 Server**: Your Command & Control server (VPS) must be set up and running as per the `VPS_DEPLOYMENT_GUIDE.md`.
2.  **SSH Client App**: Install an SSH client application on your mobile device. Recommended apps include:
    *   **Termius** (iOS/Android)
    *   **JuiceSSH** (Android)
    *   **iTerm2** (iOS - for advanced users)
3.  **Internet Connectivity**: Your mobile device needs an active internet connection to reach your VPS.
4.  **SSH Credentials**: You will need the username and password (or SSH key) for your C2 server.

## 📡 Connecting to Your C2 Server via SSH

Follow these steps to establish an SSH connection from your phone to your C2 server:

1.  **Open Your SSH Client App**: Launch the SSH client application on your mobile device.
2.  **Create a New Connection**: Look for an option to add a new host or connection.
3.  **Enter Connection Details**:
    *   **Hostname/IP Address**: Enter the public IP address of your VPS (e.g., `192.0.2.1`).
    *   **Port**: Enter the SSH port for your VPS (default is 22, but may be different if you configured it otherwise during VPS setup). The `SSH_TUNNEL_PORT` for the reverse shell will be different and is specified in the `VPS_DEPLOYMENT_GUIDE.md`.
    *   **Username**: Enter the username for your VPS (e.g., `operator` or `ubuntu`).
    *   **Authentication**: Choose your authentication method:
        *   **Password**: Enter your VPS password.
        *   **SSH Key**: If you use SSH keys, import your private key into the app and select it.
4.  **Save and Connect**: Save the connection details and initiate the connection.
5.  **Accept Host Key (if prompted)**: If this is your first time connecting, you may be asked to accept the host's fingerprint. Confirm it matches your VPS.

Once connected, you will have a command-line interface to your C2 server.

## 👁️ Interacting with Live Watch Sessions

After connecting to your C2 server via SSH, you can interact with the live reverse shell sessions established by ZERO_SPLOIT_USB v6.0. The exact commands will depend on your C2 framework (e.g., Sliver, Metasploit, or a custom handler).

Typically, you will:

1.  **List Active Sessions**: Use your C2 framework's command to list all active reverse shell sessions. For example, in a simple Netcat listener, you'd see incoming connections.
2.  **Interact with a Session**: Select a session to interact with. This will give you a remote shell on the compromised target.
3.  **Execute Commands**: You can now execute commands on the target system as if you were directly on it.

**Example (Conceptual for a simple handler):**

```bash
# On your phone's SSH client, connected to VPS
operator@vps:~$ screen -r <session_name> # Reattach to a named screen session running your handler

# Inside the target's shell (via reverse connection)
whoami
sysinfo
ls -la
```

**Important**: Refer to your `VPS_DEPLOYMENT_GUIDE.md` and the documentation of your chosen C2 framework (e.g., Sliver, Metasploit) for specific commands to manage and interact with sessions.

## 🔒 Security Considerations

*   **Strong Passwords/SSH Keys**: Always use strong, unique passwords or, preferably, SSH keys for your VPS.
*   **Two-Factor Authentication (2FA)**: Enable 2FA on your SSH client app and VPS for an added layer of security.
*   **VPN**: Consider connecting to your VPS via a VPN from your mobile device for enhanced privacy and security.
*   **Secure Wi-Fi**: Only connect from trusted and secure Wi-Fi networks.
*   **Keep Apps Updated**: Ensure your SSH client app and mobile OS are always up-to-date to protect against vulnerabilities.

By following this guide, you can effectively leverage the "Live Watch" capabilities of ZERO_SPLOIT_USB v6.0 from anywhere, providing real-time control over your operations.
