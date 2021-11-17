from flask import Flask
from flask.wrappers import Response
from werkzeug.wrappers import response
import requests, json

while(1):
    print("select any of the following choices")
    print("1. Add student")
    print("2. Fetch all students")
    print("3. Update student")
    print("4. Delete student")
    print("5. Exit")
    choice = int(input())
    if choice==1:
        print("enter id")
        id=int(input())
        print("enter name")
        name=input()
        print("enter stream")
        stream=input()
        res = requests.post('http://localhost:8000/create',json= {'id':id,'name':name,'stream':stream}).content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4, separators=(',',': '))
        print(json_formatted_str)
    elif choice==2:
        res = requests.get('http://localhost:8000/read').content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4)
        print(json_formatted_str)
    elif choice==3:
        print("enter id")
        id=int(input())
        print("enter name")
        name=input()
        print("enter stream")
        stream=input()
        res = requests.put('http://localhost:8000/update',json= {'id':id,'name':name,'stream':stream}).content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4)
        print(json_formatted_str)
    elif choice==4:
        print("enter id")
        id=int(input())
        res = requests.delete('http://localhost:8000/delete',json= {'id':id}).content
        obj = json.loads(res)
        json_formatted_str = json.dumps(obj, indent=4)
        print(json_formatted_str)
    elif choice==5:
        break
    else:
        print("invalid option selected")