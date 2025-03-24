import cv2
import cvzone
import time

from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
from cvzone.SerialModule import SerialObject
from time import sleep


# url = 'http://192.168.137.65/480x320.jpg' # URL para ESP32cam
# cap = cv2.VideoCapture(url)  # Capturar imagen desde url
cap = cv2.VideoCapture(0)  # Capturar imagen desde cámara de PC
#time.sleep(1)  # Esperar 1 segundo después de abrir la cámara
detector = FaceMeshDetector(maxFaces=1)  # Detector de cara
plotY = LivePlot(720, 480, [20, 50], invert=True)  # Gráfico
arduino = SerialObject()

# winName = 'IP_CAM'
# cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

idList = [22, 23, 24, 26, 110, 130, 157, 158, 159, 160, 161, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)
parpadeo = False
inicio = 0
final = 0
tiempo = 0
conteo_sue = 0
muestra = 0
sueno = False

while (1):

    #cap.open(url)  # Antes de capturar el frame abrimos la url

    #ret, img = cap.read()  # Captura de frame

    # if ret:
    #   cv2.imshow(winName,frame)

    #if not ret:
        #print("Error al leer el frame de la cámara")
        #continue
    try:
        ret, img = cap.read()
        if not ret:
            print("Error al leer el frame de la cámara")
            continue
    except cv2.error as e:
        print(f"Error de OpenCV: {e}")
        continue
    except Exception as e:
        print(f"Error general: {e}")
        continue


    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)

        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        lenghtVer, _ = detector.findDistance(leftUp, leftDown)
        lenghtHor, _ = detector.findDistance(leftLeft, leftRight)
        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lenghtVer / lenghtHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = round(sum(ratioList) / len(ratioList), 0)

        if ratioAvg < 34 and counter == 0 and parpadeo is False:
            blinkCounter += 1
            parpadeo = True
            inicio = time.time()
            counter = 1
            color = (0, 255, 0)
        elif ratioAvg > 34 and parpadeo is True:
            parpadeo = False
            final = time.time()

        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        tiempo = round(final - inicio, 0)

        if tiempo >= 3 and sueno is False:
            conteo_sue += 1
            muestra = tiempo
            inicio = 0
            final = 0
            sueno = True
            arduino.sendData([1])
            sleep(3)
        elif tiempo < 3 and sueno is True:
            arduino.sendData([0])
            sueno = False

        cvzone.putTextRect(img, f'Parpadeos: {blinkCounter}', (20, 50), colorR=color)
        cvzone.putTextRect(img, f'Duracion: {tiempo}', (20, 400), colorR=color)
        cvzone.putTextRect(img, f'Micro sueno: {conteo_sue}', (20, 450), colorR=color)

        imgPlot = plotY.update(ratioAvg, color)
        imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
    else:
        imgStack = cvzone.stackImages([img, img], 2, 1)

    cv2.imshow("Image", imgStack)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == 27:
        break
    if cv2.getWindowProperty("Image", cv2.WND_PROP_VISIBLE) < 1:  
        break  # Se cierra si el usuario presiona la "X"

cv2.destroyAllWindows()
