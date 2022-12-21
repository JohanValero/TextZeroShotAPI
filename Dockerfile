# Imagen oficial de Docker que incluye Python 3.10.5 y un conjunto reducido de dependencias
# necesarias para ejecutar aplicaciones Python.
# La imagen es "slim" (o "delgada") en el sentido de que incluye solo lo esencial para ejecutar
# aplicaciones Python y no incluye paquetes adicionales o librerías que no son necesarios para
# la mayoría de las aplicaciones.
# La imagen está basada en la distribución de Linux "Debian Bullseye", que es la distribución en desarrollo de Debian.
FROM python:3.10.5-slim-bullseye

# Crea un directorio llamado "wd" en el sistema de archivos del contenedor.
RUN mkdir wd

# El comando establece el directorio "/wd" como el directorio de trabajo del contenedor.
WORKDIR /wd

# El comando copia el archivo "requirements.txt" del contexto de construcción
# al directorio de trabajo del contenedor.
COPY requirements.txt .

# El comando instala todas las dependencias necesarias especificadas en el
# archivo "requirements.txt" utilizando pip.
RUN pip install -r requirements.txt

# El comando copia todos los archivos del contexto de construcción al directorio
# de trabajo del contenedor.
COPY ./ ./

# Se ejecuta durante la construcción del contenedor para dejar en las capas de caché
# el modelo predictivo y permitir una rápida re-utilización en producción.
RUN python3 setup_cache.py

# Establece el comando predeterminado para el contenedor. Este comando iniciará un
# servidor web Gunicorn con un solo trabajador y ocho hilos, escuchando en el puerto
# especificado por la variable de entorno $PORT y ejecutando la aplicación principal en el módulo "main".
CMD exec gunicorn --workers=1 --threads=8 -b :$PORT main:app