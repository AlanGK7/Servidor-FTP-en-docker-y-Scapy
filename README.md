# Servidor-FTP-en-docker-y-Scapy

## Descripción
En conjunto, **lftp** y **ProFTPD** forman una pareja ideal para usuarios técnicos o administradores que buscan eficiencia, seguridad y automatización avanzada en sus sistemas. A diferencia de otras combinaciones, esta se enfoca
en un rendimiento sólido desde la terminal y una gestión completa del servidor, lo que la convierte en una opción
preferente en contextos profesionales o de alta demanda técnica.

Los softwares que utilizaremos para el cliente y el servidor serán **lftp** y
**ProFTPD**, respectivamente. A continuación, se ofrecerá una descripción más detallada de los comandos necesarios y del proceso de instalación para cada uno de ellos. Comenzaremos con la configuración del servidor, luego
abordaremos la del cliente y, finalmente, mostraremos cómo establecer la conexión entre ambos.

Como parte del estudio del protocolo **FTP**, se utilizó **Scapy** para interceptar, modificar e inyectar tráfico entre el cliente (lftp) y el servidor (ProFTPD), ambos ejecutándose como contenedores **Docker**.
El objetivo principal fue analizar el comportamiento del servicio FTP ante alteraciones en el protocolo.

> [!IMPORTANT]
> Este proyecto ha sido diseñado y probado exclusivamente en sistemas operativos **Linux**, particularmente distribuciones basadas en **Ubuntu/Debian**.  
> Algunos comandos, rutas y configuraciones pueden no funcionar correctamente en **Windows** o **macOS** sin adaptaciones adicionales.

### 📁 Estructura del Proyecto

```plaintext
┌──────────────┐         docker network: redes_net        ┌──────────────┐
│   Cliente    │  <—————————— comunicación FTP ——————————>│  Servidor    │
│   (lftp)     │                                          │  (ProFTPD)   │
└──────────────┘                                          └──────────────┘
           ⬇                                                  ⬇
     Interfaz virtual                                Interfaz virtual
         br-XXX                                           br-XXX   
               ↘                                        ↙
                   ┌────────────────────────────────┐
                   │     Host (Scapy, Python)       │
                   └────────────────────────────────┘


```


## ⚙️ Instalación

### 🔧 Instalación del servidor
Para la instalación del servidor ProFTPD, se creó una red interna dentro del mismo dispositivo. Aunque este
paso es opcional y no estrictamente necesario, se optó por esta ción con el fin de trabajar en un entorno
más controlado y aislado. 
> [!TIP]
> Es altamente recomendable exponer el puerto 21 sí no optas por una red Docker.

Para ello empezamos creando la red con el siguiente comando:
```bash
sudo docker network create redes_net
```
Con este paso, se crea la red interna. Para el servidor, utilizaremos una imagen de Ubuntu, la cual será conectada
a dicha red. Descargaremos la imagen asignándole el nombre **”servidor”**. Para ello, utilizamos el siguiente comando,
el cual iniciará la descarga correspondiente:

```bash
sudo docker run -dit –name servidor –network redes_net ubuntu bash
```
Una vez finalizada la descarga, verificamos que la imagen de Ubuntu se encuentre disponible localmente en
Docker. Además, accederemos a un contenedor basado en esta imagen mediante un segundo comando. Para ello,
utilizamos los siguientes comandos:

```bash
sudo docker container ls # para verificar la descarga
sudo docker exec -it servidor /bin/bash # para acceder a la bash del contenedor ”servidor”donde se alojara el servidor 
```
A continuación, procederemos con la ción del servidor ProFTPD. Antes de iniciar su instalación, es
importante tener en cuenta ciertos requisitos previos, los cuales se pueden consultar en su documentación oficial.

