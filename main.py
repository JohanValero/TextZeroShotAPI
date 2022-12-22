import os

# Se importa Flask y otras funciones necesarias
# para crear una aplicación web.
from flask import Flask, request, jsonify

# Se importa la función de pipeline de la biblioteca de
# procesamiento de lenguaje natural "transformers".
from transformers import pipeline

gClassifier = None

# Se definen las etiquetas candidatas para la clasificación.
gCandidateLabels = ["insulto", "enojado", "negativo", "queja"]

# Se define una plantilla de hipótesis para utilizar
# con el clasificador.
gHypothesysTemplate = "Esta reseña es {}." 

# Máxima calificación a ser otenida por una
# evaluación de reseña.
gMaxScore = 0.4

# Se obtiene el valor del puerto a utilizar para la aplicación
# web desde una variable de entorno.
gPORT = os.getenv('PORT', default = None)
print("PORT:", gPORT)

# Se crea una instancia de Flask y se asigna a la
# variable "app" como aplicación web.
app = Flask(__name__)

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