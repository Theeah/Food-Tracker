#Global Variables
foodList=["00"] #Needs to be list of food, not list of IDs

class food:
    def __init__(self,foodID,foodType,open,useBy,usagesLeft):
        self.ID=foodID
        self.type=foodType
        self.open=open
        self.useByDate=useBy
        self.usagesLeft=usagesLeft

def generateID(array):
    id="-1"
    index=len(foodList)
    try:
        id=int(array[index-1])+1
        if(id<10):
            id=str(id)
            id=("0"+id)
        else:
            id=str(id)
    except:
        id="00"
    return id

def inpUseDate(): #Used when adding an item. Gets the user to input the useByDate.
    print("What is the use by date of the food item?")
    useByDate=input() #Make sensible to input.
    #Validation
    return useByDate

def inpUsages(): #Used when adding an item. Gets the user to input the number of usages.
    print("How many meals will the item last?")
    usages=input()
    try:
        usages=int(usages)
    except:
        print("Please input a whole number.")
        usages=-1
    return usages

def inpType(): #Used when adding an item. Gets the user to choose which type of food the new item is.
    print("What type of item would you like to add?")
    print("[1] Protein")
    print("[2] Vegetables")
    print("[3] Cheese")
    choice=input()
    foodType=""
    if(choice=="1"):
        foodType="Protein"
    elif(choice=="2"):
        foodType="Vegetables"
    elif(choice=="3"):
        foodType="Cheese"
    else:
        print("Please input the number indicating the type of food.")
        foodType="fail"
    return foodType

def addItemChat(): #Activates when the user decides to add a new food item.
    type=inpType()
    while(type=="fail"):
        type=inpType()
    
    useByDate=inpUseDate()

    usages=inpUsages()
    while(usages==-1):
        usages=inpUsages()
    
    
    id=generateID(foodList)
    
    food1=food(id,type,False,useByDate,usages)
    print(food1.ID,food1.type,food1.useByDate,food1.open,food1.usagesLeft)
        
def chatBotStart(): #'Main Menu' of the chat bot. Decide what action to take.
    print("What action would you like to take?")
    print("[1] Add a food item")
    #Other options here.
    
    option=input()
    if(option=="1"):
        addItemChat()
    else:
        print("Sorry, command not found.")
    
    print("Would you like to perform another action?")
    print("[1] Yes")
    print("[2] No")
    choice=input()
    if(choice=="1"):
        chatBotStart()
    elif(choice=="2"):
        print("Thank you for using foodTracker.")
    else:
        print("Command not found. Ending chat.")

#Start
chatBotStart()