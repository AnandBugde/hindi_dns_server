import json
from dnslib import DNSRecord, RR, QTYPE, A
from socketserver import UDPServer, BaseRequestHandler

# Load domain mappings from JSON file
def load_domain_map():
    with open("domain_map.json", "r", encoding="utf-8") as f:
        return json.load(f)

DOMAIN_MAP = load_domain_map()

class DNSHandler(BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).strip(".")

        print(f"📥 Received DNS request for: {qname}")

        ip = DOMAIN_MAP.get(qname, None)
        if ip:
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=60))
            socket.sendto(reply.pack(), self.client_address)
            print("✅ Responded with IP: {ip}")
        else:
            print("❌ Domain not found.")
            # Optionally return NXDOMAIN or forward to upstream DNS

if __name__ == "__main__":
    print("🌐 Hindi DNS Server (DevaDNS) running on port 5353...")
    with UDPServer(("0.0.0.0", 5353), DNSHandler) as server:
        server.serve_forever()
