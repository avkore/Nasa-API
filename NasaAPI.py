import requests
import json
import sqlite3

con = sqlite3.connect('nasa.sqlite')  #Creating Connection and Cursor
cursor = con.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Nasa

(id INTEGER PRIMARY KEY AUTOINCREMENT,
Camera_Name VARCHAR(50),
Date VARCHAR(100),
URL VARCHAR(150));''')  #Creating Table With 4 Columns -> ID, Camera Name, Date, Link; ID is auto incremented.
  

con.commit()


def get_rover_info():
    try:
        sol = input("please enter random number: ")
        key = 'XNtODxE2xP0nGwfO1mrLKiNoEilLJsO6PtpUcdYJ'
        url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&api_key={key}'
        r = requests.get(url)
        status_code = r.status_code
        more_info = r.headers
        result = json.loads(r.text)
        if status_code == 200: #Works Only if Connection is Successful

            with open("data.json", 'w') as file:
                json.dump(result, file, indent=3)   #Writing Data To JSON

            photos = result['photos']
            link = photos[1]
            link1 = link["img_src"]               #Extracting Info From Dictionary
            camera = photos[0]
            camera1 = camera["camera"]
            camera2 = camera1["full_name"]
            date = photos[2]
            date1 = date["earth_date"]

            print(f"Image Link-> {link1} \nCamera Name-> {camera2} \nDate-> {date1}")   #Printing Data

            cursor.execute("INSERT INTO Nasa (Camera_Name, Date, URL) VALUES (?,?,?)", (camera2, date1, link1)) #Writing Data To Table
            con.commit() #Commiting Changes

        else:
            print("Connection Problem")  #If Connection Was not Successful

    except IndexError:
        print("Please Enter Different Number. There Is No Information For Current One.") #If API Could not Search Data


get_rover_info() #Calling Function
