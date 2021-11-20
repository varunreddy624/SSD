from collections import defaultdict
from flask import Flask
from flask.wrappers import Response
from werkzeug.wrappers import response
import requests, json, random

session = requests.Session()

order = defaultdict(lambda: [0, 0])
menu = {}
totalCostOfOrder = 0
is_logged_in = False


def signup():
    username = input("enter username\n")
    password = input("enter password\n")
    is_chef = False

    res = session.post('http://localhost:8000/signup',json={
        'username':username,
        'password':password,
        'is_chef':is_chef
    }).content

    obj = json.loads(res)
    
    print(obj['data'])

def login():

    global is_logged_in

    username = input("enter username\n")
    password = input("enter password\n")

    res = session.post('http://localhost:8000/login',json={
        'username':username,
        'password':password,
    }).content

    obj = json.loads(res)

    if(obj['data']=="success"):
        is_logged_in = True
        print("login success")

    else:
        print("invalid credentials")

def getMenu():
    global menu
    menu = {}
        
    res = session.get('http://localhost:8000/menu/fetch').content
    obj = json.loads(res)
    for i in obj:
        menu[int(i)]=[obj[i]["half_plate_price"],obj[i]["full_plate_price"]]


def printMenu():
    print("item id\t\thalf plate price\tfull plate price")
    for i in menu:
        print(f'{i}\t\t{menu[i][0]}\t\t\t{menu[i][1]}')


def printBill(total_bill_summary):

    present_order=total_bill_summary['order']
    item_total_cost=total_bill_summary['item_total_cost']
    randomDiscountValue=total_bill_summary['random_discount_val']
    totalCostOfOrder=total_bill_summary['total_bill_cost']
    updatedShare=total_bill_summary['updated_share_of_each_person']
    tip=total_bill_summary['tip_percent']


    for i in present_order:
        menukey=i
        if type(i)!=int:
            menukey=int(i)

        if present_order[i][0] > 0:
            print(f'Item {i}[Half][{present_order[i][0]}]: {format(menu[menukey][0]*present_order[i][0], ".2f")}')
        if present_order[i][1] > 0:
            print(f'Item {i}[Full][{present_order[i][1]}]: {format(menu[menukey][1]*present_order[i][1], ".2f")}')



    print(f'Total: {format(item_total_cost,".2f")}')    
    print(f'Tip: {format(tip,".2f")}%')
    print(f'Discout/Increase: {format(randomDiscountValue,".2f")}')
    print(f'Final Total: {format(totalCostOfOrder,".2f")}')
    print(f'Updated share of each person is: {format(updatedShare,".2f")}')


def getOrder():
    if menu=={}:
        print("See the latest menu to order")
        return 
    
    else:
        global totalCostOfOrder,order
        print(order)
        while(1):
            print("enter item id from menu or enter -1 to finish order")
            itemid = int(input())
            if itemid == -1:
                break
            print("if half enter 0; if full enter 1")
            type = int(input())
            print("enter quantity")
            quantity = int(input())
            order[itemid][type] += quantity
            totalCostOfOrder += (int(menu[itemid][type])*quantity)


