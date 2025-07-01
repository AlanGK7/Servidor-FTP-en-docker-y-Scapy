# Servidor-FTP-en-docker-y-Scapy

# Descripción
En conjunto, lftp y ProFTPD forman una pareja ideal para usuarios técnicos o administradores que buscan eficiencia, seguridad y automatización avanzada en sus sistemas. A diferencia de otras combinaciones, esta se enfoca
en un rendimiento sólido desde la terminal y una gestión completa del servidor, lo que la convierte en una opción
preferente en contextos profesionales o de alta demanda técnica.

Los softwares que utilizaremos para el cliente y el servidor serán lftp y
ProFTPD, respectivamente. A continuación, se ofrecerá una descripción más detallada de los comandos necesarios y del proceso de instalación para cada uno de ellos. Comenzaremos con la configuración del servidor, luego
abordaremos la del cliente y, finalmente, mostraremos cómo establecer la conexión entre ambos.

Como parte del estudio del protocolo FTP, se utilizó Scapy para interceptar, modificar e inyectar tráfico entre el cliente (lftp) y el servidor (ProFTPD), ambos ejecutándose como contenedores Docker.
El objetivo principal fue analizar el comportamiento del servicio FTP ante alteraciones en el protocolo.

> ❗️**Important:**  
> Este proyecto ha sido diseñado y probado exclusivamente en sistemas operativos **Linux**, particularmente distribuciones basadas en **Ubuntu/Debian**.  
> Algunos comandos, rutas y configuraciones pueden no funcionar correctamente en **Windows** o **macOS** sin adaptaciones adicionales.

## ⚙️ Instalción del servidor
### 1. Crear la red Docker
Para la instalación del servidor ProFTPD, se creó una red interna dentro del mismo dispositivo. Aunque este
paso es opcional y no estrictamente necesario, se optó por esta configuración con el fin de trabajar en un entorno
más controlado y aislado. 
> [!TIP]
> Es altamente recomendable exponer el puerto 21 sí no optas por una red Docker.

Para ello empezamos creando la red con el siguiente comando:
```bash
sudo docker network create redes_net
```
