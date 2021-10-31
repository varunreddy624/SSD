import csv
import random
from typing import final


menu=[]
with open('Menu.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    for item in reader:
        menu.append(item)

print("MENU")
print("Item No Half Plate Full Plate")
for i in range(len(menu)):
    if i!=0:
        print("\t".join(menu[i]))
    
order=[]
totalCostOfOrder=0


while(1):
    print("enter item id from menu or enter -1 to finish order")
    itemid = int(input())
    if itemid==-1:
        break
    print("if plate enter 1; if full enter 2")
    type = int(input())
    print("enter quantity")
    quantity = int(input())
    order.append([itemid,type,quantity])
    totalCostOfOrder+=(int(menu[itemid][type])*quantity)

print("enter the percentage of tip in number of either 0 or 10 or 20")
tip = int(input())
tipValue = round(totalCostOfOrder*(0.01)*tip,2)
totalCostOfOrder+=tipValue
print(f'amount to be paid is {format(totalCostOfOrder,".2f")}')
print("enter number of people to split bill")
numberOfPeopleToSplit = int(input())
individualShare = round(totalCostOfOrder/numberOfPeopleToSplit,2)
print(f'share for each person {format(individualShare,".2f")}')
print("The restaurant has started a limited time event called “Test your luck”. Do you wish to participate in this event? Input yes or no")
choice = input()
if choice=="yes":
    arr=[20]*20 + [0]*8 + [-10]*6 + [-25]*4 + [-50]*2
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
        print(f'better luck next time, for now your bill is increased by {randomDiscountOutcome}%')
    else:
        print(" ****\t ****")
        print("|    |\t|    |")
        print("|    |\t|    |")
        print("|    |\t|    |")
        print(" ****\t ****")
        print("      {}")
        print("    ______")
        print(f'congratulations, you got a discount of {randomDiscountOutcome}% on the bill')
else:
    randomDiscountOutcome = 0

for i in order:
    print(f'Item {i[0]}[{i[2]}]: {int(menu[i[0]][i[1]])*i[2]}')
print(f'Total: {format(totalCostOfOrder-tipValue,".2f")}')
print(f'Tip: {format(tipValue,".2f")}')
randomDiscountValue = round(totalCostOfOrder*(0.01)*randomDiscountOutcome,2)
print(f'Discout/Increase: {format(randomDiscountValue,".2f")}')
totalCostOfOrder += randomDiscountValue
print(f'Final Total: {format(totalCostOfOrder,".2f")}')
updatedShare = round(totalCostOfOrder/numberOfPeopleToSplit,2)
updatedShare = round(updatedShare,2)
print(f'Updated share of each person is: {format(updatedShare,".2f")}')