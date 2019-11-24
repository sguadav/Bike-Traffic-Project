import csv
import requests
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


# Get data function, separates the file into each column title
def getData(csvUrl):
    with requests.Session() as s:
        download = s.get(csvUrl)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)

        date = []
        day = []
        highTemp = []
        lowTemp = []
        precipitation = []
        brooklynNum = []
        manhattanNum = []
        williamsburgNum = []
        queensboroNum = []
        totalNum = []
        my_list.pop(0)
        for j in my_list:
            date.append(j[0])
            day.append(j[1])
            highTemp.append(float(j[2]))
            lowTemp.append(float(j[3]))
            tempPrecipitation = re.sub(r", | \(S\)", "", j[4])
            tempPrecipitation2 = re.sub(r"[A-Z]", "0", tempPrecipitation)
            precipitation.append(float(tempPrecipitation2))
            brooklynNum.append(float(j[5].replace(",", "")))
            manhattanNum.append(float(j[6].replace(",", "")))
            williamsburgNum.append(float(j[7].replace(",", "")))
            queensboroNum.append(float(j[8].replace(",", "")))
            totalNum.append(float(j[9].replace(",", "")))
    return date, day, highTemp, lowTemp, precipitation, brooklynNum, manhattanNum, \
           williamsburgNum, queensboroNum, totalNum


def getDictFrequency(Dependent, listTest):
    dictionary = {}
    x = 0
    for dayTest in Dependent:
        if dayTest in dictionary:
            dictionary[dayTest] += int(listTest[x])
        else:
            dictionary[dayTest] = int(listTest[x])
        x += 1
    return dictionary


# Function that creates a 5 normal distributions comparing each bridge plus the total
# to see which bridge contributes more to the total per date(to answer question 1)/day/temp/precipitation
def dateAnalysis(date, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total):
    plt.plot(date, savgol_filter(brooklynNum, len(brooklynNum)-1, 2), label='Brooklyn')
    plt.plot(date, savgol_filter(manhattanNum, len(manhattanNum) - 1, 2), label='Manhattan')
    plt.plot(date, savgol_filter(williamsburgNum, len(williamsburgNum) - 1, 2), label='Williamsburg')
    plt.plot(date, savgol_filter(queensboroNum, len(queensboroNum) - 1, 2), label='Queensboro')
    plt.plot(date, savgol_filter(total, len(total)-1, 2))
    plt.ylabel('Number of Cyclist')
    plt.xlabel('Date')
    plt.title('Number of Cyclist per Date')
    plt.legend(loc='best')
    plt.savefig("date.png")
    plt.show()
    return


def dayAnalysis(day, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total):
    #Brooklyn
    dictBrook = getDictFrequency(day, brooklynNum)
    dayBrook, numCyclistBrook = zip(*sorted(dictBrook.items()))
    plt.plot(dayBrook, numCyclistBrook, label='Brooklyn Bridge')
    #Manhattan
    dictMan = getDictFrequency(day, manhattanNum)
    dayMan, numCyclistMan = zip(*sorted(dictMan.items()))
    plt.plot(dayMan, numCyclistMan, label='Manhattan Bridge')
    #Williamsburg
    dictWill = getDictFrequency(day, williamsburgNum)
    dayWill, numCyclistWill = zip(*sorted(dictWill.items()))
    plt.plot(dayWill, numCyclistWill, label='Williamsburg Bridge')
    #Queensboro
    dictQueens = getDictFrequency(day, queensboroNum)
    dayQueens, numCyclistQueens = zip(*sorted(dictQueens.items()))
    plt.plot(dayQueens, numCyclistQueens, label='Queensboro Bridge')
    #Total
    dictTot = getDictFrequency(day, totalNum)
    dayTot, numCyclistTot = zip(*sorted(dictTot.items()))
    plt.plot(dayTot, numCyclistTot, label='Total')
    plt.ylabel('Number of Cyclist')
    plt.xlabel('Day')
    plt.title('Number of Cyclist per Day')
    plt.legend(loc='best')
    plt.savefig("day.png")
    plt.show()
    return


