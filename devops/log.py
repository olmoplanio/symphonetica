import os
import time

bin_dir = "bin"

if not os.path.exists(bin_dir):
    print("No /bin directory found.")
    exit(1)

print("Compiled font files with timestamps:\n")

for file in sorted(os.listdir(bin_dir)):
    if file.endswith(".ttf") or file.endswith(".otf"):
        full_path = os.path.join(bin_dir, file)
        mod_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(full_path)))
        print(f"{file:20} — {mod_time}")
