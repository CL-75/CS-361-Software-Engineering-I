import csv

filepath = "C:/Users/Yesac/OneDrive - Oregon State University/CS 361 - Software Engineering I/Module 3 - Architecture and Diagramming/Sprint 3 Code/amazon_co-ecommerce_sample.csv"
File = open(filepath, encoding="utf-8")
Reader = csv.reader(File)
Data = list(Reader)

# Grabbing all column info (categories)
for i in list(range(0, len(Data))):
    print(Data[i][8])