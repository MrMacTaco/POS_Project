from tkinter import *
from tkinter import ttk
from core_functions import *
from transaction import *
from inventory import *
COL_BACKDROP = "#CACACA"
COL_TITLE = "#A1A1A1"
COL_DARK = "#A1A1A1"
COL_BUTTON = "#3071FF" ##"#2B64E5" ## action button colour
COL_CONFIRM = "#2FC633" ## confirm button colour
## The maximum length of strings shown in the transaction panel, in characters
LEN_ITEM = 30
HEIGHT_MAIN = 360
WIDTH_SIDE_BUTTON = 20
HEIGHT_SIDE_BUTTON = 2 ## The heigh (in lines) of left and right panel objects
HEIGHT_CENTER = 3
WIDTH_CENTER = 40
def searchKey(event):
    searchButton()
def addKey(event):
    addItemTrans()
def rmKey(event):
    rmItemTrans()
def discKey(event):
    editDiscount()
def confirmKey(event):
    tPage.iList.confirmButton()
def resetAll(event):
    ## Reset the program for the next user
    tPage.iList.confirmButton()
    resetSearchResult()
    file = open("receipt.txt","w")
    file.write("")
def searchButton():
    global itemName, itemPrice
    key = entryVar.get()
    if (key == ""):
        ## Don't update if nothing was entered
        return False
    ## Check if an isbn was entered
    if (key.isdigit() and len(key) == 10 ):
        item = searchIsbn(key)
    else:
        item = searchName(key)
    if item == None:
        ## If no item is found, show an error
        isbnVar.set("Item '"+ key + "' not found")
        nameVar.set("")
        priceVar.set("")
        quantityVar.set("")
        itemName = None
        itemPrice = None
    else:
        ## Show the item
        item = item.split("|")
        entryVar.set("")
        isbnVar.set("ISBN: " + item[0])
        nameVar.set("Title: " + item[1])
        priceVar.set("Price: " + priceToString(item[2]))
        quantityVar.set("Quantity: " + str(int(item[3])))
        itemName = item[1]
        itemPrice = int(item[2])
    return True
def addItemTrans():
    global itemName, itemPrice
    if itemName == None:
        return False
    tPage.iList.addItemInt(itemName,itemPrice)
    tPage.iList.lBox.curselection[0]
def rmItemTrans():
    tPage.iList.rmItem()
def editDiscount():
    global w
    w = Toplevel()
    w.title = "Discount"
    frame = Frame(w)

    frame.grid()
    Label(frame,text="Enter the discount percentage:\n\
    (0-100 where 0 is no discount)").grid(column=0,row=0)
    out = StringVar()
    e = Entry(frame,textvariable=out,width=5)
    e.grid(column=0,row=1)
    e.bind("<Return>",chooseDisc)
    e.focus()
def chooseDisc(event):
    global w
    if event.widget.get().isdigit():
        tPage.iList.trans.discountTrans(int(event.widget.get()))
        tPage.iList.updateItems()
        w.destroy()
def resetSearchResult():
    entryVar.set("")
    isbnVar.set("ISBN: ")
    nameVar.set("Title: ")
    priceVar.set("Price: ")
    quantityVar.set("Quantity: ")
class page:
    """ Page class, handles each frame in the notebook
        nFrame: top-level frame
    """
    def __init__(self,parent,searchPane,itemListPane):
        self.nFrame = Frame(parent,height=HEIGHT_MAIN,width=640,padx=10,pady=10)
        ##self.nLabel = Label(nFrame,)
        if searchPane:
            self.center = centerPanel(self.nFrame,entryVar,isbnVar,nameVar,priceVar,quantityVar)
            self.center.frame.grid(column=1,row=0,rowspan=5,padx=5)
        if itemListPane:
            self.iList = itemList(self.nFrame)
            self.iList.frame.grid(column=2,row=0)
