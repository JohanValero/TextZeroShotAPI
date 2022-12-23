# Objetivo del repositorio
El objetivo en este repositorio es compartir el conocimiento necesario para enseñar la publicación de una API Restfull de un modelo predictivo en la nube de forma serverless, con el fin de que todos los miembros del equipo puedan tener acceso a las herramientas y conocimientos fundamentales para desarrollar proyectos en la nube. Esto no solo nos permitirá abordar los desafíos actuales con confianza y eficiencia, sino que también nos preparará para enfrentar nuevos retos en el futuro.

A través de este documento, exploraremos diferentes aspectos de Python y Docker, y aprenderemos sobre Git y CI/CD. También exploraremos el concepto de la nube y cómo implementar nuestro proyecto en diferentes plataformas de nube, como Google Cloud Platform (GCP), Amazon Web Services (AWS), Microsoft Azure y Oracle Cloud Infrastructure (OCI). Además, exploraremos cómo entrenar un modelo predictivo y visualizar datos.

Compartir nuestro conocimiento y trabajar juntos como un equipo es clave para nuestro éxito. Al compartir nuestro conocimiento y aprender unos de otros, podemos mejorar nuestras habilidades y enfrentar cualquier desafío que se nos presente. Esperamos que este repositorio sea una herramienta valiosa para todos nosotros mientras trabajamos juntos para aprender y crecer en nuestras habilidades de desarrollo en la nube.

# TextZeroShotAPI
Una aplicación de clasificación de texto en Python que utiliza la librería transformers y un modelo de lenguaje previamente entrenado llamado "Recognai/bert-base-spanish-wwm-cased-xnli" para clasificar reseñas como positivas o negativas. Que se despliega en despliegue continuo en Google Cloud Plataform (GCP).

