################################################################################
#File: transaction.py
#Date: 2020-25-02
#Version: 1.0
#Purpose: Manages the current user tranasction by keeping track of each item
#		  added, total cost, adding/removing from transcation and printing
#		  receipt to .txt when finished.
###############################################################################

class transaction:
	def __init__(self):
		self.trans = []
		self.cost = 0
		self.discount = 1

	#Adds an item to the "transaction" list, in the format of a list
	def addToTrans(self,name,price):
		item = [name,price]
		self.trans.append(item)
		self.cost += int(price)

	#Removes specified item from the "transaction" list
	def removeFromTrans(self,location):
		self.cost -= int(self.trans[location][1])
		del self.trans[location]

	#Prints the entire "transaction" list out in a neat format
	def printTrans(self):
		for i in self.trans:
			print(str(i[0])+" "+self.addDecimal(str(i[1])))
		print("Taxes are "+self.addDecimal(self.cost*0.15))
		print("Total bill is "+self.addDecimal(self.cost*1.15))

	#Discounts the transaction
	def discountTrans(self,percent):
		#Checks if percent is int or float and operates accordingly
		if (0 <= percent <= 100):
			self.discount = (100-percent)/100
		else:
			print("Invalid discount amount. Please try again.")

	#Helper function to add decimal places into price strings when printing to user
	def addDecimal(self,value):
		value = int(value)
		length = len(str(value))
		strNum = "$"+str(value)[:length-2]+"."+str(value)[length-2:]
		return strNum

	#Getter functions that just returns different variables
	def getTrans(self):
		return self.trans

	def __str__(self):
		return str(self.trans)

	def getTax(self):
		return int(self.cost*0.15*self.discount)

	def getTotal(self):
		return int(self.cost*1.15*self.discount)

	def getCost(self):
		return str(self.cost*self.discount)

	def getDiscount(self):
		return self.discount
