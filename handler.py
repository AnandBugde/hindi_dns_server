# handler.py

from dnslib import DNSRecord, RR, QTYPE, A
from socketserver import BaseRequestHandler
from domain_map import load_domain_map

DOMAIN_MAP = load_domain_map()

class DNSHandler(BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        request = DNSRecord.parse(data)
        qname = str(request.q.qname).strip(".")

        print(f"📥 Received DNS request for: {qname}")

        ip = DOMAIN_MAP.get(qname)
        if ip:
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A(ip), ttl=60))
            socket.sendto(reply.pack(), self.client_address)
            print(f"✅ Responded with IP: {ip}")
        else:
            print("❌ Domain not found.")