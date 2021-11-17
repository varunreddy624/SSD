from flask import Flask
from flask.wrappers import Response
from werkzeug.wrappers import response
import requests, json

while(1):
    print("select any of the following choices")
    print("1. Add item")
    print("2. Fetch the menu")
    print("3. Exit")
    choice = int(input())

    if choice==1:
        print("enter item id")
        item_id=int(input())
        print("enter half plate price")
        half_plate_price=int(input())
        print("enter full plate price")
        full_plate_price=int(input())
        res = requests.post('http://localhost:8000/create',json= {'item_id':item_id,'half_plate_price':half_plate_price,'full_plate_price':full_plate_price}).content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4, separators=(',',': '))
        print(json_formatted_str)

    elif choice==2:
        res = requests.get('http://localhost:8000/read').content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4)
        print(json_formatted_str)
        
    elif choice==3:
        break
    else:
        print("invalid option selected")