import os
import json
import csv

# Se importa Flask y otras funciones necesarias
# para crear una aplicación web.
from flask import Flask, request, jsonify

# Se importa la función de pipeline de la biblioteca de
# procesamiento de lenguaje natural "transformers".
from transformers import pipeline

# Este módulo proporciona acceso a la plataforma de almacenamiento de
# Google Cloud, que permite almacenar y acceder a archivos en la nube.
from google.cloud import storage

gClassifier = None

# Se definen las etiquetas candidatas para la clasificación.
gCandidateLabels = ["insulto", "enojado", "negativo", "queja"]

# Se define una plantilla de hipótesis para utilizar
# con el clasificador.
gHypothesysTemplate = "Esta reseña es {}." 

# Máxima calificación a ser otenida por una
# evaluación de reseña.
gMaxScore = 0.4

# Lista de los meses del año en español.
gMonths = [
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre"
]

# Nombre del bucket de Google Cloud Storage donde se encuentran los archivos.
gCLOUD_BUCKET = 'bucket-analitica-qa'

# Nombre del archivo JSON en el bucket.
gCLOUD_BLOB_JSON : str = 'data_json/comentarios-youtube.json'

# Nombre del archivo CSV que se guardará en el bucket.
gCLOUD_BLOB_CSV  : str = 'data_csv/comentarios-youtube.csv'

# Se obtiene el valor del puerto a utilizar para la aplicación
# web desde una variable de entorno.
gPORT = os.getenv('PORT', default = None)
print("PORT:", gPORT)

# Se crea una instancia de Flask y se asigna a la
# variable "app" como aplicación web.
app = Flask(__name__)

def verify_list(iList: list[str], iClassifier, iMinValue: float) -> list[bool]:
    print("TYPE OF ARRAY: ", type(iList), ", TYPE [0]: ", type(iList[0]))
    vResult = iClassifier(
        iList,
        candidate_labels = gCandidateLabels,
        hypothesis_template = gHypothesysTemplate
    )
    print(vResult)
    return None
    

# Se define una función para verificar si el texto de entrada
# es considerado negativo por el clasificador.
def verify_text(iInputText: str, iClassifier, iMinValue: float) -> bool:

    # Si el texto es vacío o nulo, se devuelve False.
    if (not iInputText) or len(iInputText) == 0:
        return False
    
    # Se ejecuta el clasificador con el texto de entrada.
    vResult = iClassifier(
        iInputText,
        candidate_labels = gCandidateLabels,
        hypothesis_template = gHypothesysTemplate
    )
    
    # Se verifica si alguna de las puntuaciones obtenidas por
    # el clasificador es mayor al valor mínimo especificado.
    for vScore in vResult['scores']:
        if vScore > iMinValue:
            return True
    
    # Si no se ha encontrado ninguna puntuación mayor al valor
    # mínimo, se devuelve False.
    return False

# Obtiene los datos en formato JSON desde el bucket de Google Cloud Storage.
def get_json():
    # Crea un cliente(conexión) de Google Cloud Storage
    vClient = storage.Client()
    
    # Obtiene conexión al bucket.
    vBucket = vClient.get_bucket(gCLOUD_BUCKET)
    
    # Obtiene el blob (archivo) del bucket.
    vBlob = vBucket.get_blob(gCLOUD_BLOB_JSON)
    
    # Descarga el blob(archivo) JSON en una cadena de texto.
    vJSON_Data = vBlob.download_as_string()
    
    # Convierte la cadena de texto JSON en un diccionario Python.
    vJSON_Data = json.loads(vJSON_Data)
    return vJSON_Data

# Esta función recibe una lista de diccionarios y escribe cada uno de ellos en un archivo CSV.
def write_csv(iJsonData : list[ dict[ str, any ] ] ) -> None:
    # Abre el archivo CSV en modo escritura
    with open('datos.csv', 'w', encoding = 'UTF-8', newline='') as vFile:
        # Especifica los nombres de las columnas
        vFieldNames = [
            'valoracion',
            'comentario',
            'fecha',
            'valoracion_number',
            'score',
            'day',
            'month',
            'month_string',
            'year'
        ]
        # Crea un objeto DictWriter para escribir el archivo CSV.
        vWriter = csv.DictWriter(vFile, fieldnames = vFieldNames)
        # Escribe la primera fila con los nombres de las columnas.
        vWriter.writeheader()
        # Escribe las filas restantes con los datos de cada diccionario.
        vWriter.writerows(iJsonData)

