"""Copyright Oticon Medical NICE

Developped by : Luc PERARD

File description : Class container for WebcamTL.

"""

from tkinter import Canvas, DoubleVar, Entry, Frame, IntVar, LabelFrame, Radiobutton, Scrollbar, filedialog
from tkinter import Label
from tkinter.constants import BOTTOM, TOP
from tkinter.ttk import Combobox
from tkinter import Button

from PIL import Image, ImageTk
import cv2

class WebcamTL():
    """Class containing a GUI for Parameters attributes

    """

    def __init__(self, frame, view, model=None):
    #Constructor for the Paramaters class

        self.frame = frame
        self.view = view
        self.model = model

        self.frame.configure(bg=self.model.parameters_dict['backgroundColor'])
        self.initAttributes()
                
        self.initFrame()
        self.initWidgets()

    def initAttributes(self):
    #This method instancitaes all the attributes
        self.frameline_webcam = Frame(self.frame, bg=self.model.parameters_dict['backgroundColor'])
        self.frameline_button = Frame(self.frame, bg=self.model.parameters_dict['backgroundColor'])

        self.snapperImg = Image.open("snapper.png")
        self.snapperImg = self.snapperImg.resize((45, 40), Image.ANTIALIAS)
        self.snapperImg = ImageTk.PhotoImage(self.snapperImg)

        self.label_webcam = Label(self.frameline_webcam, bg=self.model.parameters_dict['backgroundColor'])

        self.combo_webcam = Combobox(self.frameline_button, state="readonly", width=10, values=['Webcam 1', 'Webcam 2', 'Webcam 3'])
        self.combo_webcam.current(0)

        self.button_snap = Button(self.frameline_button, image=self.snapperImg, command=self.button_snap_callback)

        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def initFrame(self):
    #This method pack every frame      
        self.frameline_webcam.pack(pady=5)
        self.frameline_button.pack()

    def initWidgets(self):
    #This method pack every button
        self.label_webcam.pack()

        self.combo_webcam.pack(side='left', pady=8, padx=5, expand='yes')
        self.combo_webcam.bind("<<ComboboxSelected>>", self.combo_webcam_callback)

        self.button_snap.pack(side='left', pady=8, padx=5, expand='yes')

    def button_snap_callback(self):
    #this method is called when the button add is clicked.    
        image = self.img   
        self.path = filedialog.asksaveasfilename(title = "Select file", filetypes = (("all files","*.*"), ("png files","*.png"), ("jpeg files","*.jpeg")))
        if (self.path != "") and (self.path[-4:] != '.png'):
            image.save(self.path + ".png")

    def combo_webcam_callback(self, args=None):
    #This method change the selected webcam
        cv2.destroyAllWindows()
        self.capture = cv2.VideoCapture(self.combo_webcam.current(), cv2.CAP_DSHOW)
        
    def show_frames(self, args=None):
    # Get the latest frame and convert into Image
        try:
            cv2image= cv2.cvtColor(self.capture.read()[1],cv2.COLOR_BGR2RGB)
            self.img = Image.fromarray(cv2image)
            cv2image = cv2.resize(cv2image,(700,520))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image = img)
            self.label_webcam.imgtk = imgtk
            self.label_webcam.configure(image=imgtk)
        except:
            None

        if self.view.topLevel_webcam.state() == "normal":
            self.label_webcam.after(40, self.show_frames)