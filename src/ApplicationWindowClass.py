
from tkinter import font #, simpledialog
import tkinter as tk
from tkinter import *
import tkinter.font as tkfont

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
        self.fontSize = 12
        self.links = []

        self.audioController = None
        self.audioControllerInitalized = False

        self.fullscreen = False
    
    def initiate_window(self, windowTitle, displaySettings = {}, pdelay=0, delay=True, debugdisplay=False):
        # Reset local settings
        self.settings = displaySettings
        self.fontSize = self.settings["FONTSIZE"]
        self.theme = displaySettings["THEME"]

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
        self.master.config(bg=self.theme["WINDOWBGCOLOR"], highlightthickness=0, borderwidth=0)
        self.master.bind('<Configure>', self._window_resize_event)
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.create_widgets()
        self.window_is_open = True
        self.master.attributes("-fullscreen", self.fullscreen)

    def initiate_audio(self, audioController):
        self.audioController = audioController
        self.audioController.addLayer("UI")
        self.audioControllerInitalized = True
    
    def set_settings(self, displaySettings, pdelay=0, delay=True, debugdisplay=False):
        # Reset local settings
        self.settings = displaySettings
        self.fontSize = self.settings["FONTSIZE"]

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
        self.links = []
    
    def display(self, msg="", br=1, br2=0):
        self.screen.display(msg, br, br2)
    
    def displayAction(self, msg, command, br=1, br2=0):
        ''' Displays a message, but attaches a command to it if the player clicks it '''
        tag = f"<cmd{command}>"
        self.output_box.tag_configure(tag)
        self.output_box.tag_bind(tag, "<Button-1>", lambda event: self._get_auto_input(event, command))
        self.links.append(f"cmd{command}")
        message = f"{tag}<a>{msg}<a>{tag}"
        self.screen.display(message, br, br2)
    
    def displayHeader(self, msg="", br=0, br2=0):
        self.screen.displayHeader(msg, br, br2)
    
    def closeDisplay(self, closeDisplay = True):
        ''' Causes a window display update '''
        if closeDisplay:
            self.screen.closeDisplay()
        if self.window_is_open:
            self.output_box.configure(state=NORMAL)
            self.output_box.delete('1.0', END)
            lines = self.screen.get_current_lines()
            for line in lines:
                self.formatAndDisplayLine(line)
                # self.output_box.insert(END, "{}\n".format(line), ("<r>"))
            self.output_box.see("end")
            self.output_box.configure(state=DISABLED)
    
    def formatAndDisplayLine(self, line):
        ''' Gets all tags from the line and inserts the line into the output box with the proper tags '''
        allTags = self.tags + self.links
        lines = self.formatLine(line, allTags)
        for formattedLine in lines:
            self.output_box.insert(END, "{}".format(formattedLine[0]), (formattedLine[1]))
        self.output_box.insert(END, "\n")
        # Reset focus to input line
        self.input_line.focus_set()
        self.input_line.focus()
        self.input_line.focus_set()
    
    def formatLine(self, line, tags, tagsApplied = []):
        ''' Formats a line with the proper tags '''
        # Check if line needs formatted:
        if "<" in line:
            # get initial tag:
            tag = line.split("<")[1].split(">")[0]
            # Check if tag is valid:
            if tag in tags:
                tag = "<{}>".format(tag)
            else:
                return []
            # Split the line into pretag, tagged, and post tagged sections
            preTag = line.split(tag)[0]
            tagged = line.split(tag)[1]
            postTag = line.split(tag)[2]
            section1 = [(preTag, tagsApplied)]
            section2 = self.formatLine(tagged, tags, tagsApplied + [tag])
            section3 = self.formatLine(postTag, tags, tagsApplied)
            section4 = ""
            if len(line.split(tag)) >= 3:
                rest = ""
                for str in line.split(tag)[3:]:
                    rest += f"{tag}{str}"
                section4 = self.formatLine(rest, tags, tagsApplied)
            return section1 + section2 + section3 +section4
        else:
            if len(line) == 0:
                line = ""
            return [(line, tagsApplied)]
        

    
    def dprint(self, msg):
        self.screen.dprint(msg)


    # Local functions
    def create_widgets(self):
        self.fontSize = 10
        self.font = font.Font(family="courier", size=self.fontSize)

        self.output_box = tk.Text(self.master, wrap=tk.WORD, font=self.font, state=tk.DISABLED, padx=10, pady=10)
        self.output_box.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.scroll_bar = tk.Scrollbar(self.master, command=self.output_box.yview)
        self.scroll_bar.grid(row=0, column=2, sticky="ns")
        self.output_box.config(background=self.theme["WINDOWBGCOLOR"], foreground=self.theme["DEFAULTTEXTCOLOR"], 
                               borderwidth=0, highlightthickness=0, yscrollcommand=self.scroll_bar.set)
        
        self.output_box['yscrollcommand'] = self.scroll_bar.set

        # Set style tags
        self.tags = []
        # Styling tags
        for tag in self.theme['STYLE'].keys():
            newtag = self.theme['STYLE'][tag]['tag']
            self.tags.append(newtag)
            self.output_box.tag_configure(f"<{newtag}>", font=self.theme['STYLE'][tag]['font'])
            if "foreground" in self.theme['STYLE'][tag].keys():
                self.output_box.tag_configure(f"<{newtag}>", foreground=self.theme['STYLE'][tag]['foreground'])
            if "background" in self.theme['STYLE'][tag].keys():
                self.output_box.tag_configure(f"<{newtag}>", background=self.theme['STYLE'][tag]['background'])
        # Foreground tags
        for tag in self.theme['FOREGROUND'].keys():
            newtag = self.theme['FOREGROUND'][tag]['tag']
            self.tags.append(newtag)
            self.output_box.tag_configure(f"<{newtag}>", foreground=self.theme['FOREGROUND'][tag]['foreground'])
        # Background tags
        for tag in self.theme['BACKGROUND'].keys():
            newtag = self.theme['BACKGROUND'][tag]['tag']
            self.tags.append(newtag)
            self.output_box.tag_configure(f"<{newtag}>", background=self.theme['BACKGROUND'][tag]['background'])

        # Create the input textbox
        self.inputText = StringVar()
        self.input_line = tk.Entry(self.master, font=("Courier", 12), foreground=self.theme["DEFAULTTEXTCOLOR"],
                                   background=self.theme["INPUTBGCOLOR"], borderwidth=2, width=50)
        self.input_line.grid(row=1, column=0, pady=10)

        self.input_line.focus_set()

        # self.settings_button = tk.Button(self.master, text="+", command=self.update_font_size)
        # self.settings_button.grid(row=1, column=1, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.input_line.bind("<Return>", self._press_enter_event)
    
    def _press_enter_event(self, event):
        self._enter_pressed = True
    
    def _close_button_event(self):
        self.window_is_open = False
        self.master.destroy()

    def _get_enter_pressed(self):
        if self._enter_pressed:
            self._enter_pressed = False
            #if self.audioControllerInitalized:
            self.audioController.playBufferedAudio("UI", "click", False, False)
            return True
        return False
    
    def _window_resize_event(self, event):
        self.recalculate_line_length()

    def recalculate_line_length(self):
        width = self.output_box.winfo_width()
        font = self.output_box["font"]
        font_face = tkfont.Font(family=font, size=self.fontSize, weight="normal")

        char_width = int(font_face.measure("A") + 0.5)
        maxChars = int(1.0 * (width) / char_width)
        if maxChars > 0:
            self.max_line_characters = maxChars
        # if self.window_is_open:
        #     self.screen.set_line_length(self.max_line_characters)
        self.closeDisplay(False)

    def get_max_line_characters(self):
        return self.max_line_characters
    
    def get_input(self, convert_to_int = False, clearinput=True, acceptNothing = False):
        input_string = None
        while input_string == None:
            while not self._get_enter_pressed() and self.window_is_open:
                self.call_update()
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
        # Return the input string
        return input_string
    
    def _get_auto_input(self, event, cmd):
        self.input_line.delete(0,END)
        self.input_line.insert(0, cmd)
        self._enter_pressed = True
    
    def wait_for_enter(self):
        self.displayAction("<i>Anything to continue...<i>", 0)
        self.closeDisplay()
        while not self._get_enter_pressed() and self.window_is_open:
            self.call_update()
        if not self.window_is_open:
            return -1
        self.input_line.delete(0,END)
    
    '''
    def update_font_size(self):
        font_size = simpledialog.askinteger("Font size", "Enter font size:", minvalue=8, maxvalue=72)
        if font_size:
            self.fontSize = font_size
            self.settings["FONTSIZE"] = self.fontSize
            self.output_box.config(font=("Courier", self.fontSize))
    '''

    def call_update(self):
        self.update()
        if self.audioControllerInitalized:
            self.audioController.updateAll()
        
    def get_settings(self):
        return self.settings
    
    def set_fullscreen(self, fullscreen):
        if self.window_is_open and self.fullscreen != fullscreen:
            self.master.attributes("-fullscreen", fullscreen)
            self.fullscreen = fullscreen