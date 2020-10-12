# Amber
# CIS 41B
# Final Project
# Description is attached in readme.txt

import tkinter as tk
import tkinter.messagebox as tkmb
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
import numpy as np
import re

class MainWin(tk.Tk) :
    def __init__(self) :
        super().__init__()
        self.geometry("400x100")

        self._conn = sqlite3.connect("boba.db")
        self._cur = self._conn.cursor()

        # ['Cupertino', 'San Jose', 'Mountain View', 'Palo Alto', 'Santa Clara', 'Sunnyvale', 'Saratoga']
        self._cityList = [city[0]  for city in self._cur.execute("SELECT city FROM Cities") ]

        tk.Label(self, text = "Choice 1").grid(row = 0, column = 0)
        # Display boba shops based on distance from De Anza as the first criteria and then based on ranking as a secondary criteria
        tk.Button(self, text = "Display boba shops", command = self.displayBoba).grid(row = 0, column = 1, sticky = "w")

        tk.Label(self, text = "Choice 2").grid(row = 1, column = 0)
        # Search for Boba shops
        tk.Button(self, text = "Search for boba shop", command = self.clickBobaShop).grid(row = 1, column = 1, sticky = "w")

        tk.Label(self, text = "Choice 3").grid(row = 2, column = 0)
        # Ploting
        tk.Button(self, text = "Number of 4-5 starred boba stores in each city", command = self.starred).grid(row = 2, column = 1, sticky = "w")


        self.protocol("WM_DELETE_WINDOW", self.closeWin)
        
    def closeWin(self) :
        """ close the window and database """
        self._conn.close()
        self.destroy()    

    def displayBoba(self) : #1
        """ create a DisplayBobaShop object, pop up a window of distance categories """
        display = DisplayBobaShop(self, self._cur, self._cityList)
        self.wait_window(display)

    def clickBobaShop(self) : #2
        """ create a BobaShop object, pop up a window for with two choices to search boba shop """
        boba = BobaShop(self, self._cur, self._cityList)  
        self.wait_window(boba)

    def starred(self) : #3
        """ Show in a graph the number of 4-5 starred boba shops over each city """
        self._cur.execute("SELECT Boba.cityID FROM Boba JOIN Ranking ON Boba.rankingID = Ranking.id AND Ranking.ranking >= 4")
        starredList = self._cur.fetchall()

        cityidList = [cityid[0] for cityid in self._cur.execute("SELECT Boba.cityID FROM Boba JOIN Ranking ON Boba.rankingID = Ranking.id AND Ranking.ranking >= 4") ]

        npArr = np.array(cityidList)
        cityNum = [len(npArr[npArr == i])      for i in range(1, len(self._cityList)) ]

        matplotlib.rcParams['figure.figsize'] = (8, 6)
        plt.bar(np.arange(1, len(self._cityList)), cityNum)
        plt.xticks(np.arange(1, len(self._cityList)), self._cityList)

        plt.title("Number of 4-5 starred boba shops over each city")
        plt.xlabel("City Name")
        plt.ylabel("Number of boba stores")

        plt.show()

class DisplayBobaShop(tk.Toplevel) :
    def __init__(self, master, cur, cityList) :
        super().__init__(master)
        #self.geometry("400x300")
        self._cur = cur
        self._cityList = cityList

        self._var = 0
        self._controlVar = tk.IntVar()
        count = 0        

        tk.Label(self, text = "Distance categories: ").grid()

        self._distanceList = [   record  for record in self._cur.execute("SELECT distance FROM Boba ORDER BY distance")]

        self._disNP = np.linspace(0, self._distanceList[-1][0], 5)
        self._controlVar = tk.IntVar()
        count = 0
        for i in range(0, len(self._disNP)-1):
            tk.Radiobutton(self, text = str(self._disNP[i]) + "miles <= distance < " + str(self._disNP[i+1]) + "miles", variable = self._controlVar, value = count, command = lambda: self.resetValue(self._controlVar.get())).grid(row = count, sticky = 'w')
            count += 1
        self._B = tk.Button(self, text = "OK", command = self.clickOK).grid(row = 5)

        self.focus_set()
        self.grab_set()          


    def clickOK(self):
        """ get the starting distance and ending distance, call showList method to show boba list accroding to starting and ending distance """
        startD = self._disNP[self._var]
        endD = self._disNP[self._var + 1]

        self.showList(startD, endD)
    def resetValue(self, val):
        """ set new value to var variable """
        self._var = val

    def showList(self, startD, endD) :
        """ create a object of ShowWin, pop up a window with a boba list sorted by distance """
        dWin = ShowWin(self, self._cur, startD, endD)
        self.wait_window(dWin)

class ShowWin(tk.Toplevel) :
    def __init__(self, master, cur, startD, endD) :
        super().__init__(master)
        self._cur = cur

        self._bobaList = [record for record in self._cur.execute("SELECT Boba.bobaName, Boba.distance, Boba.address, Boba.description, Ranking.ranking FROM Boba JOIN Ranking ON Boba.rankingID = Ranking.id AND Boba.distance >= ? AND Boba.distance < ? ORDER BY Boba.distance", (startD, endD)) ]

        tk.Label(self, text = "Distance between " + str(startD) + " and " + str(endD)).grid()
        self._LB = tk.Listbox(self, height = 10, width = 20)
        self._LB.grid()

        bobaNameList = [name[0] for name in self._bobaList]
        self._LB.insert(tk.END, *bobaNameList)

        self.focus_set()
        self.grab_set()         
        self._LB.bind("<<ListboxSelect>>", self.showInfo)


    def showInfo(self, event) :
        """ pop up a message window to the user by showing the infomation of the selected boba shop """
        index = self._LB.curselection()[0]
        bbInfo = "Name: " + str(self._bobaList[index][0]) + "\nDistance: " + str(self._bobaList[index][1]) + "miles\nAddress: " + str(self._bobaList[index][2]) + "\nRanking: " + str(self._bobaList[index][4]) + "\nDescription: " + str(self._bobaList[index][3])
        tkmb.showinfo(title = "Info of selected Boba shop", message = bbInfo)
        self.focus_set() 

