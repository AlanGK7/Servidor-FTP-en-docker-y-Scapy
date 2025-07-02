#Primera inyección: Intento de inicio de sesión con una cadena USER muy grande
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="USER " + "A"*1000 + "\r\n"))

#Inyección 2: comando inventado
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="INVALIDCMD arg\r\n"))
