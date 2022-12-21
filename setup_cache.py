# Se encarga de descargar y almacenar en caché el modelo de lenguaje antes de iniciar la aplicación.
from transformers import pipeline

gClassifier = pipeline(
    "zero-shot-classification", 
    model = "Recognai/bert-base-spanish-wwm-cased-xnli"
)

gClassifier(
    "Esto es una ejecución de prueba",
    candidate_labels = ["dummy"],
    hypothesis_template = '{}'
)