class BobaShop(tk.Toplevel) :
    def __init__(self, master, cur, cityList) :
        super().__init__(master)
        self.geometry("200x50")
        self._cur = cur
        self._cityList = cityList

        # Search by city (Santa Clara County/ Bay Area)
        tk.Button(self, text = "Search by city", command = self.showBobaList).grid()
        # Search by dollar sign (Santa Clara County/ Bay Area)
        tk.Button(self, text = "Search by dollar sign", command = self.dollarSign).grid()

    def showBobaList(self) :
        """ create a BobaCity object, pop up a window to ask for input to search boba shop by city """
        dWin = BobaCity(self, self._cur, self._cityList)
        self.wait_window(dWin)

    def dollarSign(self) :
        """ create a BobaDollarSign object, pop up a window with a list of boba sorted by dollar signs """
        dWin = BobaDollarSign(self, self._cur)
        self.wait_window(dWin)

class BobaCity(tk.Toplevel) :
    def __init__(self, master, cur, cityList) :
        super().__init__(master)
        #self.geometry("400x300")
        self._cur = cur
        self._cityList = cityList
        self._inputCity = ""
        self._entry = tk.StringVar()

        self._frame = tk.Frame(self)

        tk.Label(self._frame, text = ",".join(self._cityList)).grid(row = 0, column = 0, columnspan = 3)
        tk.Label(self._frame, text = "Enter city name:").grid(row = 1, column = 0, sticky = "w")
        self._E = tk.Entry(self._frame, textvariable = self._entry)
        self._E.grid(row = 1, column = 1, sticky = "w")

        self._bobaList = []

        self._LB = tk.Listbox(self._frame, height = 10, width = 30)
        self._LB.grid(columnspan = 2, sticky = "w")

        self._frame.grid()

        self._E.bind("<Return>", self.searchByCity)
        self._LB.bind("<<ListboxSelect>>", self.showBobaInfo)

    def searchByCity(self, event) :
        """ show error message if the input is invalid, show a list of boba shops if the input is valid """
        self._LB.delete(0, tk.END)
        self._inputCity = self._entry.get().strip().lower().title()
        if self._inputCity not in self._cityList :
            tkmb.showinfo(title = "Error", message = "Enter valid input")
        else :
            self._bobaList = [ bobaShop   for bobaShop in self._cur.execute("SELECT Boba.bobaName, Boba.address FROM Boba JOIN Cities ON Boba.cityID = Cities.id AND Cities.city = ?", (self._inputCity,)) ]
            #print(self._bobaList)
            showList = [record[0]   for record in self._bobaList]
            self._LB.insert(tk.END, *showList)


    def showBobaInfo(self, event) :
        """ pop up a message window to show the information of the selected boba shop """
        index = self._LB.curselection()[0]
        bobaName = self._bobaList[index][0]

        self._cur.execute("SELECT Boba.bobaName, Boba.distance, Boba.address, Boba.description, Ranking.ranking FROM Boba JOIN Ranking ON Boba.rankingID = Ranking.id AND Boba.bobaName = ? AND Boba.address = ?", (bobaName,self._bobaList[index][1]))
        infoTup = self._cur.fetchall()
        bbInfo = "Name: " + str(infoTup[0][0]) + "\nDistance: " + str(infoTup[0][1]) + "miles\nAddress: " + str(infoTup[0][2]) + "\nRanking: " + str(infoTup[0][4]) + "\nDescription: " + str(infoTup[0][3])
        tkmb.showinfo(title = "Info of selected Boba shop", message = bbInfo)


class BobaDollarSign(tk.Toplevel) :
    def __init__(self, master, cur) :
        super().__init__(master)
        self.geometry("400x400")
        self._cur = cur
        tk.Label(self, text = "Boba shops ordered by dollar sign").grid()

        self._LB = tk.Listbox(self, height = 20, width = 35)
        self._LB.grid()

        self._result = [record     for record in self._cur.execute("SELECT Boba.bobaName, Boba.address, Price.price FROM Boba JOIN Price ON Boba.priceID = Price.id AND Price.price !=  ? ORDER BY Price.id", ("NULL",))]

        self._bobaDollarSign = [   "{0:3s}{1:10s}".format(record[-1], record[0]).strip()   for record in self._result ]
        self._LB.insert(tk.END, *self._bobaDollarSign)

        self._LB.bind("<<ListboxSelect>>", self.showBobaInfo)

    def showBobaInfo(self, event) :
        """ pop up a message window to show the information of the selected boba shop """
        index = self._LB.curselection()[0]
        nameBoba = self._result[index][0]

        self._cur.execute("SELECT Boba.bobaName, Boba.distance, Boba.address, Boba.description, Ranking.ranking FROM Boba JOIN Ranking ON Boba.rankingID = Ranking.id AND Boba.bobaName = ? AND Boba.address = ?", (nameBoba, self._result[index][1]))
        tupInfo = self._cur.fetchall()
        bbInfo = "Name: " + str(tupInfo[0][0]) + "\nDistance: " + str(tupInfo[0][1]) + " miles\nAddress: " + str(tupInfo[0][2]) + "\nRanking: " + str(tupInfo[0][4]) + "\nDescription: " + str(tupInfo[0][3])
        tkmb.showinfo(title = "Info of selected Boba shop", message = bbInfo)


def main() :
    app = MainWin()
    app.mainloop()

main()