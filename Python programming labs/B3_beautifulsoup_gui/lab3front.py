'''
Description: This file contains two classes (DisplayWin, MainWin).
             Class DisplayWin displays a window of popular names depending
             on the country name that the user selected from the ListBox.
             Class MainWin displays a mian window that asks the user for just one
             alphabet character, and displays all the country names in the database starting with that
             character.
'''

import tkinter as tk
import tkinter.messagebox as tkmb
import sqlite3
import re


class DisplayWin(tk.Toplevel) :
    def __init__(self, master, cursor, name) :
        super().__init__(master)
        self.geometry("300x300")
        
        tk.Label(self, text = "Most popular name for "+ name).grid(row = 0, column = 0)
        F1 = tk.Frame(self)
        S = tk.Scrollbar(F1)
        self._LB = tk.Listbox(F1, height = 10, width = 30, yscrollcommand = S.set)
        self._LB.grid(row = 1, column = 0)
        S.grid(row = 1, column = 1, sticky = "ns")
        F1.grid(row = 1, column = 0)
        
        cursor.execute("SELECT * FROM popularNameDB WHERE country = ?", (name,))
        results = filter(None, cursor.fetchone()[1:])
        for ele in sorted(results) :
            self._LB.insert(tk.END, str(ele))
        
        self.focus_set()
        S.config(command = self._LB.yview)
        
class MainWin(tk.Tk) :
    def __init__(self) :
        super().__init__()
        self.geometry("500x300")
        
        self._conn = sqlite3.connect("popularName.db")
        self._cur = self._conn.cursor()
        
        self._countrySet = {name[0][0]     for name in self._cur.execute("SELECT country FROM popularNameDB")}
        
        F0 = tk.Frame(self)

        tk.Label(F0, text = "Enter first letter of the country name").grid(row = 0, column = 0)
        self._entryText = tk.StringVar()
        self._E = tk.Entry(F0, textvariable = self._entryText)
        self._E.grid(row = 0, column = 1)
        self._E.bind("<Return>", self.getInput)
        F2 = tk.Frame(self)
        self._strVar = tk.StringVar()
        self._countryLabel = tk.Label(F0, textvariable = self._strVar).grid(row = 2, column = 0, columnspan = 2, sticky = 'w')
        F0.grid(row = 0, column = 0)
        
        S1 = tk.Scrollbar(F2)
        self._LB = tk.Listbox(F2, height = 10, width = 45, yscrollcommand = S1.set)
        self._LB.grid(row = 3, column = 0)
        
        S1.grid(row = 3, column = 1, sticky = "ns")
        S1.config(command = self._LB.yview)
        F2.grid(row = 3, column = 0)
        self.list1 = []
        
        self._LB.bind('<<ListboxSelect>>', self.clickDisplayWin)
        self.protocol("WM_DELETE_WINDOW", self.closeWin)
        
    def closeWin(self) :
        """ close the window and database """
        self._conn.close()
        self.destroy()
        
    def getInput(self,event):
        '''This method receives an event from the constructor. When the user clicks enter on the input,
                The method checks the input. If the input is valid, country names starting with the input the user
                gave will be inserted and displayed on the ListBox.'''        
        self._LB.delete(0, tk.END)
        self._entryText.set(self._entryText.get().strip())
        m = re.match("^([A-Za-z])$", self._entryText.get())
        if not m or m == None:
            tkmb.showinfo(title = "Error", message = "Enter a letter only")
        elif m.group().upper() not in self._countrySet :
            tkmb.showinfo(title = "Error", message = "No country in database starting letter " + self._entryText.get())
        else :    
            self._strVar.set("Click to choose country")
            self._cur.execute("SELECT country FROM popularNameDB WHERE country LIKE ?", (str(self._entryText.get().strip())+"%",))
            nameTup = self._cur.fetchall()
            for ele in sorted(nameTup) :
                self._LB.insert(tk.END, str(*ele)) 
            self.list1 = nameTup

    def clickDisplayWin(self, event):
        '''This method receivesd an event from the ListBox. When the user clicks on one of the selections,
                the countryName the user selected is passed to the constructor of the DisplayWin class.'''        
        if self._entryText.get() != "" :
            index = self._LB.curselection()[0]
            dWin = DisplayWin(self, self._cur, self.list1[index][0])
            self.wait_window(dWin)

app = MainWin()
app.mainloop()