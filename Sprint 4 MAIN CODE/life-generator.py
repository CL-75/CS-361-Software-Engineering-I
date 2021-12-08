# Casey Levy
# CS 361 - Sprint 4 Assignment
# Creating a working version of Life Generator app and communicating with another microservice
# License: https://creativecommons.org/licenses/by-sa/4.0/
# Toy Data gathered from: https://www.kaggle.com/PromptCloudHQ/toy-products-on-amazon
# Some code inspired by https://www.youtube.com/watch?v=VaY7xa8wiIU&t=1038s
# Panda Library documentation used, cites made within program where needed

from tkinter import *
from tkinter import ttk
from os import path
import tkinter as tk
import pandas as pd
import csv
import pika
import threading
import json



# -------- RabbitMQ Setup -------------------
#set up for rabbitMQ
url = 'amqps://ihxxgxga:MCHwDogOGrdLZrIseSj5YEmMS2_rWfLi@grouse.rmq.cloudamqp.com/ihxxgxga'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='Generator')


# -------- RabbitMQ Consuming ---------------
# Get's info from Population Generator
def callback(ch, method, properties, body):
    print("[x] Life Gen Received from Pop Gen %r" %(body))
    body = str(body, 'utf-8')
    print(body)
    if len(body) == 2:   # if the length is two then the popGen program is requesting info
        sendBack(body)
    elif body[:9] == "No states":
        noStates()
    else:    # if a state population was found
        body = json.loads(body)
        print(body)
        display_box.insert("1.0", body[1][2])
        display_box.insert("1.0", "\n")
        display_box.insert("1.0", body[1][1])


