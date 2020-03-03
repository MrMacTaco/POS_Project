# inventory.py
# Has 5 functions: Create, Add, Subtract, SearchISBN, SearchName
# Notes:
#       ISBN input must be a string, search returns are strings of fromat
#       "ISBN|NAME|PRICE|QUANTITY"

def create(isbn, name, price, quantity):

    # Create string of format ISBN|NAME|PRICE|QUANTITY
    createList = [str(isbn), str(name), str(price), str(quantity)]
    createString = "|".join(createList)
    createString = createString + "\n"

    # Check to see if item already exists
    if (searchIsbn(isbn) == createString):
        return True
    else:

        # Append to inventory.txt
        inventory = open("inventory.txt", "a")
        inventory.write(createString)
        inventory.close()
        return False

def add(isbn, quantity):
    
    # Find item in inventory and create list containing each line
    inventory = open("inventory.txt", "r")
    fileList = inventory.readlines()
    outputList = []
    for line in fileList:
        line = line.strip('\n')
        lineList = line.split("|")
        if (lineList[0] == str(isbn)):
            value = lineList[3]
            total = int(value) + int(quantity)
            lineList[3] = str(total)
            outputLine = "|".join(lineList)
            outputList.append(outputLine)
        else:
            outputList.append(line)
    inventory.close()

    # Overwrite inventory.txt with new blank file and fill in lines
    inventory = open("inventory.txt", "w+")
    inventory.write("\n".join(outputList))
    inventory.close()

def subtract(isbn, quantity):
    
    # Same as add() but subtracting
    inventory = open("inventory.txt", "r")
    fileList = inventory.readlines()
    outputList = []
    for line in fileList:
        line = line.strip('\n')
        lineList = line.split("|")
        if (lineList[0] == str(isbn)):
            value = lineList[3]
            total = int(value) - int(quantity)
            lineList[3] = str(total)
            outputLine = "|".join(lineList)
            outputList.append(outputLine)
        else:
            outputList.append(line)
    inventory.close()

    # Overwrite inventory.txt
    inventory = open("inventory.txt", "w+")
    inventory.write("\n".join(outputList))
    inventory.close()

def searchIsbn(isbn):

    # Check each line in inventory.txt for ISBN
    inventory = open("inventory.txt", "r")
    fileList = inventory.readlines()
    for line in fileList:
        lineList = line.split("|")
        if (lineList[0] == str(isbn)):
            return line
            break
    inventory.close()

def searchName(name):
    
    # Check each line in inventory.txt for Name
    inventory = open("inventory.txt", "r")
    fileList = inventory.readlines()
    for line in fileList:
        lineList = line.split("|")
        if (lineList[1].lower() == str(name).lower()):
            return line
            break
    inventory.close()
