#Primera modificación: Solo SYN (handshake falso)
send(IP(dst="172.18.0.4")/TCP(sport=RandShort(), dport=21, flags="S")) 

#Segunda modificación: Comando PASS fuera de contexto
send(IP(dst="172.18.0.4") / TCP(sport=RandShort(), dport=21, flags="PA", seq=1) / Raw(load="PASS xyz\r\n"))

#Tercera modificación: Comando PASS fuera de contexto
send(IP(dst="172.18.0.4")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="USER root\r\n"))
