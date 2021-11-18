from collections import defaultdict
from flask import Flask
from flask.wrappers import Response
from werkzeug.wrappers import response
import requests, json, random

order = defaultdict(lambda: [0, 0])
menu = {}
totalCostOfOrder = 0

def getOrder():
    global totalCostOfOrder,order
    totalCostOfOrder = 0
    order = defaultdict(lambda: [0, 0])
    print(order)
    while(1):
        print("enter item id from menu or enter -1 to finish order AND GENERATE BILL")
        itemid = int(input())
        if itemid == -1:
            break
        print("if half enter 0; if full enter 1")
        type = int(input())
        print("enter quantity")
        quantity = int(input())
        order[itemid][type] += quantity
        totalCostOfOrder += (int(menu[itemid][type])*quantity)
    
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

        for i in order:
            if order[i][0] > 0:
                print(f'Item {i}[Half][{order[i][0]}]: {format(int(menu[i][0])*order[i][0], ".2f")}')
            if order[i][1] > 0:
                print(f'Item {i}[Full][{order[i][1]}]: {format(int(menu[i][1])*order[i][1], ".2f")}')
        
        total_item_cost = totalCostOfOrder-tipValue
        print(f'Total: {format(total_item_cost,".2f")}')
        
        print(f'Tip: {format(tip,".2f")}%')
        randomDiscountValue = round(totalCostOfOrder*(0.01)*randomDiscountOutcome, 2)
        print(f'Discout/Increase: {format(randomDiscountValue,".2f")}')
        totalCostOfOrder += randomDiscountValue
        print(f'Final Total: {format(totalCostOfOrder,".2f")}')
        updatedShare = round(totalCostOfOrder/numberOfPeopleToSplit, 2)
        updatedShare = round(updatedShare, 2)
        print(f'Updated share of each person is: {format(updatedShare,".2f")}')

        res = requests.post('http://localhost:8000/transaction/add',json= {
                                                                            'item_total_cost':total_item_cost,
                                                                            'tip_percent':tip,
                                                                            'number_of_persons_to_split':numberOfPeopleToSplit,
                                                                            'random_discount_val':randomDiscountValue,
                                                                            'total_bill_cost':totalCostOfOrder
                                                                            }).content

        transaction_id = json.loads(res)['transaction_id']
        
        for i in order:
            if order[i][0] > 0:
                requests.post('http://localhost:8000/item_list/add',json= {
                                                                            'transaction_id':transaction_id,
                                                                            'item_id':i,
                                                                            'type': 'Half',
                                                                            'quantity':order[i][0]
                                                                        })
            if order[i][1] > 0:
                requests.post('http://localhost:8000/item_list/add',json= {
                                                                            'transaction_id':transaction_id,
                                                                            'item_id':i,
                                                                            'type': 'Full',
                                                                            'quantity':order[i][1]
                                                                        }) 

        print("bill added to db successfully")


while(1):
    print("select any of the following choices")
    print("1. Fetch the menu")
    print("2. Order items")
    print("3. Generate Bill")
    print("4. View Previous Transaction")
    print("5. Exit")
    choice = int(input())

    if choice==1:
        menu = {}
        
        res = requests.get('http://localhost:8000/menu/fetch').content
        obj = json.loads(res)
        print("item id\t\thalf plate price\tfull plate price")
        for i in obj:
            print(f'{i}\t\t{obj[i]["half_plate_price"]}\t\t\t{obj[i]["full_plate_price"]}')
            menu[int(i)]=[obj[i]["half_plate_price"],obj[i]["full_plate_price"]]

    elif choice==2:
        getOrder()

    elif choice==5:
        break

    else:
        print("invalid option selected")    