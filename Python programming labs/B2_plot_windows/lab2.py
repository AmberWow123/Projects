# description : This file contains three classes (DialogWin, PlotWin, and MainWin). 
#               class MainWin pop up a window for the user to choose the rental price or the percent increase
#               class DialogWin lets the user choose which city for the rental trend plot
#               class PlotWin plot either the rental trend or the rental percent increase

import matplotlib
matplotlib.use('TkAgg')                                 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import tkinter.messagebox as tkmb
from rent import Rent

class DialogWin(tk.Toplevel):
    def __init__(self, master, ob) :
        super().__init__(master)
        
        self.title("Choose City")
        self._var = -1
        control_var = tk.IntVar()
        #control_var.set(0)
        self.focus_set()
        self.grab_set()        
        for i in range(len(ob.getCityList())) :
            tk.Radiobutton(self, text = ob.getCityList()[i], variable = control_var, value = i, command = lambda : self.resetValue(control_var.get())).grid(row = i, sticky = 'w')
        
        tk.Radiobutton(self, text = "All", variable = control_var, value = 13, command = lambda : self.resetValue(control_var.get())).grid(row = 13, sticky = 'w')
        self.transient(master)
        tk.Button(self, text = "OK", command = self.clickOK).grid(row = 14, sticky = 'w')
        
    def resetValue(self, val) :
        """ set value to the instance variable var """
        self._var = val
        
    def getVal(self) :
        """ return the instance variable var """
        return self._var
    
    def clickOK(self):
        """ destroy the recent window """
        self.destroy()
        
class PlotWin(tk.Toplevel) :
    def __init__(self, master, ob, val = -1) : # for rental price
        super().__init__(master)
        fig = plt.figure(figsize=(6, 8))
        if(val >= 0):
            ob.plotRentalPrice(val)
        else:
            ob.plotPercentIncrease()
        canvas = FigureCanvasTkAgg(fig, master=self)      
        canvas.get_tk_widget().grid()
        canvas.draw()              
        
        self.focus_set()   
        self.transient(master)
        
class MainWin(tk.Tk) :
    def __init__(self) :
        super().__init__()
        self.fileError = False
        self.title("Rent Data")
        self.geometry("230x50+200+200")
        try:           
            obj = Rent()  
            tk.Label(self, text = "Rent Data for Santa Clara County", fg = "blue").grid(row = 0, column = 0, columnspan = 5)  
            tk.Button(self, text = "Trend over Time", command = lambda : self.clickDialogWin(obj)).grid(row = 1)
            tk.Button(self, text = "Percent Increase", command = lambda : self.clickPlotWin(obj)).grid(row = 1, column = 1)              
        except IOError as e:
            tkmb.showerror(title = "Error", message = "unable to open " + str(e))
            self.fileError = True  
        
    def clickOK(self):
        """ destroy the recent window """
        self.destroy()        

    def clickDialogWin(self, ob) :
        """ creates a DialogWin object, gets an index to know which city to plot', then creates a PlotWin object to plot the graph"""
        dWin = DialogWin(self, ob)
        self.wait_window(dWin)
        value = dWin.getVal()
        if value > -1:
            win = PlotWin(self, ob, value)
        
    def clickPlotWin(self, ob) :
        """ creates a plotWin object to plot the graph """
        dWin = PlotWin(self, ob)
        
app = MainWin()
if not app.fileError:
    app.mainloop()
