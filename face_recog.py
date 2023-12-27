import cv2
import face_recognition
import numpy as np

def es_tono_piel(parte_cara):
    imagen_hsv = cv2.cvtColor(parte_cara, cv2.COLOR_BGR2HSV)
    minimo = np.array([0, 48, 80], dtype="uint8")
    maximo = np.array([20, 255, 255], dtype="uint8")
    mascara = cv2.inRange(imagen_hsv, minimo, maximo)
    porcentaje_piel = (cv2.countNonZero(mascara) / (parte_cara.size / 3)) * 100
    return porcentaje_piel > 40  

def capturar_foto_credencial(camara):
    print("Please, press'c' to take the picture.")
    while True:
        ret, frame = camara.read()
        cv2.imshow('ID Picture - press "c" to take the picture', frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite('credencial_foto.jpg', frame)
            cv2.destroyAllWindows()
            break

def comparar_con_persona_en_camara(credencial_cara_codificada, camara):
    print("Look to the camera to verify your identity.")
    while True:
        ret, frame = camara.read()
        localizaciones_caras = face_recognition.face_locations(frame)
        caras_codificadas = face_recognition.face_encodings(frame, localizaciones_caras)

        for cara_codificada, ubicacion_cara in zip(caras_codificadas, localizaciones_caras):
            resultados = face_recognition.compare_faces([credencial_cara_codificada], cara_codificada)
            top, right, bottom, left = ubicacion_cara
            parte_cara = frame[top:bottom, left:right]
            if True in resultados and es_tono_piel(parte_cara):
                print("Â¡Identity Verified! Access Granted.")
            elif True in resultados:
                print("Correct identity, but this is a picture. Access Denied")
            else:
                print("Access Denied. Wrong person.")

        cv2.imshow('Comparing in real time - Presiona "q" para salir', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

def ejecutar_reconocimiento():
    camara = cv2.VideoCapture(0)
    capturar_foto_credencial(camara)
    credencial_imagen = face_recognition.load_image_file("credencial_foto.jpg")
    credencial_cara_codificada = face_recognition.face_encodings(credencial_imagen)[0]
    comparar_con_persona_en_camara(credencial_cara_codificada, camara)
    camara.release()

ejecutar_reconocimiento()