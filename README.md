# TextZeroShotAPI
Una aplicación de clasificación de texto en Python que utiliza la librería transformers y un modelo de lenguaje previamente entrenado llamado "Recognai/bert-base-spanish-wwm-cased-xnli" para clasificar reseñas como positivas o negativas. Que se despliega en despliegue continuo en Google Cloud Plataform (GCP).

## Python
Para instalar Python en Windows, primero debes descargar la versión adecuada de la página oficial de Python (https://www.python.org/downloads/). Asegúrate de elegir la versión de acuerdo a tu sistema operativo y las necesidades de tu proyecto. Una vez descargado, ejecuta el instalador y sigue las instrucciones en pantalla.
> Nota: La instalación en sistemas unix tiene pasos distintos.

Una vez instalado Python, puedes crear y activar un entorno virtual usando el comando ```py -m venv env```. Este comando creará una carpeta llamada "env" que contendrá tu entorno virtual. Para activarlo, debes ejecutar el comando ```env\Scripts\activate.bat``` desde la línea de comandos.
> Nota: Si estas en un sistema unix, debes instalar manualmente el gestor de entornos virtuales.

> Nota: La activación de un entorno virtual se ejecuta con el comando ```source env\bin\activate```.

Es una buena práctica usar entornos virtuales porque te permiten tener diferentes versiones y paquetes de Python instalados en tu máquina sin interferir entre sí. Además, te ayudan a mantener el proyecto aislado de otras dependencias del sistema.

Para instalar el archivo requirements.txt, debes asegurarte de que tu entorno virtual esté activado y ejecutar el comando ```pip install -r requirements.txt```. Este comando instalará todos los paquetes y dependencias especificadas en el archivo, solo en el entorno virtual en la terminal.

Para ejecutar la aplicación main.py, asegúrate de estar en la carpeta donde se encuentra el archivo, y tener el entorno virtual con todas las dependencias, y ejecuta el comando ```py main.py```. Esto iniciará la ejecución de la aplicación.

> Nota: Si estás en un sistema operativo unix debes ejecutar el comando ```python3 main.py```.

Al abrir se puede consultar el API en:
+ Respuesta positiva: http://127.0.0.1:8000/?text=Esta%20es%20una%20empresa%20grandiosa
+ Respuesta negativa: http://127.0.0.1:8000/?text=Es%20mejor%20movistar

## ¿Qué es Docker?
Docker es una plataforma de contenedores que permite a los desarrolladores empaquetar y ejecutar aplicaciones en cualquier entorno de forma segura y predecible. Los contenedores son una forma de virtualización ligera que permite a las aplicaciones correr en un entorno aislado sin tener que instalar todo el software necesario en la máquina anfitriona.

Docker es importante en la nube porque permite a los desarrolladores empaquetar y desplegar aplicaciones de manera consistente en cualquier entorno, incluyendo la nube. Esto facilita el trabajo en equipo y permite a los equipos trabajar de manera más eficiente y rápida.

En serverless, Docker es importante porque permite a los desarrolladores crear aplicaciones que se pueden ejecutar en cualquier entorno sin tener que preocuparse por la infraestructura subyacente. Esto permite a los desarrolladores centrarse en el código de la aplicación en lugar de en la configuración y el mantenimiento del servidor. Además, Docker permite a los desarrolladores crear contenedores que se pueden ejecutar en cualquier plataforma de serverless, lo que facilita el despliegue de aplicaciones en diferentes entornos.

Para instalar Docker en Windows, debes seguir los siguientes pasos:

1. Descarga Docker Desktop para Windows desde la página oficial de Docker (https://www.docker.com/products/docker-desktop).

2. Ejecuta el instalador y sigue las instrucciones en pantalla. Asegúrate de permitir que Docker tenga acceso a tu red y a tu disco duro durante la instalación.

3. Una vez instalado, inicia Docker Desktop y espera a que se complete el proceso de inicio.

4. Para configurar WSL2 (Windows Subsystem for Linux), debes seguir los siguientes pasos:

5. Abre una ventana del símbolo del sistema con privilegios de administrador y ejecuta el comando "dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart".

6. Ejecuta el comando "dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart".

7. Abre la aplicación Configuración de Windows y selecciona "Aplicaciones".

8. Selecciona "Programas y características" en la columna de la izquierda y luego haz clic en "Activar o desactivar características de Windows" en el panel de la derecha.

9. Selecciona "Windows Subsystem for Linux" y haz clic en "Aceptar".

10. Reinicia tu ordenador cuando se te solicite.

11. Abre la tienda de Microsoft y busca "Linux" para encontrar distribuciones de Linux disponibles para instalar. Selecciona una distribución y sigue las instrucciones en pantalla para completar la instalación.

12. Una vez instalado y configurado WSL2, debes ejecutar el comando "wsl --set-default-version 2" para establecer WSL2 como la versión predeterminada de WSL. Luego, puedes iniciar la distribución de Linux que hayas instalado y comenzar a trabajar con Docker desde el terminal de Linux.

### Crear imagen y contenedor Docker.

Para construir una imagen Docker a partir de un archivo Dockerfile y un conjunto de opciones adicionales.

Ejecutar el siguiente comando:
```
docker build -e PORT=8000 -p 8000:8000 -t app_clasificadora .
```
1. La opción "-e PORT=8000" establece una variable de entorno con el nombre "PORT" y el valor "8000" durante la construcción de la imagen. Esto permite utilizar el valor de la variable de entorno "PORT" en el Dockerfile para determinar en qué puerto escuchar la aplicación.

2. La opción "-p 8000:8000" establece una regla de mapeo de puertos que expone el puerto 8000 del contenedor en el puerto 8000 del host. Esto permite acceder a la aplicación en el contenedor a través del puerto 8000 del host.

3. La opción "-t app_clasificadora" le da un nombre a la imagen que se está construyendo. En este caso, la imagen se llamará "app_clasificadora".
```
docker run --name clasificador_texto app_clasificadora
```
Este código ejecuta un contenedor de Docker con el nombre "clasificador_texto" a partir de una imagen llamada "app_clasificadora". Al ejecutar este comando, se creará un contenedor nuevo y se iniciará a partir de la imagen especificada.

Al crear el contenedor se puede consultar el API en:
+ Respuesta positiva: http://127.0.0.1:8000/?text=Esta%20es%20una%20empresa%20grandiosa
+ Respuesta negativa: http://127.0.0.1:8000/?text=Es%20mejor%20movistar

## ¿Qué es la nube?
La nube es un término utilizado para describir la prestación de servicios de informática, como almacenamiento de datos, procesamiento de datos y aplicaciones a través de Internet en lugar de utilizar recursos informáticos locales. En lugar de tener que adquirir y mantener la infraestructura informática necesaria de forma local, las empresas pueden utilizar servicios de la nube proporcionados por proveedores de la nube como Amazon Web Services, Microsoft Azure o Google Cloud Platform. Esto permite a las empresas utilizar la infraestructura informática de la nube de forma flexible y ajustar su uso según sea necesario.

Desplegar aplicaciones en la nube tiene varias ventajas:
+ Escalabilidad: Es fácil aumentar o disminuir el tamaño de la infraestructura en la nube para satisfacer los cambios en la demanda de la aplicación. Esto permite a las empresas adaptarse rápidamente a los cambios en la demanda sin tener que adquirir y configurar hardware adicional de forma manual.
+ Gestión de la infraestructura: Al utilizar una plataforma en la nube, se delega la gestión de la infraestructura a la proveedora de la nube. Esto permite a las empresas enfocarse en el desarrollo y el mantenimiento de su aplicación en lugar de preocuparse por la gestión de la infraestructura subyacente.
+ Costo: Desplegar aplicaciones en la nube puede ser más económico que adquirir y mantener la infraestructura necesaria de forma local. Muchas plataformas en la nube ofrecen tarifas basadas en el uso, lo que permite a las empresas pagar solo por lo que utilizan.
+ Disponibilidad: Las plataformas en la nube suelen tener altos niveles de disponibilidad y redundancia, lo que reduce el riesgo de interrupciones en el servicio de la aplicación.
+ Agilidad: Desplegar aplicaciones en la nube permite a las empresas implementar y probar nuevas funcionalidades de forma más rápida y sencilla.
+ Flexibilidad: Las plataformas en la nube ofrecen una gran variedad de opciones de configuración y personalización, lo que permite a las empresas adaptar su infraestructura a sus necesidades específicas.

## ¿Qué es CI/CD?
CI/CD (Continuous Integration / Continuous Deployment) es una práctica de desarrollo de software que se enfoca en automatizar y optimizar el proceso de integración y despliegue de código en entornos de producción.

La integración continua (CI, por sus siglas en inglés) se refiere al proceso de integrar y probar el código de manera constante y automatizada. Cada vez que un desarrollador realiza un cambio en el código, este cambio se integra con el código base y se ejecutan pruebas automatizadas para verificar que no haya ningún error. De esta manera, se pueden detectar problemas de forma temprana y solucionarlos antes de que el código se despliegue a entornos de producción.

Por otro lado, el despliegue continuo (CD, por sus siglas en inglés) se refiere al proceso de desplegar el código de manera automatizada y frecuente a entornos de producción. En lugar de esperar a tener una versión completamente terminada del software para desplegarla, el proceso de CD permite desplegar cambios incrementales de forma constante. De esta manera, se pueden implementar mejoras y nuevas funcionalidades de forma más rápida y segura.

En resumen, CI/CD es una práctica que busca automatizar y optimizar el proceso de integración y despliegue de código, lo que permite mejorar la calidad del software y reducir el tiempo de entrega de nuevas funcionalidades.

## Desplegar de forma continua en Google Cloud Plataform (GCP).

