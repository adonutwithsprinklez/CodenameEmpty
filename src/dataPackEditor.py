

# Official imports
import copy
from tkinter import font
import tkinter as tk
from tkinter import ttk
from tkinter import *

# Local Imports
from jsonDecoder import loadJson, saveJson


class MetaDataEditor(tk.Frame):
    def __init__(self, fileLocation, settings):
        self.settings = settings
        self.fileLoc = fileLocation
        self.metaFileData = loadJson(metaFile)

        self.window_is_open = False

    def initiate_window(self):
        root = tk.Tk()
        super().__init__(root)
        print(self.fileLoc)
        super().winfo_toplevel().title("Project: Empty Datapack Editor | {}".format(self.fileLoc))

        self.master = root
        self.master.geometry("{}x{}".format(600,400))
        self.master.minsize(600, 400)
        self.master.protocol('WM_DELETE_WINDOW', self._close_button_event)
        root.option_add('*tearOff', FALSE)
        
        self.menubar = Menu(self.master)
        self.master['menu'] = self.menubar
        
        self.create_widgets()
        self.pack()
        self.window_is_open = True

        self.master.mainloop()
    
    def create_widgets(self):
        self.font = font.Font(family="courier", size=10)

        menu_file = Menu(self.menubar)
        menu_edit = Menu(self.menubar)
        menu_help = Menu(self.menubar)
        self.menubar.add_cascade(menu=menu_file, label='File')
        self.menubar.add_cascade(menu=menu_edit, label='Edit')
        self.menubar.add_cascade(menu=menu_help, label='Help')

        # menu_file.add_command(label='New', command=self.newFile)
        menu_file.add_command(label='Open...', command=self.openFile)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self._close_button_event)

        menu_edit.add_command(label='Save', command=self.savePack)

        menu_help.add_command(label='Help', command=self.menuHelp)
        menu_help.add_command(label='About', command=self.menuAbout)

        self.masterframe = ttk.Frame(self.master)
        self.masterframe.pack(expand=1, fill="both")
        self.tabControl = ttk.Notebook(self.masterframe)

        self.create_metadatatab()
        self.create_modifiertab()
        self.create_enemiestab()

        # TODO: Add the other tabs
        # self.tabControl.add(self.areatab, text = "  Areas  ")
        # self.tabControl.add(self.armortab, text = "  Armors  ")
        # self.tabControl.add(self.misctab, text = "  Misc  ")
        # self.tabControl.add(self.npcstab, text = "  NPCs  ")
        # self.tabControl.add(self.queststab, text = "  Quests  ")
        # self.tabControl.add(self.racetab, text = "  Races  ")
        # self.tabControl.add(self.weapontab, text = "  Weapons  ")
        # self.areatab = ttk.Frame(self.tabControl)
        # self.armortab = ttk.Frame(self.tabControl)
        # self.eventtab = ttk.Frame(self.tabControl)
        # self.misctab = ttk.Frame(self.tabControl)
        # self.npcstab = ttk.Frame(self.tabControl)
        # self.queststab = ttk.Frame(self.tabControl)
        # self.racetab = ttk.Frame(self.tabControl)
        # self.weapontab = ttk.Frame(self.tabControl)

        self.tabControl.pack(expand=1, fill="both")
    
    def create_metadatatab(self):
        # TAB CREATION
        self.metadatatab = ttk.Labelframe(self.tabControl, text="Data Pack Info")
        self.metadatatab.grid(row=0, column=0, padx=50, pady=50, sticky=E+W+N+S)
        self.tabControl.add(self.metadatatab, text = "  Metadata  ")


        # SCROLLABLE CREATION
        canvas = tk.Canvas(self.metadatatab)
        scrollbar = ttk.Scrollbar(self.metadatatab, orient=VERTICAL, command=canvas.yview)
        
        metadataFrame = ttk.Frame(canvas)
        metadataFrame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=E+W+N+S)
        metadataFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        # ELEMENT CREATION
        ttk.Label(metadataFrame, text="Name", font=self.font).grid(row=0, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(metadataFrame, text="Author", font=self.font).grid(row=1, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(metadataFrame, text="Description", font=self.font).grid(row=2, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(metadataFrame, text="Pack Type", font=self.font).grid(row=3, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(metadataFrame, text="Version", font=self.font).grid(row=4, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(metadataFrame, text="Game Descriptions", font=self.font).grid(row=5, column=0, padx=10, pady=5, sticky=E)

        self.packName = Entry(metadataFrame, font=self.font)
        self.packAuth = Entry(metadataFrame, font=self.font)
        self.packDesc = Entry(metadataFrame, font=self.font)
        self.packType = Entry(metadataFrame, font=self.font)
        self.packVers = Entry(metadataFrame, font=self.font)
        self.packName.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky=E+W)
        self.packAuth.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=E+W)
        self.packDesc.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=E+W)
        self.packType.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky=E+W)
        self.packVers.grid(row=4, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.packName.insert(END, self.metaFileData["name"])
        self.packAuth.insert(END, self.metaFileData["author"])
        self.packDesc.insert(END, self.metaFileData["desc"])
        self.packType.insert(END, self.metaFileData["packType"])
        self.packVers.insert(END, self.metaFileData["version"])

        self.gameDesc = tk.Text(metadataFrame)
        self.gameDesc.configure(font=self.font, wrap='none')
        self.gameDesc.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky=E+W+N+S)


        # FINISHING TOUCHES
        canvas.create_window((0, 0), window=metadataFrame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        metadataFrame.rowconfigure(5, weight=1)
        metadataFrame.columnconfigure(0, weight=0)
        metadataFrame.columnconfigure(1, weight=1)
        metadataFrame.columnconfigure(2, weight=3)
        metadataFrame.columnconfigure(2, weight=3)

        metadataFrame.pack(expand=1, fill="both")
        self.metadataGameDescFill()


    def create_modifiertab(self):
        self.modifiertab = ttk.Frame(self.tabControl)
        self.modifiertab.grid(row=0, column=0, padx=50, pady=50, sticky=E+W+N+S)
        self.tabControl.add(self.modifiertab, text = "  Modifiers  ")


        # SCROLLABLE CREATION
        canvas = tk.Canvas(self.modifiertab)
        
        modifierFrame = ttk.Frame(canvas)
        modifierFrame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=E+W+N+S)

        # ELEMENT CREATION
        # Files display
        self.modifierFilesList = StringVar(value=[])
        modifierFilesFrame = Frame(modifierFrame)
        modifierFilesFrame.grid(row=0, column=0, sticky=N+E+W+S)
        ttk.Label(modifierFilesFrame, text="Collections", font=self.font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.modifierFiles = Listbox(modifierFilesFrame, listvariable=self.modifierFilesList, font=self.font)
        self.modifierFiles.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.modifierFiles.bind("<<ListboxSelect>>", self._modifierLoadCollection)
        ttk.Button(modifierFilesFrame, text="-", command=self.delModifierFile).grid(row=2, column=0, sticky=N+S+W+E)
        ttk.Button(modifierFilesFrame, text="+", command=self.newModifierFile).grid(row=2, column=1, sticky=N+S+W+E)

        modifierFilesFrame.rowconfigure(1, weight=1)
        modifierFilesFrame.columnconfigure(0, weight=1)
        modifierFilesFrame.columnconfigure(1, weight=1)

        # Modifier List Display
        self.currentModifiersList = StringVar(value=[])
        seperator = ttk.Separator(modifierFrame, orient=VERTICAL)
        seperator.grid(row=0, column=1, stick=N+S)
        modifiersListFrame = Frame(modifierFrame)
        modifiersListFrame.grid(row=0, column=2, sticky=N+E+W+S)

        ttk.Label(modifiersListFrame, text="Modifiers", font=self.font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.modifierList = Listbox(modifiersListFrame, listvariable=self.currentModifiersList,  font=self.font)
        self.modifierList.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.modifierList.bind("<<ListboxSelect>>", self._modifierLoadModifier)
        ttk.Button(modifiersListFrame, text="-", command=self.delModifierFile).grid(row=2, column=0, sticky=N+S+W+E)
        ttk.Button(modifiersListFrame, text="+", command=self.newModifierFile).grid(row=2, column=1, sticky=N+S+W+E)

        modifiersListFrame.rowconfigure(1, weight=1)
        modifiersListFrame.columnconfigure(0, weight=1)
        modifiersListFrame.columnconfigure(1, weight=1)

        # Modifier data display
        seperator = ttk.Separator(modifierFrame, orient=VERTICAL)
        seperator.grid(row=0, column=3, stick=N+S)
        modifierDataFrame = Frame(modifierFrame)
        modifierDataFrame.grid(row=0, column=4, sticky=N+E+W+S)
        
        ttk.Label(modifierDataFrame, text="Modifier ID", font=self.font).grid(row=0, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(modifierDataFrame, text="Name", font=self.font).grid(row=1, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(modifierDataFrame, text="Description", font=self.font).grid(row=2, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(modifierDataFrame, text="Effect", font=self.font).grid(row=3, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(modifierDataFrame, text="Strength", font=self.font).grid(row=4, column=0, padx=10, pady=5, sticky=E)

        self.modId = Entry(modifierDataFrame, font=self.font)
        self.modName = Text(modifierDataFrame, height=3, font=self.font)
        self.modDesc = Text(modifierDataFrame, height=3, font=self.font)
        self.modEffect = Entry(modifierDataFrame, font=self.font)
        self.modStrength = Entry(modifierDataFrame, font=self.font)
        saveModifier = Button(modifierDataFrame, text="Save", command=self.saveModifier)

        self.modId.grid(row=0, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modName.grid(row=1, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modDesc.grid(row=2, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modEffect.grid(row=3, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modStrength.grid(row=4, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        saveModifier.grid(row=5, column=0, columnspan=2, sticky=E+W+S)
        # self.packName.insert(END, self.metaFileData["name"])

        self.modName.configure(wrap='none')
        self.modDesc.configure(wrap='none')

        modifierDataFrame.columnconfigure(1, weight=1)


        # FINISHING TOUCHES
        canvas.create_window((0, 0), window=modifierFrame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        modifierFrame.rowconfigure(0, weight=1)
        modifierFrame.columnconfigure(0, weight=0)
        modifierFrame.columnconfigure(1, weight=0)
        modifierFrame.columnconfigure(2, weight=0)
        modifierFrame.columnconfigure(3, weight=0)
        modifierFrame.columnconfigure(4, weight=1)

        modifierFrame.pack(expand=1, fill="both")

        self.modifierInitialLoad()
    
    def create_enemiestab(self):
        self.enemytab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.enemytab, text = "  Enemies  ")
    
    def _close_button_event(self):
        self.window_is_open = False
        self.master.destroy()

    def newFile(self):
        pass

    def openFile(self):
        pass

    def savePack(self):
        pass

    def saveModifier(self):
        currentModifierData = {}
        currentModifierData["name"] = self.modifierGetModName()
        currentModifierData["desc"] = self.modifierGetModDesc()
        currentModifierData["effect"] = self.modEffect.get()
        currentModifierData["strength"] = self.modStrength.get()
        print(currentModifierData)
        currentModifierId = list(self.currentOpenCollection.keys())[self.selectedModifier]
        newModifierID = self.modId.get()
        if (currentModifierId != newModifierID):
            self.currentOpenCollection[newModifierID] = currentModifierData
            del self.currentOpenCollection[currentModifierId]
        else:
            self.currentOpenCollection[newModifierID] = currentModifierData
        modifierFiles = self.metaFileData["modifiers"]
        print ((self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json", self.currentOpenCollection))
        saveJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json", self.currentOpenCollection)

    def menuHelp(self):
        pass

    def menuAbout(self):
        pass

    def newModifierFile(self):
        pass
    
    def delModifierFile(self):
        pass

    def metadataGameDescFill(self):
        self.gameDesc.delete('1.0', END)
        lines = self.metaFileData["gameDesc"]
        self.gameDesc.insert(END, "{}".format(lines.pop(0)))
        for line in lines:
            self.gameDesc.insert(END, "\n{}".format(line))
    
    def metadataGameDescGet(self):
        lines = self.gameDesc.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]
    
    def modifierInitialLoad(self):
        self.modifierLoadCollection(0)
    
    def _modifierLoadCollection(self, *args):
        if len(self.modifierFiles.curselection()) == 1:
            idx = self.modifierFiles.curselection()[0]
            if (idx != self.selectedModFile):
                self.modifierLoadCollection(idx)
    
    def modifierLoadCollection(self, idx):
        self.selectedModFile = idx

        modifierFiles = self.metaFileData["modifiers"]
        self.currentOpenCollection = loadJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json")

        self.modifierFilesList.set(modifierFiles)
        self.modifierFiles.selection_set(self.selectedModFile)
        self.modifierFiles.see(self.selectedModFile)

        self.modifierLoadModifier(0)
    
    def _modifierLoadModifier(self, *args):
        if len(self.modifierList.curselection()) == 1:
            idx = self.modifierList.curselection()[0]
            if (idx != self.selectedModifier):
                self.modifierLoadModifier(idx)
    
    def modifierLoadModifier(self, idx):
        self.selectedModifier = idx
        
        self.currentModifiersList.set(list(self.currentOpenCollection.keys()))
        self.modifierList.selection_set(self.selectedModifier)
        self.modifierList.see(self.selectedModifier)

        currentModifier = list(self.currentOpenCollection.keys())[self.selectedModifier]
        self.modId.delete(0, END)
        self.modId.insert(END, currentModifier)
        self.modifierSetModNameField(copy.copy(self.currentOpenCollection[currentModifier]["name"]))
        self.modifierSetModDescField(copy.copy(self.currentOpenCollection[currentModifier]["desc"]))
        self.modEffect.delete(0, END)
        self.modEffect.insert(END, self.currentOpenCollection[currentModifier]["effect"])
        self.modStrength.delete(0, END)
        self.modStrength.insert(END, self.currentOpenCollection[currentModifier]["strength"])
    
    def modifierSetModNameField(self, lines):
        self.modName.delete("1.0", END)
        if (len(lines)>=1):
            self.modName.insert(END, lines.pop(0))
        for line in lines:
            self.modName.insert(END, "\n" + line)

    def modifierGetModName(self):
        lines = self.modName.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]

    def modifierSetModDescField(self, lines):
        self.modDesc.delete("1.0", END)
        if (len(lines)>=1):
            self.modDesc.insert(END, lines.pop(0))
        for line in lines:
            self.modDesc.insert(END, "\n" + line)
    
    def modifierGetModDesc(self):
        lines = self.modDesc.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]
        
        


# Setup Constansts
RES_FOLDER = "res/"
SETTINGS_FILE = RES_FOLDER + "settings.json"


# Load settings file
settings = loadJson(SETTINGS_FILE)


# Get datapacks info
dataPackSettings = {}
for setting in settings["DATAPACKSETTINGS"].keys():
    dataPackSettings[setting] = settings["DATAPACKSETTINGS"][setting]

allPacks = dataPackSettings["packsToLoad"]
initialDataPack = dataPackSettings["start"]


# Load metadata file
metaFile = "%s%s/meta.json" % (RES_FOLDER, initialDataPack)

appWindow = MetaDataEditor(RES_FOLDER+initialDataPack, settings)
appWindow.initiate_window()

