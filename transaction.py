################################################################################
#File: transaction.py
#Date: 2020-25-02
#Version: 1.0
#Purpose: Manages the current user tranasction by keeping track of each item
#		  added, total cost, adding/removing from transcation and printing
#		  receipt to .txt when finished.
###############################################################################

#Creates the empty "transaction" list
def createTrans():
	return [],0

#Adds an item to the "transaction" list, in the format of a list
def addToTrans(trans,name,price):
	global cost
	item = [name,price]
	trans.append(item)
	cost += int(price)
	return trans

#Removes specified item from the "transaction" list
def removeFromTrans(trans,location):
	global cost
	cost -= int(trans[location][1])
	del trans[location]
	return trans

#Prints the entire "transaction" list out in a neat format
def printTrans(trans,cost):
	for i in trans:
		print(str(i[0])+" "+addDecimal(str(i[1])))
	print("Taxes are "+addDecimal(cost*0.15))
	print("Total bill is "+addDecimal(cost*1.15))

#Helper function to add decimal places into price strings when printing to user
def addDecimal(value):
	value = int(value)
	length = len(str(value))
	strNum = "$"+str(value)[:length-2]+"."+str(value)[length-2:]
	return strNum

###############################################################################
#Testing
from inventoryManager import *
a,cost = createTrans()
print("Values of a:", a, "Cost: ",addDecimal(cost))

while(True):
	cmd = input("Select Transaction: 1.Add Name 2.Add ISBN 3.Remove 4.Finish\n")
	if (cmd == "1"):
		name = input("Add which item?\n")
		item = searchName(name).split("|")
		addToTrans(a,item[1],item[2])
		print("Item " + item[1] + " added!")
	elif (cmd == "2"):
		name = input("Add which item?\n")
		item = searchIsbn(name).split("|")
		addToTrans(a,item[1],item[2])
		print("Item " + item[1] + " added!")
	elif(cmd == "3"):
		location = int(input("Remove which item?\n"))
		removeFromTrans(a,location)
		print("Item " + name + " removed!")
	elif(cmd == "4"):
		break
	else:
		pass

printTrans(a,cost)