def tempAnalysis(averageTemp, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total):
    sortaverageTemp, sortbrooklynNum, sortmanhattanNum, sortwilliamsburgNum, sortqueensboroNum, sorttotal = \
        zip(*sorted(zip(averageTemp, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total)))
    plt.plot(sortaverageTemp, savgol_filter(sortbrooklynNum, len(brooklynNum) - 1, 2), label='Brooklyn')
    plt.plot(sortaverageTemp, savgol_filter(sortmanhattanNum, len(manhattanNum) - 1, 2), label='Manhattan')
    plt.plot(sortaverageTemp, savgol_filter(sortwilliamsburgNum, len(williamsburgNum) - 1, 2), label='Williamsburg')
    plt.plot(sortaverageTemp, savgol_filter(sortqueensboroNum, len(queensboroNum) - 1, 2), label='Queensboro')
    plt.plot(sortaverageTemp, savgol_filter(sorttotal, len(total) - 1, 2), label='Total')
    plt.ylabel('Number of Cyclist')
    plt.xlabel('Average Temperature')
    plt.title('Number of Cyclist per Average Temperature')
    plt.legend(loc='best')
    plt.savefig("temperature.png")
    plt.show()
    return


def precipitationAnalysis(precipitation, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total):
    sortprecipitation, sortbrooklynNum, sortmanhattanNum, sortwilliamsburgNum, sortqueensboroNum, sorttotal = \
        zip(*sorted(zip(precipitation, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, total)))
    plt.plot(sortprecipitation, savgol_filter(sortbrooklynNum, len(brooklynNum) - 1, 2), label='Brooklyn')
    plt.plot(sortprecipitation, savgol_filter(sortmanhattanNum, len(manhattanNum) - 1, 2), label='Manhattan')
    plt.plot(sortprecipitation, savgol_filter(sortwilliamsburgNum, len(williamsburgNum) - 1, 2), label='Williamsburg')
    plt.plot(sortprecipitation, savgol_filter(sortqueensboroNum, len(queensboroNum) - 1, 2), label='Queensboro')
    plt.plot(sortprecipitation, savgol_filter(sorttotal, len(total) - 1, 2), label='total')
    plt.ylabel('Number of Cyclist')
    plt.xlabel('Precipitation')
    plt.title('Number of Cyclist per Precipitation')
    plt.legend(loc='best')
    plt.savefig("precipitation.png")
    plt.show()
    return


if __name__ == '__main__':
    csvUrl = 'https://engineering.purdue.edu/~milind/ece20875/2019fall/assignments/project/bike-data.csv'
    # Get data function
    date, day, highTemp, lowTemp, precipitation, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, totalNum = \
        getData(csvUrl)
    dataTemp = np.array([highTemp, lowTemp])
    # Gets the average temperature bewteen low and high
    averageTemp = np.average(dataTemp, axis=0)

    listDescribers = [date, day, averageTemp, precipitation]
    listCyclist = [brooklynNum, manhattanNum, williamsburgNum, queensboroNum]

    # CHANGE THE FOLLOWING TO DECIDE WHAT TO ANALYZE
    typeGraph = 'Precipitation'

    # Plots what you decided to analyze
    if typeGraph is 'Date':
        dateAnalysis(date, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, totalNum)
    elif typeGraph is 'Day':
        dayAnalysis(day, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, totalNum)
    elif typeGraph is 'Temperature':
        tempAnalysis(averageTemp, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, totalNum)
    elif typeGraph is 'Precipitation':
        precipitationAnalysis(precipitation, brooklynNum, manhattanNum, williamsburgNum, queensboroNum, totalNum)
    else:
        print('Set typeGraph to one of these strings to analyze to analyze: '
              '1) "Date" 2) "Day" 3) "Temperature" 4) "Precipitation"')
