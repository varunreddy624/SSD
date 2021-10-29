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
    


print("enter item id from menu")
itemid = int(input())
print("if plate enter 1 if full enter 2")
type = int(input())
print("enter quantity")
quantity = int(input())
print("enter the percentage of tip in number of either 0 or 10 or 20")
tip = int(input())
total = (1+(0.01*(tip)))*int(menu[itemid][type])*quantity
total = round(total,2)
print("amount to be paid is "+str(total))
print("enter number of people to split bill")
numberOfPeopleToSplit = int(input())
individualShare = total / numberOfPeopleToSplit
individualShare = round(individualShare,2)
print("share for each person "+str(individualShare))
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
    print("result of lucky draw is "+str(randomDiscountOutcome)+"%")
    if(randomDiscountOutcome >= 0):
        print(" **** ")
        print("*    *")
        print("*    *")
        print("*    *")
        print("*    *")
        print(" **** ")
    else:
        print(" ****\t ****")
        print("|    |\t|    |")
        print("|    |\t|    |")
        print("|    |\t|    |")
        print(" ****\t ****")
        print("      {}")
        print("    ______")
else:
    randomDiscountOutcome = 0


print(f'Item {itemid}[{quantity}]: {int(menu[itemid][type])*quantity}')
print(f'Total: {int(menu[itemid][type])*quantity}')
print(f'Tip percentage: {tip}')
print(f'Discout/Increase Percent: {randomDiscountOutcome}')
finalTotal = (1+(0.01*randomDiscountOutcome))*total
finalTotal = round(finalTotal,2)
print(f'Final Total: {finalTotal}')
updatedShare = finalTotal/numberOfPeopleToSplit
updatedShare = round(updatedShare,2)
print("Updated share of each person is: "+str(updatedShare))


# 5
# 1
# 3
# 20
# 2
# yes