class centerPanel:
    def __init__(self,parent,varEntry,varISBN,varNAME,varPRICE,varQUAN):
        """ Frame for the search interface.
        Parameters: parent object,
        """
        self.frame = Frame(parent,height=HEIGHT_MAIN,width=400,bg="white")
        self.isbn = Label(self.frame,textvariable=varISBN,anchor="w",
        height=HEIGHT_CENTER,width=WIDTH_CENTER).grid(column=0,row=0,sticky="ew")
        self.name = Label(self.frame,textvariable=varNAME,anchor="w",
        height=HEIGHT_CENTER,width=WIDTH_CENTER).grid(column=0,row=1,sticky="ew")
        self.price = Label(self.frame,textvariable=varPRICE,anchor="w",
        height=HEIGHT_CENTER,width=WIDTH_CENTER).grid(column=0,row=2,sticky="ew")
        self.quantity = Label(self.frame,textvariable=varQUAN,anchor="w",
        height=HEIGHT_CENTER,width=WIDTH_CENTER).grid(column=0,row=3,sticky="ew")
        self.entry = Entry(self.frame,textvariable=varEntry,
        width=WIDTH_CENTER)
        self.entry.grid(column=0,row=4,sticky="ew")
        self.entry.bind_all("<Return>",searchKey)
        self.entry.bind_all("<Control-s>",searchKey)
        self.entry.bind_all("<Escape>",self.clearEntry)
        self.entry.bind_all("<Control-a>",addKey)
        self.entry.bind_all("<Control-r>",rmKey)
        self.entry.bind_all("<Control-d>",discKey)
        self.entry.bind_all("<Control-c>",confirmKey)
        ##self.entry.bind_all("<uparrow>",navUp)
        ##self.entry.bind_all("<downarrow>",navDown)
    def clearEntry(self,event):
        entryVar.set("")
class itemList:
    """ GUI for the right side menu
    """
    def __init__(self,parent):
        self.frame = Frame(parent,bg=COL_TITLE)
        self.frame.grid(rowspan=6)
        self.trans = transaction()
        self.items = []
        ## Title and separator
        Label(self.frame,text="Item",bg=COL_TITLE).grid(column=0,row=0)
        Label(self.frame,text="Price",anchor="w",bg=COL_TITLE).grid(column=2,
        row=0,sticky="w")
        ## item list
        self.lFrame = Frame(self.frame,bg=COL_TITLE)
        self.lFrame.grid(column=0,row=1,columnspan=3)
        self.listVar = StringVar(value=self.items)
        self.lBox = Listbox(self.lFrame,listvariable=self.listVar,width=LEN_ITEM,font=("TkFixedFont",12),height=6)
        self.lBox.grid(column=0,row=0)
        self.lFrame.grid_columnconfigure(0, weight=1)
        self.lFrame.grid_rowconfigure(0, weight=1)
        ## Scrollbar
        self.sBar = Scrollbar(self.lFrame,orient=VERTICAL,
        command=self.lBox.yview)
        self.lBox.configure(yscrollcommand=self.sBar.set)
        self.sBar.grid(column=1,row=0,sticky="ns")
        ## Bottom items
        self.taxVar = StringVar(value="$0.00")
        self.totalVar = StringVar(value="$0.00")
        self.discVar = StringVar(value="-")

        Label(self.frame,text="Discount:",anchor="w",bg=COL_DARK).grid(column=0,
        row=3,sticky="ew")
        self.totalLabel = Label(self.frame,textvariable=self.discVar,anchor="e",
        bg=COL_DARK).grid(column=1,row=3,columnspan=3,sticky="ew")

        Label(self.frame,text="Tax:",anchor="w",bg=COL_DARK).grid(column=0,row=4
        ,sticky="ew")
        self.taxLabel = Label(self.frame,textvariable=self.taxVar,anchor="e",
        bg=COL_DARK).grid(column=1,row=4,columnspan=2,sticky="ew")

        Label(self.frame,text="Total:",anchor="w",bg=COL_DARK).grid(column=0,
        row=5,sticky="ew")
        self.totalLabel = Label(self.frame,textvariable=self.totalVar,anchor="e",
        bg=COL_DARK).grid(column=1,row=5,columnspan=3,sticky="ew")

        self.confirm = Button(self.frame,text="Confirm",command=self.confirmButton,underline=0,bg=COL_CONFIRM)
        self.confirm.grid(column=0,row=6 ,columnspan=3,sticky="nesw")
    def confirmButton(self):
        ## Export receipt
        file = open("receipt.txt","w")
        l = []
        file.write("RECORD OF TRANSACTION\n" + "-" *30 + "\n")
        ## Write items
        for item in self.trans.getTrans():
            num = priceToString(item[1])
            l.append(item[0] + (" " *(LEN_ITEM - (len(item[0]) + len(num)))) + num)
        for item in l:
            file.write(item + "\n")
        ## Write totals
        output = "-" *30 + "\n"
        d = str(100 - (int(self.trans.getDiscount()*100)))
        tax = priceToString(self.trans.getTax())
        total = priceToString(self.trans.getTotal())
        output = output + "DISCOUNT" + (" " * (LEN_ITEM - (9+len(d))) ) + d + "%\n"
        output = output + "TAX" + (" " * (LEN_ITEM - (3+len(tax))) ) + tax + "\n"
        output = output + "TOTAL" + (" " * (LEN_ITEM - (5+len(total))) ) + total + "\n"
        file.write(output)
        file.close()
        ## Reset transaction
        self.items = []
        self.trans = transaction()
        resetSearchResult()
        self.updateItems()
    def addItemInt(self,name,cents):
        """ Adds an item to the list box.
        name: the name of the item as a string
        price: the price of the item in cents
        """
        string = name
        num = priceToString(cents)
        self.trans.addToTrans(name,cents)
        ## Add spacing
        ##string = string + " " * 2*(LEN_ITEM - (len(string) + len(num))) + num
        ##self.items.append(string)
        self.updateItems()
    def rmItem(self):
        if len(self.lBox.curselection()) > 0:
            self.trans.removeFromTrans(self.lBox.curselection()[0])
            self.updateItems()
    def updateItems(self):
        l = []
        for item in self.trans.getTrans():
            num = priceToString(item[1])
            l.append(item[0] + (" " * 2 *(LEN_ITEM - (len(item[0]) + len(num)))) + num)
        self.listVar.set(l)
        d = 100 - (int(self.trans.getDiscount()*100))
        if d != 0:
            self.discVar.set( str(d) + "%")
        else:
            self.discVar.set("-")
        self.taxVar.set(priceToString(self.trans.getTax()))
        self.totalVar.set(priceToString(self.trans.getTotal()))
