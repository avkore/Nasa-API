import requests
import json
import sqlite3

con = sqlite3.connect('nasa.sqlite')  #ქონექშენის და კურსორის შექმნა
cursor = con.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Nasa

(id INTEGER PRIMARY KEY AUTOINCREMENT,
Camera_Name VARCHAR(50),
Date VARCHAR(100),
URL VARCHAR(150));''')  #ვქმნი ცხრილს, სადაც მექნება 4 სვეტი-> აიდი, კამერის სახელი, თარიღი და ლინკი(ოთხივე სტრინგ(ვარჩარ) ტიპის მონაცემია)
                        # აიდის აუტოინკრემენტი აქვს, ასე რომ თვითონ გაიზრდება

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
        if status_code == 200: #მუშაობს მხოლოდ ქონექშენის დამყარების შემთხვევაში

            with open("data.json", 'w') as file:
                json.dump(result, file, indent=3)   #მოძებნილი ინფორმაციის ფაილში ჩაწერა

            photos = result['photos']
            link = photos[1]
            link1 = link["img_src"]               #სასურველი მონაცემების დიქშენერიდან ამოღება
            camera = photos[0]
            camera1 = camera["camera"]
            camera2 = camera1["full_name"]
            date = photos[2]
            date1 = date["earth_date"]

            print(f"Image Link-> {link1} \nCamera Name-> {camera2} \nDate-> {date1}")   #მონაცემების დაპრინტვა

            cursor.execute("INSERT INTO Nasa (Camera_Name, Date, URL) VALUES (?,?,?)", (camera2, date1, link1)) #ამ ბრძანებით ვსვავ ცხრილში სასურველ მონაცემებს
            con.commit() #ამ ბრძანებით ავსახავ ცხრილში ცვლილებებს

        else:
            print("Connection Problem")  #თუ ქონექშენი ვერ დამყარდა პრინტავს შემდეგ ტექსტს

    except IndexError:
        print("Please Enter Different Number. There Is No Information For Current One.") #ვითვალისწინებ იმ შემთხვევას, როდესაც შეყვანილი რიცხვზე ინფორმაცია არ იძებნება


get_rover_info() #ვიძახებ ფუნქციას
