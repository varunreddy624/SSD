from flask import Flask
from flask.wrappers import Response
from werkzeug.wrappers import response
import requests, json

while(1):
    print("select any of the following choices")
    print("1. Fetch the menu")
    print("3. Exit")
    choice = int(input())

    if choice==1:
        res = requests.get('http://localhost:8000/read').content
        obj = json.loads(res)
        print("item id\t\thalf plate price\tfull plate price")
        for i in obj:
            print(f'{i}\t\t{obj[i]["half_plate_price"]}\t\t\t{obj[i]["full_plate_price"]}')
        
    elif choice==3:
        break
    else:
        print("invalid option selected")