## Main window
master = Tk()
master.title("Point of Sales")
mainFrame = Frame(master)
mainFrame.grid()
mainFrame.bind_all("<Control-F1>",resetAll)
note = ttk.Notebook(mainFrame)
note.grid(column=0,row=0)
## global tkinter variables
entryVar = StringVar()
isbnVar = StringVar(value="ISBN: ")
nameVar = StringVar(value="Title: ")
priceVar = StringVar(value="Price: ")
quantityVar = StringVar(value="Quantity: ")

itemName = None
itemPrice = None

tPage = page(note,True,True)
##iPage = page(note,True,False)
##rPage = page(note,True,True)

note.add(tPage.nFrame,text="Transactions")
##note.add(iPage.nFrame,text="Inventory")
##note.add(rPage.nFrame,text="Returns")
actionLabel = Label(tPage.nFrame,text="Actions",width=WIDTH_SIDE_BUTTON,height=5,
        relief="raised",bg=COL_TITLE)
actionLabel.grid(row=0,column=0,sticky="nsew")
tAddButton = Button(tPage.nFrame,text="Add item to\nTransaction",width=WIDTH_SIDE_BUTTON,command=addItemTrans,
        underline=0,height=HEIGHT_SIDE_BUTTON,bg=COL_BUTTON)
tAddButton.grid(row=1,column=0)
tRmButton = Button(tPage.nFrame,text="Remove item from\nTransaction",width=WIDTH_SIDE_BUTTON,command=rmItemTrans,
        underline=0,height=HEIGHT_SIDE_BUTTON,bg=COL_BUTTON)
tRmButton.grid(row=2,column=0)
Button(tPage.nFrame,text="Discount\n Transaction",width=WIDTH_SIDE_BUTTON,command=editDiscount,
        underline=0,height=HEIGHT_SIDE_BUTTON,bg=COL_BUTTON).grid(row=3,column=0)
Button(tPage.nFrame,text="Search by\nISBN or name",width=WIDTH_SIDE_BUTTON,command=searchButton,
        underline=0,height=HEIGHT_SIDE_BUTTON,bg=COL_BUTTON).grid(row=4,column=0,sticky="s")

master.mainloop()