Se ha generado un pequeño Dataset (conjunto de datos) pequeño de solo 1000 reseñas de la aplicación de YouTube en Play Store (https://play.google.com/store/apps/details?id=com.google.android.youtube&hl=es) y verificar la cálidad de las reseñas comparado con la calificación de estrellas dada por el usuario. Que necesitará un pre-procesamiento de remover el texto de la calificación y calificar si la reseña es positiva o negativa.

+ Obtención del Dataset:
  + Se ingresó en la página de Play Store de YouTube y se ha extraido un subconjunto de reseñas.
  + El código de extracción es:
    + ```javascript
        divs = document.getElementsByClassName("RHo1pe")
        let result = []
        for(let i = 0; i < divs.length; i++){
          let a = divs[i].children[0].children[1].children[0].ariaLabel
          let b = divs[i].children[1].textContent
          let c = divs[i].children[0].children[1].children[1].textContent
          result.push({"valoración": a.slice(), "comentario": b.slice(), "fecha": c.slice()})
        }
        JSON.stringify(result)
  + El JSON generado es (solo 2 registros):
    + ```json
      [ {
          "valoración":"Valoración: 4 estrellas de cinco",
          "comentario":"Buena app... (Sin embargo, esta app últimamente ha mostrado anuncios inapropiados e inescrupulosos, especialmente de apps ilegales, lo peor ocurre antes, durante y después del vídeo donde los ponen a propósito con el fin de no dejar ver el vídeo al que utiliza YouTube, era mejor tiempo atrás donde lo ponían sin necesidad de interrumpir el vídeo, abajito junto a la barra de reproducción del vídeo. Deben reparar eso y regular el tema de esos anuncios ilegítimos en la app)",
          "fecha":"14 de diciembre de 2022"
        }, {
          "valoración":"Valoración: 4 estrellas de cinco",
          "comentario":"La verdad la App es buena como todas, lo de los anuncios lo entiendo por que así es como mantienen la aplicación a flote promocionando marcas etc, pero las últimas actualizaciones no ayudan en nada en vez de mejorar agregan más problemas, por ejemplo las dos flechas que aparecen al reproducir un video y no deja ver por completo y no se pueden quitar por favor solucionen eso y otras cosas si... Gracias",
          "fecha":"4 de octubre de 2022"
        },
      ]

> Nota: Adicionalmente se realiza un ligero post-processing para cambiar \\\\" por \\" y el atributo JSON "valoración" por "valoracion". Para corregir caracteres especiales y remover acentos.

## Python
Para instalar Python en Windows, primero debes descargar la versión adecuada de la página oficial de Python (https://www.python.org/downloads/). Asegúrate de elegir la versión de acuerdo a tu sistema operativo y las necesidades de tu proyecto. Una vez descargado, ejecuta el instalador y sigue las instrucciones en pantalla.
> Nota: La instalación en sistemas unix tiene pasos distintos.

Una vez instalado Python, puedes crear y activar un entorno virtual usando el comando:
```bash
py -m venv env
```
Este comando creará una carpeta llamada "env" que contendrá tu entorno virtual. Para activarlo, debes ejecutar desde la línea de comandos el comando:
```bash
env\Scripts\activate.bat
```
> Nota: Si estas en un sistema unix, debes instalar manualmente el gestor de entornos virtuales.

> Nota: La activación de un entorno virtual se ejecuta con el comando: ```source env\bin\activate```.

Es una buena práctica usar entornos virtuales porque te permiten tener diferentes versiones y paquetes de Python instalados en tu máquina sin interferir entre sí. Además, te ayudan a mantener el proyecto aislado de otras dependencias del sistema.

Para instalar el archivo requirements.txt, debes asegurarte de que tu entorno virtual esté activado y ejecutar el comando:
```bash
pip install -r requirements.txt
```
Este comando instalará todos los paquetes y dependencias especificadas en el archivo, solo en el entorno virtual en la terminal.

Para ejecutar la aplicación main.py, asegúrate de estar en la carpeta donde se encuentra el archivo, y tener el entorno virtual con todas las dependencias, y ejecuta el comando:
```bash
py main.py
```
Esto iniciará la ejecución de la aplicación.

> Nota: Si estás en un sistema operativo unix debes ejecutar el comando: ```python3 main.py```

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

5. Abre una ventana del símbolo del sistema con privilegios de administrador y ejecuta el comando:
```bash
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

6. Ejecuta el comando:
```bash
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

7. Abre la aplicación Configuración de Windows y selecciona "Aplicaciones".

8. Selecciona "Programas y características" en la columna de la izquierda y luego haz clic en "Activar o desactivar características de Windows" en el panel de la derecha.

9. Selecciona "Windows Subsystem for Linux" y haz clic en "Aceptar".

10. Reinicia tu ordenador cuando se te solicite.

11. Abre la tienda de Microsoft y busca "Linux" para encontrar distribuciones de Linux disponibles para instalar. Selecciona una distribución y sigue las instrucciones en pantalla para completar la instalación.

12. Una vez instalado y configurado WSL2, debes ejecutar el comando: ```wsl --set-default-version 2```.
Para establecer WSL2 como la versión predeterminada de WSL. Luego, puedes iniciar la distribución de Linux que hayas instalado y comenzar a trabajar con Docker desde el terminal de Linux.

### Crear imagen y contenedor Docker.

Para construir una imagen Docker a partir de un archivo Dockerfile y un conjunto de opciones adicionales.

Ejecutar el siguiente comando para compilar la imagen docker:
```bash
docker build -t app_clasificadora .
```
Ejecuta el siguiente comanda para iniciar un contenedor docker.
```bash
docker run --name clasificador_texto -e PORT=8000 -p 8000:8000 app_clasificadora
```
Este código ejecuta un contenedor de Docker con el nombre "clasificador_texto" a partir de una imagen llamada "app_clasificadora". Al ejecutar este comando, se creará un contenedor nuevo y se iniciará a partir de la imagen especificada.

1. La opción "--name clasificador_texto" nombra el contenedor para su facil reconocimiento.

2. La opción "-e PORT=8000" establece una variable de entorno con el nombre "PORT" y el valor "8000" durante la construcción de la imagen. Esto permite utilizar el valor de la variable de entorno "PORT" en el Dockerfile para determinar en qué puerto escuchar la aplicación.

3. La opción "-p 8000:8000" establece una regla de mapeo de puertos que expone el puerto 8000 del contenedor en el puerto 8000 del host. Esto permite acceder a la aplicación en el contenedor a través del puerto 8000 del host.

4. La opción "-t app_clasificadora" le da un nombre a la imagen que se está construyendo. En este caso, la imagen se llamará "app_clasificadora".

Al crear el contenedor se puede consultar el API en:
+ Respuesta positiva: http://127.0.0.1:8000/?text=Esta%20es%20una%20empresa%20grandiosa
+ Respuesta negativa: http://127.0.0.1:8000/?text=Es%20mejor%20movistar

## ¿Qué es repositorio de código?
Un repositorio de código es un lugar donde se almacena y controla el código de un proyecto de software. Existen diferentes tipos de repositorios de código, como los repositorios de código fuente, que almacenan el código fuente de un proyecto, y los repositorios de binarios, que almacenan los archivos ejecutables o compilados de un proyecto.

Los repositorios de código son útiles porque permiten controlar el cambio de código de forma centralizada y mantener un historial de las versiones del código. Esto hace que sea más fácil colaborar con otros desarrolladores, revertir cambios y resolver problemas. Además, los repositorios de código suelen incluir funcionalidades para realizar seguimiento de problemas, realizar seguimiento de tareas y hacer seguimiento de la actividad del proyecto.

En resumen, los repositorios de código son herramientas esenciales para el desarrollo de software y ofrecen una serie de beneficios, como:
+ Facilitan la colaboración con otros desarrolladores.
+ Permiten controlar el cambio de código de forma centralizada.
+ Mantienen un historial de las versiones del código.
+ Incluyen funcionalidades para realizar seguimiento de problemas y tareas.
+ Ayudan a hacer seguimiento de la actividad del proyecto.

Tu puedes clonar este repositorio usando el comando:
```bash
git clone https://github.com/JohanValero/TextZeroShotAPI.git
```
> Nota: Se asume que se ha instalado git en el equipo.

Para crear su propio repositorio git debes ejecutar los siguientes comandos, después de creado un proyecto Git:

```bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/{GitUser}/{ProjectName}.git
git push -u origin main
```
En un proyecto de software que utiliza Git, es común utilizar varias ramas para organizar el código y el desarrollo. Algunas ramas que suelen utilizarse son:
+ Producción: es la rama principal del proyecto y contiene el código que se encuentra en producción. Es importante mantener esta rama estable y libre de errores, por lo que solo se deben realizar cambios cuidadosamente probados y validados.
+ Calidad: es una rama donde se realizan pruebas y validaciones antes de integrar el código a la rama de producción. Esta rama se utiliza para asegurar que el código cumpla con los estándares de calidad y no tenga errores.
+ Desarrollo: es una rama donde se integran y proban los cambios realizados por los desarrolladores. Esta rama se utiliza como un lugar de integración para validar que los cambios realizados por diferentes desarrolladores funcionen correctamente juntos.
+ Ramas de desarrollo por desarrollador o historia de usuario: son ramas creadas por los desarrolladores para trabajar en una historia de usuario o una tarea específica. Una vez que el trabajo está completo, estas ramas se integran a la rama de desarrollo para ser probadas y validadas.

En resumen, esta estructura de ramas permite separar el código en diferentes etapas de desarrollo y validación, lo que facilita la colaboración entre los desarrolladores y mejora la calidad del código.

Este proyecto tiene la siguiente estructura de ramas(branchs):
+ main: rama de producción.
  + qa: rama de calidad.
    + development: rama de desarrollo.
      + dev-x: rama personal de desarrollo.

## ¿Qué es CI/CD?
CI/CD (Continuous Integration / Continuous Deployment) es una práctica de desarrollo de software que se enfoca en automatizar y optimizar el proceso de integración y despliegue de código en entornos de producción.

La integración continua (CI, por sus siglas en inglés) se refiere al proceso de integrar y probar el código de manera constante y automatizada. Cada vez que un desarrollador realiza un cambio en el código, este cambio se integra con el código base y se ejecutan pruebas automatizadas para verificar que no haya ningún error. De esta manera, se pueden detectar problemas de forma temprana y solucionarlos antes de que el código se despliegue a entornos de producción.

Por otro lado, el despliegue continuo (CD, por sus siglas en inglés) se refiere al proceso de desplegar el código de manera automatizada y frecuente a entornos de producción. En lugar de esperar a tener una versión completamente terminada del software para desplegarla, el proceso de CD permite desplegar cambios incrementales de forma constante. De esta manera, se pueden implementar mejoras y nuevas funcionalidades de forma más rápida y segura.

En resumen, CI/CD es una práctica que busca automatizar y optimizar el proceso de integración y despliegue de código, lo que permite mejorar la calidad del software y reducir el tiempo de entrega de nuevas funcionalidades.

## ¿Qué es la nube?
La nube es un término utilizado para describir la prestación de servicios de informática, como almacenamiento de datos, procesamiento de datos y aplicaciones a través de Internet en lugar de utilizar recursos informáticos locales. En lugar de tener que adquirir y mantener la infraestructura informática necesaria de forma local, las empresas pueden utilizar servicios de la nube proporcionados por proveedores de la nube como Amazon Web Services, Microsoft Azure o Google Cloud Platform. Esto permite a las empresas utilizar la infraestructura informática de la nube de forma flexible y ajustar su uso según sea necesario.

Desplegar aplicaciones en la nube tiene varias ventajas:
+ Escalabilidad: Es fácil aumentar o disminuir el tamaño de la infraestructura en la nube para satisfacer los cambios en la demanda de la aplicación. Esto permite a las empresas adaptarse rápidamente a los cambios en la demanda sin tener que adquirir y configurar hardware adicional de forma manual.
+ Gestión de la infraestructura: Al utilizar una plataforma en la nube, se delega la gestión de la infraestructura a la proveedora de la nube. Esto permite a las empresas enfocarse en el desarrollo y el mantenimiento de su aplicación en lugar de preocuparse por la gestión de la infraestructura subyacente.
+ Costo: Desplegar aplicaciones en la nube puede ser más económico que adquirir y mantener la infraestructura necesaria de forma local. Muchas plataformas en la nube ofrecen tarifas basadas en el uso, lo que permite a las empresas pagar solo por lo que utilizan.
+ Disponibilidad: Las plataformas en la nube suelen tener altos niveles de disponibilidad y redundancia, lo que reduce el riesgo de interrupciones en el servicio de la aplicación.
+ Agilidad: Desplegar aplicaciones en la nube permite a las empresas implementar y probar nuevas funcionalidades de forma más rápida y sencilla.
+ Flexibilidad: Las plataformas en la nube ofrecen una gran variedad de opciones de configuración y personalización, lo que permite a las empresas adaptar su infraestructura a sus necesidades específicas.

## Despliegue continuo en Google Cloud Plataform (GCP).

+ Se crea una cuenta en la nube de GCP.
  + Esta nube da la ventaja de ofrecer una capa gratuita diaria y/o mensual.
  + Para más información de como gestionar proyectos: https://cloud.google.com/resource-manager/docs/creating-managing-projects
+ Activar el API de `Cloud Build`:
  + La capa gratuita de GCP solo inicia su cobro después de 120 minutos de despliegue al día.
  + El cobro es de USD 0.003 por mínuto / 4.32 USD por día (después de los 120 minutos de la capa gratuita).
  + Para más información leer: https://cloud.google.com/build/docs
+ Activar el API de `Artifac registry`:
  + La capa gratuita de GCP solo inicia su cobro a partir de 0.5 Gigabyte (500 MB) al mes con un valor de 0.1 USD cada 500 MB.
    + Una imagen Docker de 2.5 GB tiene un precio de 1 USD/mes.
  + Para más información leer: https://cloud.google.com/artifact-registry/docs
+ Activar el API de `Cloud Run`:
  + La capa gratuita ofrece:
    + Las primeras 5 horas de procesamiento.
    + Las primeras 360.000 GiB de memoria ram por segundo.
      + Si tu aplicación usa 500 MB de ram, entonces tienes 60 horas de memoria gratuitos.
    + 2 millones de solicitudes gratutitas al mes.
  + Para más información leer: https://cloud.google.com/run/docs

### Crear un despliegue continuo en Cloud Build:
+ Se ingresa en `Artifact Registry`:
  + Se crean dos repositorios:
    + Se crea el repositorio Docker "app-clasificador-qa".
    + Se crea el repositorio Docker "app-clasificador-prod".
    + Se ingresa en Cloud Shell (CLI de gcloud) y se ejecuta el comando: `gcloud auth configure-docker us-central1-docker.pkg.dev`. Esto es necesario para configurar el auxiliar de credenciales para el dominio de Artifact Registry asociado a la ubicación de este repositorio.
      + Si no se realiza este paso, entonces no se publicarán las imagenes docker.
+ Se ingresa en `Cloud Build`:
  + Se ingresa en `Configuración` y se habilita las opciones de:
    + Cloud run, Administrador de cloud run.
    + Cuentas de servicio, Usuario de cuenta servicio.
  + Se ingresa en `Activadores/Triggers` y se escoge una región.
  + Se crea un `activador` (disparador/trigger) nombrado "activador-qa-pull-request".
    + Se recomienda activar "Solicitar aprobación antes de que se ejecute la compilación" si no se busca una automatización total.
    + Se asigna el evento "Solicitud de extracción" para ejecutar durante el "pull request".
    + Se asigna en "Rama base" el valor "^qa$", para activar la compilación automática durante los Pull request de la rama.
    + Se asgina "Ubicación del archivo de configuración de Cloud Build" el valor de `gcp-cloudbuild-qa.yaml`.
    + Se debe conectar el clodbuild al repositorio usando el GitAPI.
    + Al enviar un Pull request de la rama "Development" a la rama "qa" se generará el deploy automático:
    + Imagen de un pull request en proceso de pruebas.
    ![](https://raw.githubusercontent.com/JohanValero/TextZeroShotAPI/development/resources/Pull%20request%20pendiente%20dev2qa.PNG "Pull request en despliegue automático.")
    + Imagen de una aprobación de una compilación en Cloud Build.
    ![](https://raw.githubusercontent.com/JohanValero/TextZeroShotAPI/development/resources/Pull%20request%20aprobaci%C3%B3n%20pendiente%20dev2qa.PNG "Aprobación en Cloud Build.")
  + Se crea un `activador` (disparador/trigger) nombrado  "activador-qa-branch":
    + Se recomienda activar "Solicitar aprobación antes de que se ejecute la compilación" si no se busca una automatización total.
    + Se asigna el evento "Enviar una rama" para ejecutar durante el "push" a la rama de "qa".
    + Se asgina "Ubicación del archivo de configuración de Cloud Build" el valor de `gcp-cloudbuild-qa-deploy.yaml`.
    + Se debe conectar el clodbuild al repositorio usando el GitAPI.
    + Al finalizar el proceso se generará un servicio QA donde probar el API generado.
  + Se crea un `activador` (disparador/trigger) nombrado  "activador-prod-branch":
    + Se recomienda activar "Solicitar aprobación antes de que se ejecute la compilación" si no se busca una automatización total.
    + Se asigna el evento "Enviar una rama" para ejecutar durante el "push" a la rama de "main" (produción).
    + Se asgina "Ubicación del archivo de configuración de Cloud Build" el valor de `gcp-cloudbuild-prod-deploy.yaml`.
    + Se debe conectar el clodbuild al repositorio usando el GitAPI.
    + Al finalizar el proceso se generará un servicio en producción donde probar el API generado.
+ Se ingresa en `Cloud Storage`:
  + La capa gratuita de GCP no contempla Cloud Storage:
    + Los precios (almacenamiento estandar) son de 0,02 USD por 1 GB/mes, por lo tanto permite 50 GB por 1 USD al mes. 
  + Crear un nuevo bucket nombrado `bucket-analitica-qa`.
    + Crear el foder `data_json`:
      + Subir el archivo `comentarios-youtube.json` al bucket.
    + Crear el folder `data_csv`.
    + Agregar al bucket los permisos:
      + Al usuario "allUsers" adicionarle el permiso "allAuthenticatedUsers", esto permite que cualquier persona en internet pueda ver los archivos del Bucket.
    > Nota: Si desea conectar el Bucket en local debe generar una clave para la cuenta de servicio y setear la variable de entorno: GOOGLE_APPLICATION_CREDENTIALS=./path_to_the_key.json

> Nota: Se recomienda usar la misma región para todos los despliegues en nube. Este tutorial por default fue hecho en "us-central1", si se cambia se deberá modificar los archivos `gcp-cloudbuild-qa.yaml`, `gcp-cloudbuild-prod.yaml` y `gcp-cloudbuild-prod-deploy.yaml`.

## Visualización de datos

La visualización de datos es una técnica utilizada para representar gráficamente los datos de manera que resulten fáciles de entender e interpretar. Esta técnica se ha vuelto cada vez más importante en la industria debido a la creciente cantidad de datos que generamos y al incremento de la necesidad de utilizar estos datos para tomar decisiones informadas.

A continuación, se presentan algunas de las ventajas que ofrece la visualización de datos para las empresas:
- Permite comprender los datos de manera rápida y sencilla: La visualización de datos permite representar gráficamente los datos de manera que sean fáciles de entender e interpretar, incluso para aquellas personas que no tienen un conocimiento profundo de la materia. Esto hace que sea más sencillo comprender los datos y extraer conclusiones de ellos.
- Facilita la toma de decisiones: Al permitir comprender los datos de manera rápida y sencilla, la visualización de datos facilita la toma de decisiones basadas en datos. Esto puede ayudar a las empresas a tomar decisiones más informadas y a maximizar sus beneficios.
- Ayuda a detectar patrones y tendencias: La visualización de datos permite detectar patrones y tendencias en los datos de manera rápida y sencilla. Esto puede ayudar a las empresas a anticipar el comportamiento del mercado y a tomar decisiones de inversión y marketing más efectivas.
- Facilita la comunicación de resultados: La visualización de datos permite representar gráficamente los resultados de manera atractiva y fácil de entender. Esto hace que sea más sencillo comunicar los resultados a otros, ya sean clientes, inversores o compañeros de trabajo.

En resumen, la visualización de datos es una técnica fundamental en la industria debido a su capacidad para hacer más sencillo el procesamiento y comprensión de los datos, facilitar la toma de decisiones y detectar patrones y tendencias. Por esta razón, cada vez más empresas están invirtiendo en herramientas y técnicas de visualización de datos para poder aprovechar al máximo el potencial de sus datos.

+ Se crea una cuenta nueva en Google Data Studio.
+ Subir el archivo "/resources/datos.csv" o ejecutar el API de Python públicado con la URL http://127.0.0.1:8000/process_json (si se configuró las variables de entorno) o el equivalente de la API en Cloud.
+ Se habilita la API de Google Storage en Google Data Studio.
+ Se genera los diferentes tableros en la hoja que permita interactuar con los datos:
  + Reporte básico públicado:
    + https://datastudio.google.com/reporting/bbf8debb-e6f6-4305-af6b-3208db5ef3b9/page/ceABD
  + Vista de un reporte básico:
    + ![](https://raw.githubusercontent.com/JohanValero/TextZeroShotAPI/development/resources/dashboard_1.PNG "Reporte básico")
  + Vista de interactuando con los datos de un reporte:
    + ![](https://raw.githubusercontent.com/JohanValero/TextZeroShotAPI/development/resources/dashboard_2.PNG "Interactuando con el reporte")

## Modelos predictivos

...