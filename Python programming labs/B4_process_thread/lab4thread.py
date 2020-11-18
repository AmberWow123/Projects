'''
Description: This file contains a MainWin class that opens a window and allows user to choose a respective region
and skill, then saves the appropriate jobs in txt files in a folder with a directory of the users picking. This file uses threads
to get the data.
'''

import urllib.request as ur
import requests
from bs4 import BeautifulSoup 
import re
import time
import tkinter as tk
import tkinter.messagebox as tkmb
import tkinter.filedialog
import os
import threading

class MainWin(tk.Tk) :
    skills = ["C++", "Python", "Java", "Android", "Linux"]
    locations = ["San Francisco", "Los Angeles"]
    
    
    def __init__(self) :
        super().__init__()
        self.title("Job Listing")
        self.geometry("400x300")
        tk.Label(self, text = "Select Region").grid(row = 0, column = 0, columnspan = 2)
        tk.Button(self, text = "Northern CA", command = lambda : self.clickRegion("Northern CA", "San Francisco")).grid(row = 1, column = 0)
        tk.Button(self, text = "Southern CA", command = lambda : self.clickRegion("Southern CA", "Los Angeles")).grid(row = 1, column = 1)

        self._region = ""
        self._strVar = tk.StringVar()
        self._selectedSkill = []

        tk.Label(self, textvariable = self._strVar).grid(row = 2, column = 0, columnspan = 2)
    
        self._LB = tk.Listbox(self, height = 10, width = 30, selectmode = "multiple")
        self._LB.grid(row = 3, column = 0, columnspan = 2)
        
        tk.Button(self, text = "OK", command = self.clickOK).grid(row = 4, columnspan = 2)

    def clickRegion(self, region, country) :
        '''This program displays the skills to the listbox when the user clicks on a region.'''
        self._region = country
        self._LB.delete(0, tk.END)
        self._strVar.set("Select skill(s) for " + region + " and click OK")
        for ele in self.skills :
            self._LB.insert(tk.END, ele)

    def storeData(self, skill) :
        '''This function stores the company, job location and job title retrieved from Github in json format into a txt file and joins it to the lab4output directory'''
        page = requests.get("https://jobs.github.com/positions.json?description={}&location={}+{}".format(skill, self._region.split()[0], self._region.split()[1]))
        data = page.json()

        fh = open(os.path.join("lab4output", skill + "_jobs.txt"), "w") 
        for tag in data :
            m = re.search("([A-Za-z]*\s*[A-Za-z]*)", tag["location"])
            if m:            
                fh.write("{:<50}{:<50}{:<50}\n".format(tag["company"], m.group(), tag["title"]))
        fh.close()        
        
        
    def clickOK(self) :
        '''This method saves a folder of txt files in a directory of the user's choice after user chooses skills and clicks ok'''
        if not self._LB.curselection() :
            tkmb.showerror(title = "Error", message = "Please make a selection")
        else :
            self._selectedSkill = [ self.skills[i]   for i in self._LB.curselection()      ]
            start = os.getcwd()
            
            d = tk.filedialog.askdirectory(initialdir = ".")
            
            os.chdir(d)
            if not os.path.isdir("lab4output") :
                os.mkdir("lab4output")
                
            threads = []
            for skill in self._selectedSkill :
                t = threading.Thread(target = self.storeData, args = (skill,))
                threads.append(t)
            
            startTime = time.time()
            for t in threads :
                t.start()
            
            for t in threads :
                t.join()
            
            print("Elapsed time: {:.2f}s".format(time.time() - startTime))
            
            os.chdir(start)

app = MainWin()
app.mainloop()