# Esta función sube el archivo CSV al bucket de Google Cloud Storage
def save_csv_in_bucket() -> None:
    # Crea un cliente de Google Cloud Storage.
    vClient = storage.Client()
    # Selecciona el bucket.
    vBucket = vClient.get_bucket(gCLOUD_BUCKET)
    # Crea un blob en el bucket.
    vBlob = vBucket.blob(gCLOUD_BLOB_CSV)
    # Abre el archivo CSV en modo lectura binaria.
    with open("datos.csv", 'rb') as vFile:
        # Sube el archivo al blob.
        vBlob.upload_from_file(vFile)

# Esta función recibe un mes en forma de cadena de
# texto y devuelve su número y nombre completo.
def get_month(iMonth: str) -> str:
    # Recorre la lista de meses
    for i, vM in enumerate(gMonths):
        # Si el mes está en la cadena de
        # texto, devuelve su índice y nombre.
        if vM in iMonth:
            return i, vM
    # Si no se ha encontrado el mes, devuelve -1 y None.
    return -1, None

# Se define una ruta para la aplicación web que utiliza el
# método GET.
@app.route('/', methods = ['GET'])
def clasifica_texto():
    # Se carga el modelo machine learning para predecir la categoría
    # de una queja del call-center.
    # El modelo se basa en BERT y está preparado para procesar
    # texto en español.
    global gClassifier
    if gClassifier is None:
        gClassifier = pipeline("zero-shot-classification", model = "./local_model_pretrained")
    
    # Se obtiene el texto a clasificar desde el parámetro "text" de la petición.
    vInputText = request.args.get("text")
    
    # Se verifica si la reseña es negativa.
    vFlag = verify_text(
        vInputText,
        gClassifier,
        gMaxScore
    )
    
    # Se construye la respuesta JSON.
    vResult = {
        "status": "OK",
        "response": ("reseña negativa" if vFlag else "reseña positiva"),
        "response-bool": vFlag
    }
    
    # Convierte un diccionario Python a formato JSON.
    return jsonify(vResult)

# Procesa los datos de un archivo guardado en un JSON y guarda
# los resultados en un archivo CSV en un Bucket. 
@app.route('/process_json')
def process_json():
    # Obtiene los datos del JSON.
    vJSON_Data = get_json()
    
    # Se carga el modelo machine learning para predecir la categoría
    # de una queja del call-center.
    # El modelo se basa en BERT y está preparado para procesar
    # texto en español.
    global gClassifier
    if gClassifier is None:
        gClassifier = pipeline("zero-shot-classification", model = "./local_model_pretrained")
    
    vResult = list(map(lambda x: x["comentario"], vJSON_Data))
    verify_list(vResult, gClassifier, gMaxScore)
    #print(vResult[0])
    
    # Recorre los datos del JSON y extrae información revelante.
    for i, vData in enumerate(vJSON_Data):
        # Añade un campo al diccionario con solamente el valor númerico de la reseña.
        vData["valoracion_number"] = vData["valoracion"][12]
        # Añade un campo al diccionario con el score, calculado como el valor de la valoración dividido entre 5.
        vData["score"] = float(vData["valoracion"][12])/5
        # Añade un campo al diccionario con el día extraído de la fecha.
        vData["day"] = int(vData["fecha"][0:2])
        # Añade dos campos al diccionario con el índice del mes y el nombre del mes extraídos de la fecha.
        vData["month"], vData["month_string"] = get_month(vData["fecha"])
        # Añade un campo al diccionario con el año extraído de la fecha.
        vData["year"] = int(vData["fecha"][-4:len(vData["fecha"])])
        
        #vData["prediction"] = verify_text(
        #    vData["comentario"],
        #    gClassifier,
        #    gMaxScore
        #)
        #print("[" + str(i) + "/" + str(len(vJSON_Data)) + "] => " + str( 100*i/len(vJSON_Data) ), end="" )
    
    # Escribe los datos modificados en un archivo CSV
    write_csv(vJSON_Data)
    
    # Guarda el archivo CSV en el bucket
    save_csv_in_bucket()
    
    # Crea la respuesta JSON de la petición GET.
    vResult = {
        "status": "ok"
    }
    return jsonify(vResult)

# Si este archivo es ejecutado directamente, se despliega un servidor de pruebas para depuración.
if __name__ == "__main__":
    # Si no se proporciona un puerto, se usa el puerto 8000 por defecto.
    gPORT = gPORT if gPORT is not None else 8000
    print("Development server running in port: ", gPORT)
    app.run(
        host = "0.0.0.0",
        port = gPORT,
        debug = True
    )