### Requisitos previos
Para compilar correctamente ProFTPD desde su código fuente, es necesario contar con las siguientes dependencias y condiciones en el sistema:
- **Compilador C ANSI/ISO C89/C90**, por ejemplo GNU `gcc`
- **Herramienta de construcción** `make` (GNU make recomendado, aunque la mayoría de las implementaciones funcionan)
- **Librerías de tiempo de ejecución ANSI C y POSIX**
- **API de sockets BSD** (para la comunicación de red)
- **Espacio en disco disponible**:
  - Aproximadamente 4.5 MB para descomprimir el código fuente
  - Entre 6 y 8 MB para construir (compilar)
  - Cerca de 2 MB para la instalación final

- [proftpd/proftpd](https://github.com/proftpd/proftpd): Repositorio oficial del servidor FTP ProFTPD

Una vez verificados, comenzamos la instalación del conjunto de herramientas básicas para compilar software en
sistemas Debian/Ubuntu ejecutando el siguiente comando:

```bash
sudo apt install -y build-essential
```

Finalizada esta instalación, podemos proceder a instalar el servidor propiamente dicho. A continuación, descargamos
la versión 1.3.8 de ProFTPD directamente desde su código fuente oficial mediante el siguiente comando:

```bash
wget sudo ftp://ftp.proftpd.org/distrib/source/proftpd-1.3.8.tar.gz && tar -xvzf proftpd-1.3.8.tar.gz && cd
proftpd-1.3.8
```
Con este comando descarga el ProFTPD, lo descomprime y entra al directorio creado.

Antes de compilar ProFTPD, se deben establecer ciertas opciones de ción para ajustar su instalación al
entorno deseado. Primero, indicamos que los archivos se instalarán con el usuario root y el grupo wheel, utilizando
el siguiente comando:

```bash
sudo install_user=root install_group=wheel ./configure
```

A continuación, mos las opciones del compilador, especificando que se utilizará gcc con las flags -O para
optimización y -g para incluir información de depuración:

```bash
./configure CC=gcc CFLAGS=’-O -g’
```

Seguidamente, definimos el prefijo de instalación para que los archivos se ubiquen bajo el directorio estándar /usr,
en lugar del predeterminado /usr/local, lo cual resulta útil en entornos como Docker:

```bash
./configure –prefix=/usr
```

Finalmente, especificamos las rutas para los archivos de ción y para los archivos variables del servidor, de
modo que ProFTPD respete la jerarquía típica de directorios en sistemas basados en Linux como Ubuntu:

```bash
./configure –sysconfdir=/etc –localstatedir=/var/proftpd
```

Una vez finalizada esta ción, se realiza una prueba manual para verificar el funcionamiento correcto del servidor. Para ello, primero instalamos archivos de prueba con el siguiente comando y vemos como es su naturaleza:

```bash
sh sample-tions/PFTEST.install
Sample test Succesfully in /tmp/PFTEST.
```

Esto genera una ción de ejemplo en el directorio /tmp/PFTEST. Luego, ejecutamos ProFTPD en modo
de prueba mediante:

```bash
./proftpd -n -d 5 -c /tmp/PFTEST/PFTEST.conf
```

Además, es necesario ajustar los permisos del archivo de contraseñas generado por el entorno de prueba para
garantizar su seguridad. Esto se hace mediante el siguiente comando:

```bash
chmod 600 /tmp/PFTEST/PFTEST.passwd
```

Dado que el protocolo FTP utiliza por defecto el puerto 21, es necesario modificar el archivo proftpd.conf para ajustar
la ción del servidor. En particular, en la directiva Port, se debe especificar el valor 21, que corresponde al
puerto que utilizará el servicio. Este archivo está alojado en:

```bash
cd /usr/local/etc/
```
Buscamos el archivo **proftpd.conf**

```bash
nano proftpd.conf
```
Modificamos el puerto a 21, ejemplo de la estructura del archivo:

```conf
ServerName          "Servidor FTP ProFTPD"
ServerType          standalone
DefaultServer       on

Port                21
Umask               022
MaxInstances        30

User                nobody
Group               nogroup

<Global>
    DefaultRoot     ~
    AllowOverwrite  on
</Global>

UseFtpUsers         off
RequireValidShell   off

# Log de actividad
SystemLog           /var/log/proftpd.log
```
> [!CAUTION]
> Con el comando **RequireValidShell off** sirve para que usuarios con shells falsos puedan iniciar sesión con FTP.

Con el servidor ya en funcionamiento, procedemos a añadir un usuario que se utilizará para iniciar sesión a
través del servicio FTP. Este usuario se crea sin acceso a la terminal del sistema, utilizando el siguiente comando:

```bash
useradd -m -s /bin/false user && echo ”user:pass”| chpasswd
```
> [!TIP]
> Modificar el campo user y pass según los datos de acceso que idee conveniente

Para finalizar, verificamos la dirección IP asignada al contenedor que ejecuta el servidor FTP. Esto es necesario para
que el cliente pueda establecer la conexión correctamente. Utilizamos el siguiente comando desde otra terminal:

```bash
docker inspect -f ’{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}’ servidor
```

### ⚙️ Instalación del cliente
Para el cliente, que utiliza lftp, se crea un nuevo contenedor llamado “cliente” usando la imagen de Ubuntu y
añadiéndolo a la red “redes_net”. Luego, se procede a instalar lftp dentro del contenedor con el siguiente comando:

> [!TIP]
> Desde otra terminal.

```bash
sudo docker run -it –name cliente –network redes_net ubuntu bash
```

Con este comando se instalan las dependencias necesarias para que `lftp` funcione correctamente. Entre ellas se incluyen:
Comando: 
```bash
apt install lftp -y
```

- `readline-devel`
- `zlib-devel`
- `gnutls-devel` **o** `openssl-devel` *(opcional, para soporte de TLS/SSL)*
- `expat-devel` *(opcional, para manejo de XML)*

> 📝 **Nota:** Estas dependencias suelen instalarse automáticamente en sistemas Debian/Ubuntu al ejecutar `apt install lftp`.

## 🔌 Comunicación Cliente-Servidor

Para empezar con la conexion del cliente con el servidor primero deberemos levantar la red local con el siguiente
comando:

```bash
sudo docker network inspect redes_net
```

> [!TIP]
> Desde otra terminal del HOST.

Resultado:
```json
[
  {
    "Name": "redes_net",
    "Id": "c9e4e71b0b40...",
    "Created": "2025-07-01T20:10:15.217Z",
    "Scope": "local",
    "Driver": "bridge",
    "EnableIPv6": false,
    "IPAM": {
      "Driver": "default",
      "Options": null,
      "Config": [
        {
          "Subnet": "172.18.0.0/16",
          "Gateway": "172.18.0.1"
        }
      ]
    },
    "Containers": {
      "a1b2c3d4e5f6": {
        "Name": "servidor",
        "EndpointID": "f0a1b...",
        "MacAddress": "02:42:ac:12:00:02",
        "IPv4Address": "172.18.0.2/16",
        "IPv6Address": ""
      },
      "f6e5d4c3b2a1": {
        "Name": "cliente",
        "EndpointID": "e1b2c...",
        "MacAddress": "02:42:ac:12:00:03",
        "IPv4Address": "172.18.0.3/16",
        "IPv6Address": ""
      }
    },
    "Options": {},
    "Labels": {}
  }
]
```

Volvemos a la terminal del servidor y combrobamos que se encuentre disponible para la conexión con el siguiente comando:

```bash
ps aux | grep proftpd # debera salir un resultado como porftpd: (accepting connections)
```
> [!IMPORTANT]
> Si no se encuetra aceptando conexión ingrese el siguiente comando:
> ```bash
> proftpd
> ``` 

Para lo siguiente, es importante tener en cuenta que se ha creado un usuario con sus respectivas credenciales
para establecer la conexión con el servidor. El usuario user, con la contraseña pass, está autorizado para conectarse mediante lftp. Desde la terminal del cliente, se debe iniciar la conexión con el servidor utilizando el siguiente comando:

```bash
lftp -u user,pass servidor
```
> [!CAUTION]
> Cambiar user y pass según qué usuario fue ingresado previamente.

Luego desde la terminal del cliente se realiza el siguiente comando para unirse como usuario desde lftp a el servidor con el
usuario y la contraseña correspondiente, con un ls o cd para verificar que se encuentra en el servidor listo para bajar o subir archivos.
> [!NOTE]
> Para hacer pruebas se recomienda instalar nano para en enviar archivos txt.
> ```bash
> apt-get install nano
> ```

## Comandos FTP importantes.
El entorno se encuentra totalmente do. Para lo siguiente es importante saber los comandos que se pueden utilizar en la consola dentro del servidor. Entre los comandos FTP más comunes y representativos se encuentran:
- `USER`: Envía el nombre de usuario para iniciar sesión.
- `PASS`: Transmite la contraseña del usuario.
- `PUT`: Sube un archivo individualmente.
- `GET`: Descarga un archivo individualmente desde el servidor.
- `CWD`: Cambia el directorio de trabajo en el servidor.
- `PWD`: Muestra el directorio actual en el servidor.
- `LIST`: Lista el contenido de un directorio.
- `RETR`: Descarga un archivo del servidor.
- `STOR` o `PUT`: Sube un archivo desde el cliente al servidor.
- `DELE`: Elimina un archivo en el servidor.
- `MGET`: Descarga múltiples archivos simultáneamente.
- `MPUT`: Sube múltiples archivos a la vez.
- `MKD`: Crea un nuevo directorio.
- `RMD`: Elimina un directorio.
- `REN`: Renombra archivos.
- `SYST`: Muestra información del sistema del servidor.
- `FEAT`: Lista las funciones disponibles en el servidor.
- `QUIT`: Finaliza la sesión FTP correctamente.


## 🕵️ Utilización de Scapy
El uso de Scapy sirve para analizar, interceptar, inyectar y modificar tráfico FTP entre un cliente lftp y un servidor proftpd, ambos ejecutándose en contenedores Docker sobre una red virtual personalizada.

tendremos que identificar las iP’s de los contenedores y la interfaz de red del equipo host, esto se debe a que Docker crea una interfaz de red virtual tipo bridge (por ejemplo, br-xxxxxx), la cual conecta internamente a todos los contenedores asociados a una red personalizada. Dicha interfaz actúa como un switch virtual, permitiendo al host observar todo el tráfico que circula entre los contenedores, incluso si estos no exponen puertos al exterior. En contraste, un contenedor individual solo puede ver su propio tráfico:

Podemos ver la interfaz personalizada con el siguiente comando:

```bash
ifconfig
```
> [!NOTE]
> Identificar y anotar la interfaz **br-XXXXXX**

### Configuración
Para la utilización de Scapy es necesario tener Python instalado en la maquina HOST. Vamos a preparar la máquina para la intercepción de tráfico, inyección y manipulación de paquetes. 

Para instalar Python y Scapy se utiliza el siguiente comando:

```bash
sudo apt update
sudo apt install -y python3 python3-pip tcpdump iputils-ping
sudo apt install -y python3-scapy
```
¿Por qué no será utilizado scapy en un contenedor individual?
Porque al tener Scapy en un contenedor Docker solo ve su propio eth0. En Docker, el aislamiento de red está a nivel de interfaz, no solo IP. Esto limita la visibilidad del tráfico.

> [!IMPORTANT]
> Es estrictamente necesario tener los contenedores iniciados. Para iniciar un contenedor se utiliza el siguiente comando:
> ```bash
> sudo docker start cliente
> sudo docker start servidor_v2
>```

Luego ingresamos a la terminal de los contenedores
> [!NOTE]
> Para ingresar a la terminal de un contenedor es:
> ```bash
> sudo docker exec -it nombre_contenedor /bin/bash
>```

### intercepción de tráfico con Scapy

Para Poder utilizar Scapy hay múltiples formas, una de ellas es crear un Script en python para identificar paquetes en concreto, por ejemplo una un paquete con etiqueta **USER** y **PASS**. La otra forma de utilizarlo es enviando comandos directamente por la interfaz de Scapy.

> [!IMPORTANT]
> Ingresar el campo correspondiente en iface="" con la interfaz obtenida con ifconfig.

> [!NOTE]
> Utilizar directamente desde la interfaz de Scapy es:
> ```bash
> scapy
> sniff(iface="br-XXXXXX", prn=lambda x: x.summary(), store=False)
>```

Vamos a utilizar un **script en Python** que filtra paquetes que contienen los comandos `USER` y `PASS`, permitiendo obtener las credenciales del cliente. Esto es posible debido a las **vulnerabilidades inherentes del protocolo FTP**, el cual transmite la información en **texto plano** sin ningún tipo de cifrado.

Creamos un nuevo archivo con nano:
```bash
nano script.py
```

Al estar en el editor de texto ingresamos el siguiente Script:

```python
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

sniff(iface="br-XXXXX", filter="tcp port 21", prn=print_pkt, store=False)
```
Ejemplo de ejecución:
```text
[+] Usuario detectada USER usuario
[+] Contraseña detectada PASS 1234
[FTP] 230 User usuario logged in
```
> [!TIP]
> Para poder ver este resultado en concreto, inicia sesión lftp desde el cliente con tu usuario y contraseña previamente añadida.

Campos importantes:
- `tcp port 21`: Permite visualizar paquetes TCP dirigidos desde el puerto 21 (FTP)
- `Raw.load.decode`: permite visualizar comandos en texto claro como USER y PASS.
- `br-XXXX`: Corresponde al puente Docker que conecta los contenedores.

### 💉 Inyecciones de Tráfico (Técnicas de Fuzzing)
Las pruebas fuzz o fuzzing son un método automatizado de pruebas de software que inyecta datos inválidos, malformados o inesperados en un sistema para revelar defectos y vulnerabilidades. Una herramienta de fuzzing inyecta estos datos en el sistema y luego monitorea excepciones como fallos o fugas de información.

Primera inyección: Intento de inicio de sesión con una cadena USER muy grande
```python
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="USER " + "A"*1000 + "\r\n"))
```
El servidor responde con RST cerrando abruptamente la conexión.
> [!CAUTION]
> Es posible que el servidor se caiga, si es así iniciar nuevamente con el comando **proftpd**

Inyección 2: comando inventado
```python
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="INVALIDCMD arg\r\n"))
```
El servidor responde con un RST cerrando abruptamente la conexión. **INVALIDCMD** simula un comando no válido del protocol, respuesta 500, mensaje "comando no reconocido"

### :trollface: Modificaciones del tráfico

Primera modificación: Solo SYN (handshake falso)
```python
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="S")) 
```
El servidor responde con un paquete SYN, ACK, indicando que estaba dispuesto a aceptar la conexión. Sin embargo, al no completar el handshake, el cliente respondió con un RST, terminando abruptamente la conexión.

Segunda modificación: Comando PASS fuera de contexto
```python
send(IP(dst="ip_servidor") / TCP(sport=RandShort(), dport=21, flags="PA", seq=1) / Raw(load="PASS xyz\r\n"))
```
Simula el envío de una contraseña (PASS xyz), sin haber hecho antes un USER o sin conexión válida, el servidor FTP lo interpreta como tráfico inválido o inesperado. Como resultado, el servidor responde con un RST

Tercera modificación: Comando PASS fuera de contexto
```python
send(IP(dst="ip_servidor")/TCP(sport=RandShort(), dport=21, flags="PA")/Raw(load="USER root\r\n"))
```
Muchos servidores FTP bloquean el login como root o bien este paquete es enviado sin una sesión válida ni handshake previo, por lo que el servidor responde con un paquete RST.

## 📕 Conclusión
En este proyecto se enseña a instalar el servicio de ProFTPD y LFTP en contenedores, y se explica cómo son las interacciones entre Cliente-Servidor. También se enseña cómo utilizar Scapy, demostrando que puede ser una herramienta poderosa para la inspección, inyección y modificación de tráfico en servicios de red como FTP. Se replicó un entorno controlado y reproducible para estudiar los efectos del tráfico manipulado. Se simula cómo el servidor FTP reacciona ante entradas malformadas, comandos inesperados y sesiones TCP anómalas.








