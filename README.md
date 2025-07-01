# Servidor-FTP-en-docker-y-Scapy

# Descripción
En conjunto, **lftp** y **ProFTPD** forman una pareja ideal para usuarios técnicos o administradores que buscan eficiencia, seguridad y automatización avanzada en sus sistemas. A diferencia de otras combinaciones, esta se enfoca
en un rendimiento sólido desde la terminal y una gestión completa del servidor, lo que la convierte en una opción
preferente en contextos profesionales o de alta demanda técnica.

Los softwares que utilizaremos para el cliente y el servidor serán **lftp** y
**ProFTPD**, respectivamente. A continuación, se ofrecerá una descripción más detallada de los comandos necesarios y del proceso de instalación para cada uno de ellos. Comenzaremos con la configuración del servidor, luego
abordaremos la del cliente y, finalmente, mostraremos cómo establecer la conexión entre ambos.

Como parte del estudio del protocolo **FTP**, se utilizó **Scapy** para interceptar, modificar e inyectar tráfico entre el cliente (lftp) y el servidor (ProFTPD), ambos ejecutándose como contenedores **Docker**.
El objetivo principal fue analizar el comportamiento del servicio FTP ante alteraciones en el protocolo.

> ❗️**Important:**  
> Este proyecto ha sido diseñado y probado exclusivamente en sistemas operativos **Linux**, particularmente distribuciones basadas en **Ubuntu/Debian**.  
> Algunos comandos, rutas y configuraciones pueden no funcionar correctamente en **Windows** o **macOS** sin adaptaciones adicionales.

## ⚙️ Instalación del servidor

Para la instalación del servidor ProFTPD, se creó una red interna dentro del mismo dispositivo. Aunque este
paso es opcional y no estrictamente necesario, se optó por esta configuración con el fin de trabajar en un entorno
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
A continuación, procederemos con la configuración del servidor ProFTPD. Antes de iniciar su instalación, es
importante tener en cuenta ciertos requisitos previos, los cuales se pueden consultar en su documentación oficial.

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

Antes de compilar ProFTPD, se deben establecer ciertas opciones de configuración para ajustar su instalación al
entorno deseado. Primero, indicamos que los archivos se instalarán con el usuario root y el grupo wheel, utilizando
el siguiente comando:

```bash
sudo install_user=root install_group=wheel ./configure
```

A continuación, configuramos las opciones del compilador, especificando que se utilizará gcc con las flags -O para
optimización y -g para incluir información de depuración:

```bash
./configure CC=gcc CFLAGS=’-O -g’
```

Seguidamente, definimos el prefijo de instalación para que los archivos se ubiquen bajo el directorio estándar /usr,
en lugar del predeterminado /usr/local, lo cual resulta útil en entornos como Docker:

```bash
./configure –prefix=/usr
```

Finalmente, especificamos las rutas para los archivos de configuración y para los archivos variables del servidor, de
modo que ProFTPD respete la jerarquía típica de directorios en sistemas basados en Linux como Ubuntu:

```bash
./configure –sysconfdir=/etc –localstatedir=/var/proftpd
```

Una vez finalizada esta configuración, se realiza una prueba manual para verificar el funcionamiento correcto del servidor. Para ello, primero instalamos archivos de prueba con el siguiente comando y vemos como es su naturaleza:

```bash
sh sample-configurations/PFTEST.install
Sample test Succesfully in /tmp/PFTEST.
```

Esto genera una configuración de ejemplo en el directorio /tmp/PFTEST. Luego, ejecutamos ProFTPD en modo
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
la configuración del servidor. En particular, en la directiva Port, se debe especificar el valor 21, que corresponde al
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

## ⚙️ Instalación del cliente
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

## Comunicación Cliente-Servidor

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
> Si no se encuetra aceptando conexion ingrese el siguiente comando:
> ```bash
> proftpd
> ``` 



