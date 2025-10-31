class food:
    def __init__(self,foodID,foodType,open,useBy,usagesLeft):
        self.ID=foodID
        self.type=foodType
        self.open=open
        self.useByDate=useBy
        self.usagesLeft=usagesLeft

def generate_ID(foodList): #Generates a new ID based on the ID of the last item in the list
    id="-1"

    try:
        index=len(foodList)
        if(index==0):
            id="00"
        else:
            lastItem=foodList[index-1]
            lastItemList=lastItem.split(',')
            id=int(lastItemList[0])+1


            if(id<10):
                id=str(id)
                id=("0"+id)
            else:
                id=str(id)

    except:
        raise Exception

    return id

def inp_use_date(): #Used when adding an item. Gets the user to input the useByDate.
    print("What is the use by date of the food item?")
    useByDate=input() #Make sensible to input.
    #Validation
    return useByDate

def inp_usages(): #Used when adding an item. Gets the user to input the number of usages.
    print("How many meals will the item last?")
    usages=input()
    try:
        usages=int(usages)
    except:
        print("Please input a whole number.")
        usages=-1
    return usages

def inp_type(): #Used when adding an item. Gets the user to choose which type of food the new item is.
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

def food_shopping_calc_chat(foodList): #Calculates the number of full meals remaining and what is leftover after that number of meals has been consumed.
    protein=0
    cheese=0
    veg=0
    for foodItem in foodList:
        if(foodItem.type=="Protein"):
            protein=protein+foodItem.usages
        elif(foodItem.type=="Vegetables"):
            veg=veg+foodItem.usages
        else:
            cheese=cheese+foodItem.usages
    
    lowest=""
    if(protein<cheese):
        if(protein<veg):
            lowest=protein
        else:
            lowest=veg
    else:
        if(cheese<veg):
            lowest=cheese
        else:
            lowest=veg
    
    print(f"You have {lowest} full meals")
    if((protein-lowest)>0):
        print(f"You have {(protein-lowest)} meals worth of protein leftover.")
    if((veg-lowest)>0):
        print(f"You have {veg-lowest} meals worth of vegetables leftover.")
    if((cheese-lowest)>0):
        print(f"You have {cheese-lowest} meals worth of cheese leftover.")
    
    print("Good luck with your shopping trip!")

def add_item_chat(foodList): #Activates when the user decides to add a new food item.
    type=inp_type()
    while(type=="fail"): #Repeat if they input a non-option
        type=inp_type()
    
    useByDate=inp_use_date()

    usages=inp_usages() #Repeat if they input a non-integer
    while(usages==-1):
        usages=inp_usages()
    
    id=generate_ID(foodList)
    
    foodString=(id+","+type+",False,"+useByDate+","+str(usages))

    foodList.append(foodString)
    return foodList

def decrease_useBy(useByDate):
    import datetime
    todayDateTime=datetime.datetime.now()
    daysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31]
    splitDate=[todayDateTime.strftime("%d"),todayDateTime.strftime("%m"),todayDateTime.strftime("%y")]
    splitUseBy=useByDate.split("/")

    decrease=False
    if(int(splitUseBy[1])>int(splitDate[1])):
        decrease=True
    else:
        if(int(splitUseBy[0])>int(splitDate[0])):
            decrease=True
    
    if(decrease==True): #If useBy is less than 3 days from now, the useBy date should not be increased.
        splitDate[0]=int(splitDate[0])+3
        print(splitDate[0])
        if daysInMonth[int(splitDate[1])]<splitDate[0]: #Sorry for this monster. Just checks if we have gone over the number of days for this month
            days=splitDate[0]-daysInMonth[int(splitDate[1])-1] #days is how many days it took to get to the end of the month.
            splitDate[1]=int(splitDate[1])+1
            splitDate[0]=days
            if(splitDate[1]>12): #If new year
                splitDate[1]=1
                splitDate[2]=int(splitDate[2])+1
    
    return str(splitDate[0])+"/"+str(splitDate[1])+"/"+str(splitDate[2])

def collate_item(itemList):
    stringified=""
    for item in itemList:
        stringified=stringified+str(item)+","
    
    return stringified

def decrease_usages(foodList,itemList,itemPos):
    itemList[4]=int(itemList[4])-1
    if(itemList[2]=="False"):
        itemList[2]=True
        itemList[3]=decrease_useBy(itemList[3])

    if(itemList[4]==0):
        foodList.pop(itemPos)
    else:
        foodList[itemPos]=collate_item(itemList)
    
    return foodList

def decrease_usages_chat(foodList):
    print(foodList)
    print()
    if(len(foodList)>0):
        print("Please find and type the ID of the item you have used.")
        itemID=input()
        selectedItem=""
        for i in range(len(foodList)):
            item=foodList[i]
            itemList=item.split(",")
            if(itemList[0]==itemID):
                selectedItem=item
                print("Would you like to decrease the usages of this item?")
                print("[1] Yes")
                print("[2] No")
                print("[3] Main Menu")
                decision=input()
                if(decision=="1"):
                    foodList=decrease_usages(foodList,itemList,i)
                    print("Change saved.")
                elif(decision=="2"):
                    decrease_usages_chat(foodList)
                elif(decision=="3"):
                    print()
                else:
                    print("Please try again.")
                    decrease_usages_chat(foodList)

        if(selectedItem==""): #Activates when an invalid ID was input.
            print("Sorry, that item was not found.")
            decrease_usages_chat(foodList)
    else:
        print("There is no food in the fridge.")

    return foodList

def end_chat(foodList): #After an action is performed, will see if the user has finished with the foodTracker or not.
    print("Would you like to perform another action?")
    print("[1] Yes")
    print("[2] No")
    choice=input()
    if(choice=="1"):
        chat_bot_start(foodList)
    elif(choice=="2"):
        print("Thank you for using foodTracker.")
    else:
        print("Command not found. Ending chat.")

def chat_bot_start(foodList): #'Main Menu' of the chat bot. Decide what action to take.
    print("---------------------------------------")
    print("What action would you like to take?")
    print("[1] Add a food item")
    print("[2] Decrease the usages on a food item")
    print("[3] Generate food shopping information")
    print("[4] Exit")
    print("---------------------------------------")
    
    option=input()
    if(option=="1"):
        foodList=add_item_chat(foodList)
        end_chat(foodList)
    elif(option=="2"):
        foodList=decrease_usages_chat(foodList)
        end_chat(foodList)
    elif(option=="3"):
        food_shopping_calc_chat(foodList)
        end_chat(foodList)
    elif(option=="4"):
        print("Thank you for using foodTracker.") #Ends chat. end_chat() is not called here because then it would double check if they want to exit.
    else:
        print("Sorry, command not found.")
        end_chat(foodList)
    
def start(): #Initialises foodList and starts the chat bot for main menu.
    foodList=[]
    chat_bot_start(foodList)

#Start
start()