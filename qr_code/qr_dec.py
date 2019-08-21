import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time 
import sqlite3
from sqlite3 import Error
 
 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

 
conn=create_connection('hackathon.db')   

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, frame = cap.read()
    f=0
    decodedObjects = pyzbar.decode(frame)
    s=''
    ar=[]
    for obj in decodedObjects:
        s=obj.data.decode('utf-8')
        #print(s)
        time.sleep(5)
        
        #cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                    #(255, 0, 0), 3)
        ar=s.split(' ')    
    if len(ar)!=0:              
    
        name,mfd,exp=s.split(' ')                
        cur=conn.cursor()
        #print(db_conn.conn)
        try:
            cur.execute('''INSERT INTO items VALUES (?,?,?)''', (ar[0],ar[1],ar[2]))
        except:
            print("dup")
        conn.commit()    
    
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break