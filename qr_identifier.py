import cv2
from pyzbar.pyzbar import decode
from PIL import Image
from firebase import firebase
import time
import db_management as db
import mqttManager as mqtt

cam = cv2.VideoCapture(0)
name = ''
oldName = ''
topic2Subscribe = "test321TCCeletricaEletronica"

while 1:
    ret, frame = cam.read()
    cv2.imwrite('test.png',frame)
    a = decode(Image.open('test.png'))
    if a != []:
        name = a[0][0].decode("utf-8")
        print(name)
    if name != oldName:
        oldName = name
        status = db.use_room(name,'test321')
        if status == 1:
            print("usuario permitido")
            mqtt.set_msg(topic2Subscribe,'open')
            a = mqtt.get_msg(topic2Subscribe+'1')
            print(a)
            if a == b'Received':
                print("abriu")
            else:
                print("rejeitado")

