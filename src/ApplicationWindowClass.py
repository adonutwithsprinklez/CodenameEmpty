
import time
from tkinter import font
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
        self.window_is_open = False
    
    def initiate_window(self, windowTitle, displaySettings = {}, pdelay=0, delay=True, debugdisplay=False):
        # Reset local settings
        self.settings = displaySettings

        # Set the virtual screen settings:
        self.screen.debugging = debugdisplay
        self.screen.delay = delay
        self.screen.printdelay = pdelay

        # Window initiation
        root = tk.Tk()
        super().__init__(root)
        self.winfo_toplevel().title(windowTitle)
        self.master = root
        self.master.geometry("{}x{}".format(self.settings["WIDTH"],self.settings["HEIGHT"]))
        self.master.protocol('WM_DELETE_WINDOW', self._close_button_event)
        self.master.bind('<Configure>', self._window_resize_event)
        self.create_widgets()
        self.pack()
        self.window_is_open = True
    
    def set_settings(self, displaySettings, pdelay=0, delay=True, debugdisplay=False):
        # Reset local settings
        self.settings = displaySettings

        # Set the virtual screen settings:
        self.screen.debugging = debugdisplay
        self.screen.delay = delay
        self.screen.printdelay = pdelay
    
    def close_window(self):
        if self.window_is_open:
            self.window_is_open = False
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
        if self.window_is_open:
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
        self.font = font.Font(family="courier", size=10)

        self.output_box = tk.Text(self.master, relief=FLAT)
        self.output_box.configure(font=self.font)
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
    
    def _close_button_event(self):
        self.window_is_open = False
        self.master.destroy()

    def _get_enter_pressed(self):
        if self._enter_pressed:
            self._enter_pressed = False
            return True
        return False
    
    def _window_resize_event(self, event):
        fontSize = int(self.master.winfo_width() / 70)
        self.font = font.Font(family="courier", size=fontSize)
        self.output_box.configure(font=self.font)
    
    def get_input(self, convert_to_int = False, clearinput=True, acceptNothing = False):
        input_string = None
        while input_string == None:
            while not self._get_enter_pressed() and self.window_is_open:
                self.update()
            if not self.window_is_open:
                return -1
            input_string = self.input_line.get()
            if not acceptNothing and input_string == "":
                input_string = None
            else:
                if clearinput:
                    self.input_line.delete(0,END)
                if convert_to_int:
                    try:
                        return int(input_string)
                    except:
                        return -1
        return input_string
    
    def wait_for_enter(self):
        while not self._get_enter_pressed() and self.window_is_open:
            self.update()
        if not self.window_is_open:
            return -1