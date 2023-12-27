import sys
import cv2
import face_recognition
import numpy as np
import base64
from io import BytesIO
from PIL import Image

def es_tono_piel(parte_cara):
    imagen_hsv = cv2.cvtColor(parte_cara, cv2.COLOR_BGR2HSV)
    minimo = np.array([20, 30, 20], dtype="uint8")
    maximo = np.array([80, 255, 255], dtype="uint8")
    masc = cv2.inRange(imagen_hsv, minimo, maximo)
    mascara = cv2.bitwise_not(masc)
    #cv2.imshow("Mascara de Piel", mascara)
    #cv2.waitKey(0)
    porcentaje_piel = (cv2.countNonZero(mascara) / (parte_cara.size / 3)) * 100
    #print(porcentaje_piel)
    gris = cv2.cvtColor(parte_cara, cv2.COLOR_BGR2GRAY)
    brillo = np.mean(gris)
    #print(brillo)
    return porcentaje_piel > 50 and brillo < 70

def comparar_con_persona_en_imagen(credencial_cara_codificada, imagen):
    localizaciones_caras = face_recognition.face_locations(imagen)
    caras_codificadas = face_recognition.face_encodings(imagen, localizaciones_caras)

    for cara_codificada, ubicacion_cara in zip(caras_codificadas, localizaciones_caras):
        resultados = face_recognition.compare_faces([credencial_cara_codificada], cara_codificada)
        top, right, bottom, left = ubicacion_cara
        parte_cara = imagen[top:bottom, left:right]

        if True in resultados and es_tono_piel(parte_cara):
            return "Identity Verified. Access Granted."
        elif True in resultados:
            return "Correct identity, but this is a picture. Access Denied"
        else:
            return "Access Denied. Wrong person."

    return "No faces found in the image."

def procesar_imagen_b64(imagen_b64):
    imagen_b64 = imagen_b64.split(',')[1] 
    imagen_decodificada = base64.b64decode(imagen_b64)
    imagen = Image.open(BytesIO(imagen_decodificada))
    imagen = cv2.cvtColor(np.array(imagen), cv2.COLOR_RGB2BGR)
    return imagen

def ejecutar_reconocimiento(ruta_archivo):
    imagen = face_recognition.load_image_file(ruta_archivo)
    credencial_imagen = face_recognition.load_image_file("Mario.jpg")
    credencial_cara_codificada = face_recognition.face_encodings(credencial_imagen)[0]
    resultado = comparar_con_persona_en_imagen(credencial_cara_codificada, imagen)
    print(resultado)

if __name__ == "__main__":
    ruta_archivo = sys.argv[1]
    ejecutar_reconocimiento(ruta_archivo) 
