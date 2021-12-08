#Bianca Nelson
#10 Feb 2021
#CS361
#Sprint 3

import tkinter as tk
import popGenMain
import pika
import threading
import json


window = tk.Tk()
window.title("Population Generator")
window.geometry("1000x1000")

#set up for rabbitMQ
url = 'amqps://ihxxgxga:MCHwDogOGrdLZrIseSj5YEmMS2_rWfLi@grouse.rmq.cloudamqp.com/ihxxgxga'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='Generator2')

options_state = ["Alaska", "Alabama", "Arkansas", "Arizona", "California",
                 "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida",
                 "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas",
                 "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
                 "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota",
                 "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio",
                 "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
                 "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont",
                 "Washington", "Wisconsin", "West Virginia", "Wyoming"]


def callback(ch, method, properties, body):
    """
    Get's info from Life Generator
    """
    print("[x] Received %r" %(body))
    body = str(body, 'utf-8')
    print(body)
    if len(body) == 2: #if the length is two then the lifeGen program is requesting info
        sendBack(body)
    elif body[:13] == "No Categories": #prints to GUI that no category has been found
        noCategories(body)
    else: #prints results GUI
        body = json.loads(body)
        print(body)
        frameResults(body, 1)


def consumingWait():
    """
    Thread that allows program to continue listening for messages in the background
    """
    channel.basic_consume(queue="Generator2", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()



def sendBack(body):
    """
    Send population data to the life generator
    :param body: a string consisting of one letter and 1 number ex: "M6"
    :return: returns findings from US Census website to the life Generator
    """
    #body = str(body, "utf-8")
    state_letter = body[0]
    pop_num = body[1]     # Maybe we can pick a number from the middle of the total population instead of the first number?
    findpop = [["input_year", "input_name"]]
    searchState=[] #place holder for the year and state

    for year in range(2005, 2019): #appends year to searchState
        year = str(year)
        if year[-1] == pop_num:
            searchState.append(year)
            break
    for state in range(0, len(options_state)): #appends state name to searchState
        if options_state[state][0].lower() == state_letter.lower():
            searchState.append(options_state[state])
            break

    findpop.append(searchState)
    if len(findpop[1]) == 1: #if letter given doesn't have a matching state ex: B there are no states that start with B
        channel.basic_publish(exchange='', routing_key="Generator",
                              body="No states with the letter " + state_letter + " were found")
    else: #send population results to lifeGen
        censusResults = popGenMain.getData(findpop)
        censusResults = json.dumps(censusResults)
        channel.basic_publish(exchange='', routing_key="Generator", body=censusResults)
        print(censusResults)

def noCategories(body):
    """Displays the message 'No Categories with the letter ____ were found'
    """
    clear_results()
    message = tk.Label(resultsFrame, text=body)
    message.grid(row=0, column=0)



#sendBack("A6")




x = threading.Thread(target=consumingWait)
x.start()

#event handlers
def searchClick():
    """
    This function is triggered by the search button and it uses the US Census API to generate the population
    :return: Displays state's population in the GUI
    """
    findPop = [["input_year", "input_name"], [years.get(), states.get()]] #holds the current state
    censusResults = popGenMain.getData(findPop) #gets the population
    frameResults(censusResults, 0) #places data in the frame


def lifeGenClick():
#     pass
    clear_results()
    findPop = [["input_year", "input_name"], [years.get(), states.get()]]  # holds the current state
    censusResults = popGenMain.getData(findPop)  # gets the population
    firstLetter = censusResults[1][1][0]
    toyAmount = censusResults[1][2][0]
    print(firstLetter)
    print(toyAmount)
    channel.basic_publish(exchange='', routing_key="Generator", body=firstLetter+toyAmount)
    print("message Sent lifeGenclick")


def frameResults(aList, num):
    """
    Places the states name, year, and population into the GUI
    :param aList: List of data that needs to be placed in the GUI
    :return: Displays state, name, and year in the GUI
    """
    if num == 0:
        # creates labels for the headers
        input_year = tk.Label(resultsFrame, text="Year")
        input_state = tk.Label(resultsFrame, text="State")
        popSize = tk.Label(resultsFrame, text="Population")
    if num == 1:
        input_year = tk.Label(resultsFrame, text="Product Name")
        input_state = tk.Label(resultsFrame, text="Number of Reviews")
        popSize = tk.Label(resultsFrame, text="Average Rating")

    #displays the headers
    input_year.grid(row=0, column=0)
    input_state.grid(row=0, column=1)
    popSize.grid(row=0, column=2)


    #displays population results
    for row in range(1, len(aList)):
        yearResults = tk.Label(resultsFrame, text=aList[row][0])
        stateResults = tk.Label(resultsFrame, text=aList[row][1])
        popResults = tk.Label(resultsFrame, text=aList[row][2])

        yearResults.grid(row=row, column=0)
        stateResults.grid(row=row, column=1)
        popResults.grid(row=row, column=2)

    #exportButton = tk.Button(resultsFrame, text="Export to .csv file")
    # exportButton.grid(row=len(aList)+1, column=0, sticky="E", pady=15, columnspan=5)






#create frame
searchFrame = tk.Frame(window)

#labels for state and year
lblTitle = tk.Label(searchFrame, text="Population Generator by Bianca Nelson", font=("Arial Bold", 16))
lblState = tk.Label(searchFrame, text="State: ")
lblYear = tk.Label(searchFrame, text="Year: ")


#dropdowns
# options_state = ["Alaska", "Alabama", "Arkansas", "Arizona", "California",
#                  "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida",
#                  "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas",
#                  "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan",
#                  "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota",
#                  "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio",
#                  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
#                  "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont",
#                  "Washington", "Wisconsin", "West Virginia", "Wyoming"]
states = tk.StringVar()
states.set(options_state[0])
drop_states = tk.OptionMenu(searchFrame, states, *options_state)

options_year = [] #dropdown for the years
i = 2005
while i <= 2019: #populate the year list w/every year
    options_year.append(i)
    i += 1

years = tk.StringVar()
years.set(options_year[0])
drop_years = tk.OptionMenu(searchFrame, years, *options_year)

#buttons
searchButton = tk.Button(searchFrame, text="Search", command=searchClick)
lifeGenButton = tk.Button(searchFrame, text="Send to Life Gen", command=lifeGenClick)
#csvButton = tk.Button(searchFrame, text="Upload .csv file")


#places all relevant info in in searchFrame
lblTitle.grid(row=0, column=1, columnspan=5, pady=(0, 20))
lblState.grid(row=1, column=0)
drop_states.grid(row=1, column=1, sticky="W")
lblYear.grid(row=1, column=2)
drop_years.grid(row=1, column=3, sticky="W")
searchButton.grid(row=1, column=4, sticky="E")

#csvButton.grid(row=2, column=0, columnspan=5, sticky="E", pady=15)

#*********************************************************************************
#create results frame
resultsFrame = tk.Frame(window)

#resultsFrame Buttons
#exportButton = tk.Button(resultsFrame, text="Export to .csv file")

#places relevant info in searchFrame
#exportButton.grid(row=0, column=0, sticky="E", pady=15)

#add frames to GUI
searchFrame.place(relx=0.5, rely=0.1, anchor="center")
resultsFrame.place(relx=0.5, rely=0.3, anchor="center")



# -----------------------------------------------------------------------------------------------
def clear_results():
    for frame in resultsFrame.winfo_children():
        frame.destroy()
    resultsFrame.grid_forget()


clearButton = tk.Button(searchFrame, text="Clear Results", command=clear_results)
lifeGenButton.grid(row=2, column=3, sticky="W", pady=(20,0))
clearButton.grid(row=1, column=5, sticky="E")
# ----------------------------------------------------------------------------------------------


tk.mainloop()
