"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for WakeUpTL.

"""


from tkinter import Frame

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graph():
    """Class containing the Graph gui. 

    """

    def __init__(self, view, model, size=(6,5)):
    #Constructor for the Graph superclass

        self.model = model
        self.view = view

        self.frame = Frame(self.view)
        
        self.initFigure(size=size)
        self.addStepGraph()

    def initFigure(self, size=(6,5)):
    #This method creates the canva for the Graph
        self.fig = Figure(figsize=size, dpi=65, facecolor=self.model.parameters_dict['backgroundColor'])

        self.plot = self.fig.add_subplot(111)
        self.plot.set_facecolor(self.model.parameters_dict['backgroundColorGraph'])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().configure(bg=self.model.parameters_dict['backgroundColor'])
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()


    def addStepGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', colorLine="blue", grid=True, marker_pos=[]):
    #This method is called to add data to be plotted on self.fig    
        self.plot.step(x, y, color=colorLine, markevery=marker_pos, markerfacecolor="green", markeredgecolor="black")
        self.plot.set_title(title)

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()
        
    def addLinGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', color="blue", grid=True, marker_pos=[]):
    #This method is called to add data to be plotted on self.fig    
        self.plot.plot(x, y, color=color, markevery=marker_pos, markerfacecolor="green", markeredgecolor="black")
        self.plot.set_title(title)

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()
        
    def addScatteredGraph(self, x=[], y=[], xlabel="", ylabel="", title="", xscale="linear", yscale='linear', color="blue", grid=True, marker_pos=[]):
    #This method is called to add data to be plotted on self.fig    
        self.plot.scatter(x, y, s=10, color=color)
        self.plot.set_title(title)

        self.plot.set_xlabel(xlabel)
        self.plot.set_xscale(xscale)

        self.plot.set_ylabel(ylabel)
        self.plot.set_yscale(yscale)

        self.plot.grid(grid)

        self.canvas.draw()

    def clearGraph(self):
    #This method is called to clear all data from a Graph
        self.plot.clear()

        self.fig.set_facecolor(self.model.parameters_dict['backgroundColor'])
        self.canvas.get_tk_widget().configure(bg=self.model.parameters_dict['backgroundColor'])
        self.plot.set_facecolor(self.model.parameters_dict['backgroundColorGraph'])