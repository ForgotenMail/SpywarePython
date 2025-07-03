import socket
def simple_server(port=8888):
    """Simple server - save as separate file"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow reuse
    
    try:
        server.bind(('0.0.0.0', port))
        server.listen(5)
        
        # Get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        print(f"🚀 Server running on {local_ip}:{port}")
        print(f"🏠 Also accessible via 127.0.0.1:{port}")
        print("Press Ctrl+C to stop")
        
        while True:
            client, addr = server.accept()
            print("Accepting connections...")
            print(f"📡 Connection from {addr[0]}")
            print("Getting data from client...")
            data = client.recv(1024)
            if data:
                received = data.decode('utf-8')
                if received == "I<3CatsCauseTheyAreReallyCute":
                    message = f"FOUND YOUR TARGET! IP: {local_ip}, Host: {socket.gethostname()}"
                    print("Correct secret received. Sending response...")
                    client.send(message.encode())
                else:
                    print("Incorrect secret. Closing connection.")
                print("Closing connection...")
                client.close()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except OSError as e:
        if e.errno == 98:
            print("❌ Port 8888 already in use!")
        else:
            print(f"❌ Server error: {e}")
    finally:
        server.close()

# Uncomment to run server directly from this file:
simple_server()

print("\n" + "="*50)
print("INSTRUCTIONS:")
print("1. Save server code as 'server.py'")
print("2. Run: python server.py")
print("3. Run scanner: python scanner.py")
print("="*50)