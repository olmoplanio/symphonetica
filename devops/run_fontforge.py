import os
import platform
import subprocess
import shutil
import sys

def get_fontforge_command():
    system = platform.system()
    if system == "Windows":
        preferred_path = r"C:\Program Files (x86)\FontForgeBuilds\bin\fontforge.exe"
        if os.path.exists(preferred_path):
            return preferred_path
        return shutil.which("fontforge.exe")
    else:
        return shutil.which("fontforge")

def main():
    if len(sys.argv) < 2:
        print("❌ Missing argument: please specify the FontForge script to run.")
        print("Usage: python run-fontforge.py <script-path> [args...]")
        sys.exit(1)

    script_path = os.path.abspath(sys.argv[1])
    forwarded_args = [os.path.abspath(arg) if os.path.exists(arg) else arg for arg in sys.argv[2:]]

    if not os.path.exists(script_path):
        print(f"❌ Script file not found: {script_path}")
        sys.exit(1)

    fontforge_cmd = get_fontforge_command()
    if not fontforge_cmd:
        print("❌ FontForge not found.")
        if platform.system() == "Windows":
            print("↳ Expected at:")
            print("   C:\\Program Files (x86)\\FontForgeBuilds\\bin\\fontforge.exe")
        else:
            print("↳ Make sure 'fontforge' is available in your system PATH.")
        sys.exit(1)

    command = [fontforge_cmd, "-script", script_path] + forwarded_args

    try:
        print(f"▶ Running FontForge: {' '.join(command)}")
        subprocess.run(command, check=True)
        print("✅ FontForge script completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ FontForge failed with error:")
        print(e)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
