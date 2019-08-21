import requests
import json
from gtts import gTTS 
import os 
from BeautifulSoup import BeautifulSoup
import urllib2
import re
from py_edamam import Edamam
import time

initial_time = time.time()
flag = 0

def getRecipeByIngredients(ingredients):

    try: 
        from googlesearch import search 
    except ImportError:  
        print("No module named 'google' found") 
      
    query = "edamam"
    for x in ingredients:
        query = query + " " + x
    query = query + " site:www.edamam.com"

    for j in search(query, tld="co.in", num=5, stop=5, pause=2): 
        soup = BeautifulSoup(urllib2.urlopen(j))
        print soup.title.string


def produce_sound():
    global flag
    global initial_time

    if(flag == 1):
        return
    
    new_time = time.time()

    diff = new_time-initial_time

    if(diff <= 15):
        return

    initial_time = time.time()

    print("ALERT")

    mytext = 'Hello Infosyians, welcome to Hack With Infy'
  
    language = 'en'
      
    myobj = gTTS(text=mytext, lang=language, slow=False) 
      
    myobj.save("welcome.mp3") 
      
    os.system("mpg321 welcome.mp3") 
    flag = 1                            

def objectify(file_name):
    r = requests.post(
        "https://api.deepai.org/api/densecap",
        files={
            'image': open(file_name, 'rb'),
        },
        headers={'api-key': '8e634a28-01e5-45f4-9793-ea4971769e42'}
    )

    x = r.json()

    t_dict = {}

    t_dict['banana'] = 1
    t_dict['pineapple'] = 1
    t_dict['capsicum'] = 1
    t_dict['brinjal'] = 1
    t_dict['bottle'] = 1
    t_dict['apple'] = 1

    y = x['output']
    z = y['captions']

    listt = []

    for i in z:
        for words in i['caption'].split():
            if(str(words) in t_dict.keys()):
                listt.append(str(words))

    listt = list(dict.fromkeys(listt))

    return listt


import cv2
import numpy as np
import signal

cam = cv2.VideoCapture(1)

cv2.namedWindow("test")
cv2.moveWindow("test",550,400)


img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    x = np.amin(np.array(frame))
    y = np.amax(np.array(frame)) 

    if(y >= 180):
        produce_sound()
    else:
        flag = 0

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
        

cam.release()

cv2.destroyAllWindows()