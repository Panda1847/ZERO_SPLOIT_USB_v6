import platform
import sys
import os
import subprocess

class SystemFingerprint:
    @staticmethod
    def get_info():
        info = {
            "os": platform.system().lower(),
            "release": platform.release(),
            "version": platform.version(),
            "arch": platform.machine(),
            "python_ver": sys.version.split()[0],
            "user": os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'
        }
        
        if info["os"] == "linux":
            try:
                dist = subprocess.check_output(['lsb_release', '-is'], text=True).strip().lower()
                info["distro"] = dist
            except:
                info["distro"] = "unknown"
        
        return info

    @staticmethod
    def is_admin():
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False

if __name__ == "__main__":
    fp = SystemFingerprint.get_info()
    print(f"Detected OS: {fp['os']}")
    print(f"Architecture: {fp['arch']}")
    print(f"Is Admin: {SystemFingerprint.is_admin()}")
