# Este código contiene dos pruebas unitarias que verifican el comportamiento de
# la función verify_text. La primera prueba verifica que la función retorne False
# cuando se le pasa una reseña positiva, mientras que la segunda prueba verifica
# que la función retorne True cuando se le pasa una reseña negativa.
# La función verify_text recibe como argumentos el texto a verificar
# (vPositiveText o vNegativeText), un clasificador (gClassifier) y un
# puntaje máximo (gMaxScore). Si el puntaje obtenido por el clasificador es mayor o
# igual al puntaje máximo, se considera que la reseña es positiva y la función debería
# retornar False.
# En caso contrario, se considera que la reseña es negativa y la función debería retornar True.
# La función assert se utiliza para verificar que el valor que retorna verify_text es el esperado.
# Si el valor es el esperado, la prueba unitaria se considera exitosa y no se produce ningún error.
# Si el valor no es el esperado, se imprime un mensaje de error y la prueba unitaria se considera fallida.
# Al final del código, se imprime el mensaje "Test finish OK." si ambas pruebas
# unitarias se han completado exitosamente.
from main import verify_text, gMaxScore
from transformers import pipeline

gClassifier = pipeline(
    "zero-shot-classification", 
    model = "Recognai/bert-base-spanish-wwm-cased-xnli"
)

vPositiveText = "Esta es una empresa grandiosa"
assert verify_text(vPositiveText, gClassifier, gMaxScore) == False, "ERROR: Reseña positiva calificada como negativa."

vNegativeText = "Es mejor movistar"
assert verify_text(vNegativeText, gClassifier, gMaxScore) == True, "ERROR: Reseña negativa calificada como positiva."

gClassifier.save_pretrained("./local_model_pretrained")

print("Test finish OK.")