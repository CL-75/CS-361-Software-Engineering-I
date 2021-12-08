Population Generator by Bianca Nelson

This is a web app that can return the population of a given state using the desires state's name and year. 
It can also take a .csv file with a list of states and years and generate a file named 'output.csv' which will contain the population for all the states listed. 

How to run the program using the GUI:
1. Place popGenGUI.py, popGenMain.py, requirements.txt, and input.csv in the same directory.
2. Using the command line navigate to the directory where all files are located. 
3. The requests package is needed. To install the dependencies using the following command: 'pip install -r requirements.txt' 
4. Run the program using the following command: 'python popGenMain.py'
5. A GUI will then pop up where you can search for a state's population based on the year. 

How to run the program with an input.csv file:
1. Ensure steps 1-3 from above are completed. 
2. Run the program using the following command: 'python popGenMain.py input.csv'
3. A new file will be created within the directory named 'output.csv' is will contain the population for all the states listed in 'input.csv'