# This function is listening for the Population Generator to send a message
def consumingWait():
    channel.basic_consume(queue="Generator", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


# This is a function that will take the body and retrieve info from the amazon.csv file
def sendBack(body):
    num_toys = int(body[1])
    first_letter = body[0]
    #this is a list that will hold all the results matching first_letter, it is prefilled with headers
    findCategory=[["product_name", "number_of_reviews", "average_rating"]]
    first_category = None
    count = 0
    with open("amazon_co-ecommerce_sample.csv", "r", encoding="utf8") as file:
        reader = csv.reader(file)
        for row in reader:
            current= row[8]   #index where the category name is found
            if current == "" or count == 0:   #skips header row and any rows where the category name is empty
                count +=1
            elif first_category is None and current.lower()[0] == first_letter.lower():   #finds and assigns a category
                findCategory.append([row[1], row[5], row[7]])
                first_category = row[8]
            elif first_category is not None and current.lower() == first_category.lower():
                findCategory.append([row[1], row[5], row[7]])   #appends product_name, number_of_reviews, and average_review_rating
    if len(findCategory) == 1:   #this will be true if the letter Pop Gen sent has no categories that match it. Ex: Kansas
        message = "No Categories with the letter " + first_letter + " were found"
        publishNow(message)
        print("No categories found")
    else:
        print(findCategory[:num_toys+1])
        sendingBack = json.dumps(findCategory[:num_toys+1])
        publishNow(sendingBack)
        print("SendingBack has replied")


x = threading.Thread(target=consumingWait)
x.start()


#-------------- RabbitMQ sending -----------------
# This function sends messages to the population Generator
def publishNow(message):
    channel.basic_publish(exchange='', routing_key="Generator2", body=message)



# -------- GUI Design Specs -----------------
window = tk.Tk()
window.title("Life Generator")
window.geometry("1000x1000")
display_box = tk.Text(window, width=500, height=50, background="antique white")


# Global variable for list of categories
categories_list = []



canvas = tk.Canvas(window, height=200, width=300)
canvas.place()
category_label = tk.Label(master=window, text="Please Select a Toy Category:")
results_label = tk.Label(master=window, text="Please Enter the Number of Results You Would Like Displayed: ")
greeting1 = tk.Label(master=window, text="Welcome to Life Generator", font="bold")
greeting2 = tk.Label(master=window, text="Search Amazon's Most Popular Toys!", font="bold")
greeting3 = tk.Label(master=window, text="Use the features below to search Amazon's \n most popular toys based on their category.\n")
results_entry = tk.Entry(window, width=10)


# ------------- Functionalities -------------------
# Encoding line required for csv.reader compatibility
with open("amazon_co-ecommerce_sample.csv", "r", encoding="utf8") as file:
    file_reader = csv.reader(file)
    next(file_reader)
    for i in file_reader:
        cat_list = i[8].split(" > ")
        if cat_list[0] not in categories_list:
            categories_list.append(cat_list[0])
    categories_list.sort()



greeting1.pack()
greeting2.pack()
greeting3.pack()
category_label.pack()
categories = StringVar(window)
category_menu = ttk.Combobox(window, width=30, values=categories_list)
category_menu.pack(padx=10, pady=15)
category_menu.set("CATEGORIES")
results_label.pack()
canvas.create_window(100, 100, window=results_entry)
results_entry.pack(padx=10, pady=15)


# Utilizing panda to read csv file
# https://pandas.pydata.org/pandas-docs/stable/index.html
def generate():
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html

    display_box.delete("1.0", END)
    num_input = results_entry.get()
    int_input = int(num_input)

    am_file = "amazon_co-ecommerce_sample.csv"
    content = pd.read_csv(am_file, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

    # Panda set_option to set value for dataframe for data output
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.set_option.html?highlight=set_option#pandas.set_option
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("colheader_justify", "left")

    content.head()


    # Sorting values as well as converting to ints
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.startswith.html?highlight=startswith#pandas.Series.str.startswith
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.sort_values.html?highlight=sort_values#pandas.Series.sort_values
    # mergesort chosen as sorting method since documentation tells us "quicksort" is unstable
    option = content[content.amazon_category_and_sub_category.str.startswith(categories.get(), na = False)].copy()
    option["number_of_reviews"] = pd.to_numeric(option["number_of_reviews"], errors="coerce").fillna(0).astype(int)
    option.sort_values(["uniq_id"], ascending = True, inplace = True, kind="mergesort")
    option.sort_values(["number_of_reviews"],ascending = False, inplace = True, kind="mergesort")

    # Sorting/converting cont...
    user_choice = option.head(int_input * 10).copy()      # "top" algorithm
    user_choice["average_review_rating"] = user_choice["average_review_rating"].str[:3].astype(float)
    user_choice.sort_values(["uniq_id"], ascending = True, inplace = True, kind="mergesort")
    user_choice.sort_values(["average_review_rating"], ascending = False, inplace = True, kind="mergesort")
    user_choice["average_review_rating"] = user_choice["average_review_rating"].astype(str) + ' out of 5'
    user_choice.reset_index(drop = True, inplace = True)

    display_box.insert("end-1c", user_choice[["product_name", "number_of_reviews", "average_review_rating"]].head(int_input))


# Function to take input from GUI and send to Pop Gen program
def popGenClick():
    clearResults()
    cats, results = None, None
    cat_get = category_menu.get()
    res_get = results_entry.get()
    cats = cat_get[0]
    results = res_get[0]
    print(cats)
    print(results)
    channel.basic_publish(exchange='', routing_key="Generator2", body=cats+results)
    print("Message Sent popGenClick")


# Function to clear textbox
def clearResults():
    display_box.delete("1.0", END)


# Called if no states exist with the same first letter as toy category
# i.e. No states exist that begin with the letter "B" or "J" if user selects category "Bags" or "Jigsaws and Puzzles"
def noStates():
    clearResults()
    display_box.insert("1.0", "Error: No States Exist That Begin With Same First Letter as the Chosen Toy Category")



generate_button = tk.Button(master=window, text="Generate!", width=10, height=1, font="bold", bg="darkorange2", fg="white", relief=RAISED, command=generate)
generate_button.pack()


# Send to Population Generator Button
popGen_button = tk.Button(master=window, text="Send To Population Gen", width=20, height=1, font="bold", bg="forest green", fg="white", relief=RAISED, command=popGenClick)
clear_button = tk.Button(master=window, text="Clear Results", command=clearResults)
popGen_button.pack(pady=(5,0))
clear_button.pack(pady=(5,0))


display_box.pack(padx=10, pady=10)
window.mainloop()


# ----------------- input/output.csv ----------------------
if path.exists('input.csv'):

    with open("input.csv", "r") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=",")
        next(csv_file)

        for i in file_reader:
            user_selection = i[1]
            num = i[2]

    # More Sorting/Converting
    file = "amazon_co-ecommerce_sample.csv"
    data = pd.read_csv(file, sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
    option_2 = data[data.amazon_category_and_sub_category.str.startswith(user_selection, na = False)].copy()
    option_2["number_of_reviews"] = option_2["number_of_reviews"].str.replace(',', "").fillna(0).astype(int)
    option_2.sort_values(["uniq_id"], ascending=True, inplace = True, kind="mergesort")
    option_2.sort_values(["number_of_reviews"], ascending = False, inplace = True, kind="mergesort")

    user_choice_2 = option_2.head(int(num) * 10).copy()
    user_choice_2["average_review_rating"] = user_choice_2["average_review_rating"].str[:3].astype(float)
    user_choice_2.sort_values(["uniq_id"], ascending = True, inplace = True, kind = "mergesort")
    user_choice_2.sort_values(["average_review_rating"], ascending = False, inplace = True, kind="mergesort")
    user_choice_2["average_review_rating"] = user_choice_2["average_review_rating"].astype(str) + ' out of 5'


    user_results = user_choice_2.head(int(num)).copy()
    final_results = user_results[["product_name", "number_of_reviews", "average_review_rating"]]


    dl_file = {
        "input_item_type" : "toys",
        "input_item_category": user_selection,
        "input_number_to_generate": num,
        "output_item_name": user_results["product_name"],
        "output_item_rating": user_results["average_review_rating"],
        "output_item_num_reviews": user_results["number_of_reviews"]
            }
    res = pd.DataFrame(dl_file)
    res.to_csv("output.csv", header = True, index = False)
