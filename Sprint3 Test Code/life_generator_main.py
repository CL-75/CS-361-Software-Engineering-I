# Casey Levy
# CS 361 - Sprint 3 Assignment
# Creating a working version of Life Generator app
# License: https://creativecommons.org/licenses/by-sa/4.0/
# Toy Data gathered from: https://www.kaggle.com/PromptCloudHQ/toy-products-on-amazon
# Some code inspired by https://www.youtube.com/watch?v=VaY7xa8wiIU&t=1038s
# Toys class help from https://docs.python.org/3/howto/sorting.html

from tkinter import *
from tkinter import ttk, filedialog, messagebox
from operator import itemgetter, attrgetter
import tkinter as tk


import csv
import os


# Grabbing all column info (categories)
filepath = "C:/Users/spike/OneDrive - Oregon State University/CS 361 - Software Engineering I/Module 3 - Architecture and Diagramming/Sprint 3 Code/amazon_co-ecommerce_sample.csv"
File = open(filepath, encoding="utf-8")
Reader = csv.reader(File)
Data = list(Reader)

category_list = []
for i in list(range(0, len(Data))):
    category_list.append(Data[i][8])


# ------- Functions -----------

# Function to sort columns based on name
def sort_columns(col_header, data):
    if col_header == "amazon_category_and_sub_category":
        data.split(">")
    if col_header == "average_review_rating":
        return float(data[0])
    if col_header == "product_name" or "uniq_id":
        return data
    if col_header == "number_of_reviews":
        return int(data.replace(",", "0"))


# Function to read sorted column data
def sorted_column_reader(filepath):
    with open(filepath, "r") as file:
        input = csv.reader(file)
        next(input)
        file_content = next(input)
        file_content[2] = int(file_content[2])
    return file_content


# Function to read content from given amazon .csv file, based on file's column headers
def reader(filepath):
    category_list = []
    csv_columns = [
        "amazon_category_and_sub_category",
        "average_review_rating",
        "product_name",
        "uniq_id",
        "number_of_reviews",
    ]

    with open(filepath, "r") as file:
        Reader = csv.reader(file)
        col_headers = next(Reader)
        for i in Reader:
            categories = {}
            for x, y in enumerate(col_headers):
                if y in csv_columns:
                    categories[y] = sort_columns(y, i[x])
            category_list.append(categories)
        return category_list



# Function to write data to file
def write_file(col_header, content, path):
    with open(path, "w") as file:
        output = csv.writer(file)
        output.writerow(col_header)
        for i in content:
            output.writerow([str(j) for j in i])


# Function to download given results to .csv file
"""
def download_file():
    new_file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Download CSV", filetypes=(("CSV File", "*.csv"), ("All Files", "*.*")))
    with open(new_file, "w") as exported_file:
        written_file = csv.writer(exported_file, delimiter=",")
        for x in 
            written_file.writerow(x)

    messagebox.showinfo("Life Generator", "Download Successful!")
"""

# Toys class for easier data retrieval/usage
class Toys:
    def __init__(self, content):
        self.__content = content
        self.__file_content = content
        self.__toy_categories = sorted({
            toy
            for i in self.__file_content
            for toy in i["amazon_category_and_sub_category"]
            if toy
        })

    # Function to sort content by category name
    def category_sort(self, toy_category):
        self.__file_content = [i for i in self.__file_content if toy_category in i["amazon_category_and_sub_category"]]

    # "top" algorithm for top X toys for category Y
    # Code inspired from https://docs.python.org/3/howto/sorting.html
    def rating_sort(self, rating):
        self.rating_sort_helper((("number_of_reviews", True), ("uniq_id", False)))
        self.__file_content = self.__file_content[:rating*10]
        self.rating_sort_helper((("average_review_rating", True), ("uniq_id", False)))
        self.__file_content = self.__file_content[:rating]

    def rating_sort_helper(self, sort):
        for x, y in reversed(sort):
            self.__file_content.sort(key=itemgetter(x), reverse=y)
        return self

    def display_results(self, columns):
        return [[i[column] for column in columns] for i in self.__file_content]


# Class to access main program functions and run program
class Main():
    def __init__(self, csv_file, master):
        self.master = master
        self.total_results = []
        self.model = Toys(reader(csv_file))
        self.results = tk.StringVar(self)
        self.toy_category = tk.StringVar(self)

    # Function to get results of file content based on user input
    def generate(self):
        toy_category = self.toy_category.get()
        results = int(self.results.get())
        headers = ["product_name", "average_review_rating", "number_of_reviews"]
        self.model.category_sort(toy_category)
        self.model.rating_sort(results)
        display = self.model.display_results(headers)

        result_headers = [
            "input_item_type",
            "input_item_category",
            "input_number_to_generate",
            "output_item_name",
            "output_item_rating",
            "output_item_num_reviews"
        ]

        output = [["toys", toy_category, results] + i for i in display]
        write_file(result_headers, output, "output.csv")


# GUI Window Specs
window = tk.Tk()
window.title("Life Generator")
window.geometry('800x750')
frame = tk.Frame(master=window, width=100, height=100, bg="DarkOrange2")
frame2 = tk.Frame(master=window, width=700, height=700, highlightbackground="DarkOrange2", highlightthickness=2)











# Various Greetings/Messages

greeting1 = tk.Label(master=frame, text="Welcome to Life Generator", font="bold")
greeting2 = tk.Label(master=frame, text="Search Amazon's Most Popular Toys!", font="bold")

generate_button = tk.Button(master=frame, text="Generate!", width=10, height=1, font="bold", bg="green4", fg="black", relief=RAISED)
download_button = tk.Button(master=frame2, text="Download Results as CSV", width=30, height=1, bg="green4", fg="black", relief=RAISED)

category_label = tk.Label(master=frame, text="Please Select a Toy Category:")
category_menu = ttk.Combobox(frame, width=30, value=category_list)



results_label = tk.Label(master=frame, text="Please Enter the Number of Results You Would Like Displayed: ")
results_entry = tk.Entry(master=frame, width=10)

new_line = tk.Label(master=frame, text=" ", bg="DarkOrange2")



# GUI Implementation
frame.pack()
greeting1.pack()
greeting2.pack()
new_line.pack()
category_label.pack()
category_menu.pack(padx=10, pady=15)
results_label.pack()
results_entry.pack(padx=10, pady=15)
new_line.pack()
generate_button.pack()

download_button.place(relwidth=.1, relheight=.1)
frame2.pack(pady=20)


window.mainloop()




