
import time
import tkinter as tk
from tkinter import *

from displayClass import Screen

class ApplicationWindow(tk.Frame):
    def __init__(self, pdelay=0, delay=True, debug=False):
        # Setup local variables
        self.settings = {}
        self.debug = debug
        self.acceptingUserInput = False

        # Setup the screen object
        self.screen = Screen(pdelay, delay, debug)

        # Runtime variables
        self._enter_pressed = False
    
    def initiate_window(self, displaySettings = {}, pdelay=0, delay=True, debugdisplay=False):
        # Reset local settings
        self.settings = displaySettings

        # Set the virtual screen settings:
        self.screen.debugging = debugdisplay
        self.screen.delay = delay
        self.screen.printdelay = pdelay

        # Window initiation
        root = tk.Tk()
        super().__init__(root)
        self.master = root
        self.master.geometry("{}x{}".format(self.settings["WIDTH"],self.settings["HEIGHT"]))
        self.create_widgets()
        self.pack()
    
    def close_window(self):
        self.master.destroy()
    
    # Game engine accessible functions:
    # (Basically acts as a way to keep the legacy Screen object working)
    def clearScreen(self):
        self.screen.clearScreen()
    
    def display(self, msg="", br=1, br2=0):
        self.screen.display(msg, br, br2)
    
    def displayHeader(self, msg="", br=0, br2=0):
        self.screen.displayHeader(msg, br, br2)
    
    def closeDisplay(self):
        ''' Causes a window display update '''
        self.screen.closeDisplay()
        self.output_box.configure(state=NORMAL)
        self.output_box.delete('1.0', END)
        lines = self.screen.get_current_lines()
        for line in lines:
            self.output_box.insert(END, "{}\n".format(line))
        self.output_box.see("end")
        self.output_box.configure(state=DISABLED)
    
    def dprint(self, msg):
        self.screen.dprint(msg)

    # Local functions

    def create_widgets(self):
        self.output_box = tk.Text(self.master, relief=FLAT)
        self.output_box.grid(sticky = N + E + S + W)

        self.scroll_bar = tk.Scrollbar(self.output_box, command=self.output_box.yview)
        self.scroll_bar.config(command=self.output_box.yview) 
        self.scroll_bar.pack(side=RIGHT,fill=Y)
        
        self.output_box['yscrollcommand'] = self.scroll_bar.set
        self.output_box.pack(expand=True, fill='both')

        # Disable the output box to disallow user input
        self.output_box.configure(state=DISABLED)

        # Create the input textbox
        self.inputText = StringVar()
        self.input_line = Entry(self.master, text=self.inputText)
        self.input_line.pack(side=BOTTOM, fill='x')

        self.input_line.focus_set()

        self.input_line.bind("<Return>", self._press_enter_event)
    
    def _press_enter_event(self, event):
        self._enter_pressed = True

    def _get_enter_pressed(self):
        if self._enter_pressed:
            self._enter_pressed = False
            return True
        return False
    
    def get_input(self, convert_to_int = False, clearinput=True):
        while not self._get_enter_pressed():
            self.update()
        input_string = self.input_line.get()
        if clearinput:
            self.input_line.delete(0,END)
        if convert_to_int:
            try:
                return int(input_string)
            except:
                return -1
        return input_string