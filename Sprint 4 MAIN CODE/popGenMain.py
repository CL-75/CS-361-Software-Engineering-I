#Bianca Nelson
#10 Feb 2021
#CS361
#Sprint 3


import sys
import csv
import requests


def parseCSV(CSVfile):
    """
    parses a .csv file and generates a file name output.csv containing the population of all cities listed in the first
    .csv file
    :param CSVfile: this is a command line file which contains a states name and the year for which the population
        should be generated
    :return: generates an output.csv with the corresponding population
    """

    findCensus = []
    with open(CSVfile) as f:
        reader = csv.reader(f)
        for row in reader:
            findCensus.append(row)
    censusResults = getData(findCensus) #gets the population
    exportCSV(censusResults) #writes the output.csv file


def exportCSV(dataList):
    '''
    Creates the output.csv file after the population has already be recieved.
    :param dataList: This is a list of the states, years, and their respective locations
    :return: a file named output.csv is generated using the info from dataList
    '''

    newFile = open("output.csv", "w")
    with newFile:
        writer = csv.writer(newFile)
        writer.writerows(dataList)


def getData(Alist):
    """
    This uses the US Census API to retrieve the population of the desired location
    :param Alist: a list of states and years
    :return: a list of states, years, and the population
    """
    allResponses = [["input_year", "input_state", "output_population_size"]] #headers

    # for loop iterates through the Alist to find the population of each state one at a time.
    for x in range(1, len(Alist)):
        year = Alist[x][0]
        fipCode = getFips(Alist[x][1]) #takes the state's name or abbreviation and get the Fip code

        myKey = "6c8f8c666a1365fea65a487b79a139a8e2365457"
        baseURL = "https://api.census.gov/data/"
        dataset = "/acs/acs1?get=NAME,"
        variables = "B01003_001E"
        url = str(baseURL + year + dataset + variables + "&for=state:" + fipCode + "&key=" + myKey)
        response = requests.get(url)
        data = response.json()
        #popComma = "{:,}".format(int(data[1][1]))
        allResponses.append([year, data[1][0], data[1][1]])

    return allResponses



def getFips(state):
    """
    takes the state's name or abbreviation and get the Fip code
    :param state: the full name or abbreviation of a state
    :return: the fip code of the given state
    """
    allStates = {
        "name": ["alaska", "alabama", "arkansas", "arizona", "california",
                 "colorado", "connecticut", "district of columbia", "delaware", "florida",
                 "georgia", "hawaii", "iowa", "idaho", "illinois", "indiana", "kansas",
                 "kentucky", "louisiana", "massachusetts", "maryland", "maine", "michigan",
                 "minnesota", "missouri", "mississippi", "montana", "north carolina", "north dakota",
                 "nebraska", "new hampshire", "new jersey", "new mexico", "nevada", "new york", "ohio",
                 "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
                 "south dakota", "tennessee", "texas", "utah", "virginia", "vermont",
                 "washington", "wisconsin", "west virginia", "wyoming"],
        "abbreviation": ["ak", "al", "ar", "az", "ca",
                 "co", "ct", "dc", "de", "fl",
                 "ga", "hi", "ia", "id", "il", "in", "ks",
                 "ky", "la", "ma", "md", "me", "mi",
                 "mn", "mo", "ms", "mt", "nc", "nd",
                 "ne", "nh", "nj", "nm", "nv", "ny", "oh",
                 "ok", "or", "pa", "ri", "sc",
                 "sd", "tn", "tx", "ut", "va", "vt",
                 "wa", "wi", "wv", "wy"],
        "fips": ["02", "01", "05", "04", "06",
                 "08", "09", "11", "10", "12",
                 "13", "15", "19", "16", "17", "18", "20",
                 "21", "22", "25", "24", "23", "26",
                 "27", "29", "28", "30", "37", "38",
                 "31", "33", "34", "35", "31", "36", "39",
                 "40", "41", "42", "44", "45",
                 "46", "47", "48", "49", "51", "50",
                 "53", "55", "54", "56"]
    }
    if len(state) > 2: #full state name
        stateIndex = allStates["name"].index(state.lower())
    else: #abbreviation
        stateIndex = allStates["abbreviation"].index(state.lower())
    fipscode = allStates["fips"][stateIndex]
    return fipscode



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if len(sys.argv) > 1:
        parseCSV(sys.argv[1])
    else:
        import popGenGUI


    # else:
    #     main()