def generateBill():
    global totalCostOfOrder,order

    if len(order)==0:
        print("Add items to generate bill")
        return 

    else:

        print("enter the percentage of tip in number of either 0 or 10 or 20")
        tip = int(input())
        tipValue = round(totalCostOfOrder*(0.01)*tip, 2)
        totalCostOfOrder += tipValue
        print(f'amount to be paid is {format(totalCostOfOrder,".2f")}')
        print("enter number of people to split bill")
        numberOfPeopleToSplit = int(input())
        individualShare = round(totalCostOfOrder/numberOfPeopleToSplit, 2)
        print(f'share for each person {format(individualShare,".2f")}')
        print("Do you wish to participate in an event called “Test your luck”?")
        print("Input yes or no")
        choice = input()
        if choice == "yes":
            arr = [20]*20 + [0]*8 + [-10]*6 + [-25]*4 + [-50]*2
            '''
                Above array's size is 40, values represent discout percentage.
                So when we are randomly selecting an element from above array we have
                20/40 ==> 50% probability for +20%
                8/40 ==> 20% probability for +0%
                6/40 ==> 15% probability for -10%
                4/40 ==> 10% probability for -25%
                2/40 ==> 5% probability for -50%
            '''
            randomDiscountOutcome = random.choice(arr)
            if(randomDiscountOutcome >= 0):
                print(" **** ")
                print("*    *")
                print("*    *")
                print("*    *")
                print("*    *")
                print(" **** ")
                print("better luck next time")
                print(f'for now your bill is increased by {randomDiscountOutcome}%')
            else:
                print(" ****             ****")
                print("|    |          |    |")
                print("|    |          |    |")
                print("|    |          |    |")
                print(" ****	         ****")
                print("          {}")
                print("    ______________")
                print("congratulations")
                print(f'you got a discount of {randomDiscountOutcome}% on the bill')
        else:
            randomDiscountOutcome = 0

        total_bill_summary = {}
        
        item_total_cost = totalCostOfOrder-tipValue
        randomDiscountValue = round(totalCostOfOrder*(0.01)*randomDiscountOutcome, 2)
        totalCostOfOrder += randomDiscountValue
        updatedShare = round(totalCostOfOrder/numberOfPeopleToSplit, 2)
        updatedShare = round(updatedShare, 2)
        
        total_bill_summary['order']=order
        total_bill_summary['updated_share_of_each_person']=updatedShare
        total_bill_summary['item_total_cost']=item_total_cost
        total_bill_summary['random_discount_val']=randomDiscountValue
        total_bill_summary['total_bill_cost']=totalCostOfOrder
        total_bill_summary['tip_percent']=tip

        printBill(total_bill_summary)

        res = session.post('http://localhost:8000/transaction/add',json= {
                                                                            'item_total_cost':item_total_cost,
                                                                            'tip_percent':tip,
                                                                            'updated_share_of_each_person':updatedShare,
                                                                            'random_discount_val':randomDiscountValue,
                                                                            'total_bill_cost':totalCostOfOrder
                                                                            }).content

        transaction_id = json.loads(res)['transaction_id']
        
        orderSummary=[]
        for i in order:
            if order[i][0] > 0:
                orderSummary.append({
                                    'item_id':i,
                                    'type': 'Half',
                                    'quantity':order[i][0]
                                    })
            if order[i][1] > 0:
                orderSummary.append({
                                    'item_id':i,
                                    'type': 'Full',
                                    'quantity':order[i][1]
                                    }) 
            
        session.post('http://localhost:8000/item_list/add',json= {
                                                                        'transaction_id':transaction_id,
                                                                        'items_list':orderSummary
                                                                })
        print("bill added to db successfully")

        order = defaultdict(lambda: [0, 0])
        totalCostOfOrder = 0


def viewPreviousTransactions():
    global menu

    if menu=={}:
        getMenu()

    res = session.get('http://localhost:8000/transaction/fetch/all').content
    obj = json.loads(res)
    if(len(obj)==0):
        print("no transactions made yet")
        return
    else:
        print("transaction id \t\t total cost")
        for i in obj:
            print(f'{i}\t\t\t{obj[i]["total_bill_cost"]}')
        choice = int(input("enter the transaction id to view the transaction or -1 to exit\n"))
        if choice==-1:
            return 
        else:
            if str(choice) not in obj:
                print("enter valid transaction id in the list")
            else:
                res = session.post('http://localhost:8000/transaction/fetch/specific',json={'transaction_id':choice}).content
                obj = json.loads(res)
                printBill(obj['data'])


while(1):
    print("select any of the following choices")
    print("1. signup")
    print("2. login")
    print("3. Fetch the menu")
    print("4. Order items")
    print("5. Generate Bill")
    print("6. View Previous Transactions")
    print("7. logout")
    choice = int(input())

    if choice==1:
        signup()
    
    elif choice==2:
        login()

    elif choice==3:
        getMenu()
        printMenu()

    elif choice==4:
        getOrder()
    
    elif choice==5:
        generateBill()

    elif choice==6:
        viewPreviousTransactions()

    elif choice==7:
        break

    else:
        print("invalid option selected")    