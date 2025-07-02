
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="USER " + "A"*1000 + "\r\n"))

send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="INVALIDCMD arg\r\n"))
