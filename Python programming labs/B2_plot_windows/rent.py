# description : This file contains the Rent class and a decorator. The rent class calculates
#               both the mean rental price for each year and the percent increase for each city
#               and creates a plot for both the mean rental price and percent increase.

import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib

def showNums(func):   
    """ it is a decorator, print out the return value of the fuction passed into """
    def returnMethod(*args, **kwargs):
        returnValue = func(*args, **kwargs)
        print("returnValue of function:", returnValue)
        return returnValue
    return returnMethod

class Rent:
    START_YEAR = 2011
    END_YEAR = 2018
    def __init__(self):
        try:
            filename = "lab2prices.csv"
            self._data = np.loadtxt(filename, usecols=(i for i in range(2, ((self.END_YEAR - self.START_YEAR + 1) * 12) + 1)), dtype= int, delimiter=',')            
            filename = "lab2cities.txt"
            with open(filename) as infile:
                self._cityList = [ line.rstrip()      for line in infile       if not line.isspace()]
            
            
            self._arrMean = self.calcMeanRentalPrice()
            self._arrIncrease = self.calcPercentIncrease()
        except OSError:
            raise OSError(filename)            
        except FileNotFoundError:
            raise FileNotFoundError(filename)

    def calcMeanRentalPrice(self):
        """ create an np array, assign the data into the np array, return the np array"""
        arrMean = np.zeros((  len(self._cityList)  ,  (self.END_YEAR - self.START_YEAR + 1) ))
        for index in range(0,(self.END_YEAR - self.START_YEAR + 1)*12,12):
            arrMean[:,index//12] = self._data[:, index:index+12].mean(1)
        
        return arrMean
    
    @showNums
    def calcPercentIncrease(self) :
        """ get the means of tne start year and the end year, store the percent increase into the np array, return the np array"""
        arrIncrease = ((self._arrMean[:,-1] - self._arrMean[:,0])/self._arrMean[:,0])*100
        return arrIncrease
    
    def plotRentalPrice(self, index) :
        """ plots the rental price by means of start year and end year, 
            plots the graph depending on what the user chooses, 
            plots All if the user chooses 'All' option """
        if index + 1 > len(self._cityList):
            colorTup = ('xkcd:blue', 'xkcd:aqua', 'xkcd:beige', 'xkcd:black', 'xkcd:teal', 'xkcd:chartreuse', 'xkcd:coral', 'xkcd:sienna', 'xkcd:olive', 'xkcd:fuchsia', 'xkcd:gold', 'xkcd:grey', 'xkcd:purple')
            for i in range(len(self._cityList)):
                plt.plot(range(1,(self.END_YEAR - self.START_YEAR + 1)+1), self._arrMean[i,:], colorTup[i], label = self._cityList[i])
        else:
            plt.plot(range(1,(self.END_YEAR - self.START_YEAR + 1)+1), self._arrMean[index,:], label = self._cityList[index])
        plt.xticks(range(1, (self.END_YEAR - self.START_YEAR + 1)+1), range(self.START_YEAR, self.END_YEAR + 1))
        plt.legend(loc = "best")
        plt.title("Rental price")
        plt.xlabel("Year")
        plt.ylabel("Price")
        
    def plotPercentIncrease(self):
        """ plots the percent increase with the names of the cities as the x-axis, 
            and the percent increase as the y-axis """
        plt.plot(range(0, len(self._cityList)), self._arrIncrease, "k", marker = "o")
        plt.bar(range(0, len(self._cityList)), self._arrIncrease, align = "center")
        plt.title("Percent Increase between 2011 and 2018")
        plt.xlabel("Cities")
        plt.ylabel("Percent Increase(%)")
        plt.xticks(range(0,len(self._cityList)), self._cityList, rotation = "vertical")
        plt.ylim(min(self._arrIncrease)*0.50 , max(self._arrIncrease)*1.1)
        
    def getCityList(self):
        """ returns a list of city names stored in instance variable self._cityList """
        return self._cityList
