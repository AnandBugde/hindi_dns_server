# dns_server.py

from socketserver import UDPServer
from handler import DNSHandler
from config import PORT

if __name__ == "__main__":
    print(f"🌐 Hindi DNS Server (DevaDNS) running on port {PORT}...")
    with UDPServer(("0.0.0.0", PORT), DNSHandler) as server:
        server.serve_forever()