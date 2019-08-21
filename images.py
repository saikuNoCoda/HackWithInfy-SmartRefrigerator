import requests
import json
from gtts import gTTS 
import os 
from BeautifulSoup import BeautifulSoup
import urllib2
import re
from py_edamam import Edamam
flag = 0
type_of_camera = 0

def produce_sound_2(string_req):

	mytext = string_req
  
	language = 'en'
	  
	myobj = gTTS(text=mytext, lang=language, slow=False) 
	  
	myobj.save("welcome.mp3") 
	  
	os.system("mpg321 welcome.mp3") 											

def telegram_bot_sendtext(bot_message):	
    bot_token = '849271376:AAFWA-wnwmT8dHFTNd2i3cYPQ8tZilIonn4'
    bot_chatID = '558471519'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
   

def getRecipeByIngredients(ingredients):

	try: 
	    from googlesearch import search 
	except ImportError:  
	    print("No module named 'google' found") 
	  
	query = "edamam"
	for x in ingredients:
		query = query + " " + x
	query = query + " site:www.edamam.com"

	print_text = ""

	for j in search(query, tld="co.in", num=5, stop=3, pause=2): 
		soup = BeautifulSoup(urllib2.urlopen(j))
		print_text = print_text + "\n" + soup.title.string
		print soup.title.string
		produce_sound_2(soup.title.string)
	telegram_bot_sendtext(print_text)

def produce_sound():
	global flag
	return
	if(flag == 1):
		return

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

cam = cv2.VideoCapture(type_of_camera)

cv2.namedWindow("test")
cv2.moveWindow("test",1200,400)


img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    x = np.amin(np.array(frame))
    y = np.amax(np.array(frame)) 

    if(y >= 180 and type_of_camera == 1):
    	produce_sound()
    else:
    	flag = 0

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        getRecipeByIngredients(objectify(img_name))
        img_counter += 1
        

cam.release()

cv2.destroyAllWindows()