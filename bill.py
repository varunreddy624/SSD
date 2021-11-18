import csv
import random
from typing import DefaultDict, final


menu = []
with open('Menu.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    for item in reader:
        menu.append(item)

print("MENU")
print("Item No Half Plate Full Plate")
for i in range(len(menu)):
    if i != 0:
        print("\t".join(menu[i]))

order = DefaultDict(lambda: [0, 0])
totalCostOfOrder = 0


while(1):
    print("enter item id from menu or enter -1 to finish order")
    itemid = int(input())
    if itemid == -1:
        break
    print("if half enter 1; if full enter 2")
    type = int(input())
    print("enter quantity")
    quantity = int(input())
    order[itemid][type-1] += quantity
    totalCostOfOrder += (int(menu[itemid][type])*quantity)

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
        print(f'Item {i}[Half][{order[i][0]}]: {format(int(menu[i][1])*order[i][0], ".2f")}')
    if order[i][1] > 0:
        print(f'Item {i}[Full][{order[i][1]}]: {format(int(menu[i][2])*order[i][1], ".2f")}')
print(f'Total: {format(totalCostOfOrder-tipValue,".2f")}')
print(f'Tip: {format(tip,".2f")}%')
randomDiscountValue = round(totalCostOfOrder*(0.01)*randomDiscountOutcome, 2)
print(f'Discout/Increase: {format(randomDiscountValue,".2f")}')
totalCostOfOrder += randomDiscountValue
print(f'Final Total: {format(totalCostOfOrder,".2f")}')
updatedShare = round(totalCostOfOrder/numberOfPeopleToSplit, 2)
updatedShare = round(updatedShare, 2)
print(f'Updated share of each person is: {format(updatedShare,".2f")}')

