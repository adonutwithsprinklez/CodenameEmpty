

# Official imports
import copy
import os
from email import message
from struct import pack
from tkinter import font
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, messagebox
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
        self.font = font.Font(family="courier", size=12)
        self.fontText = font.Font(family="courier", size=10)
        self.fontBold = font.Font(family="courier", size=12, weight=font.BOLD)

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
        self.create_enemiestab()
        self.create_modifiertab()
        self.create_weaponstab()
        # self.create_areastab()
        # self.create_armorstab()
        # self.create_eventstab()
        # self.create_misctab()
        # self.create_npcstab()
        # self.create_queststab()
        # self.create_racestab()

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

        Button(metadataFrame, text="Update Metadata", command=self.savePack, font=self.font).grid(row=6,column=0, columnspan=3, sticky=E+W)

        self.packName = Entry(metadataFrame, font=self.fontText)
        self.packAuth = Entry(metadataFrame, font=self.fontText)
        self.packDesc = Entry(metadataFrame, font=self.fontText)
        self.packType = Entry(metadataFrame, font=self.fontText)
        self.packVers = Entry(metadataFrame, font=self.fontText)
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
        self.gameDesc.configure(font=self.fontText, wrap='none')
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

        canvas = tk.Canvas(self.modifiertab)
        
        modifierFrame = ttk.Frame(canvas)
        modifierFrame.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=E+W+N+S)

        # ELEMENT CREATION
        # Files display
        self.modifierFilesList = StringVar(value=[])
        modifierFilesFrame = Frame(modifierFrame)
        modifierFilesFrame.grid(row=0, column=0, sticky=N+E+W+S)
        ttk.Label(modifierFilesFrame, text="Collections", font=self.fontBold).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.modifierFiles = Listbox(modifierFilesFrame, listvariable=self.modifierFilesList, font=self.fontText)
        self.modifierFiles.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.modifierFiles.bind("<<ListboxSelect>>", self._modifierLoadCollection)
        Button(modifierFilesFrame, text="-", command=self.delModifierFile, font=self.font).grid(row=2, column=0, sticky=N+S+W+E)
        Button(modifierFilesFrame, text="+", command=self.newModifierFile, font=self.font).grid(row=2, column=1, sticky=N+S+W+E)

        modifierFilesFrame.rowconfigure(1, weight=1)
        modifierFilesFrame.columnconfigure(0, weight=1)
        modifierFilesFrame.columnconfigure(1, weight=1)

        # Modifier List Display
        self.currentModifiersList = StringVar(value=[])
        seperator = ttk.Separator(modifierFrame, orient=VERTICAL)
        seperator.grid(row=0, column=1, stick=N+S)
        modifiersListFrame = Frame(modifierFrame)
        modifiersListFrame.grid(row=0, column=2, sticky=N+E+W+S)

        ttk.Label(modifiersListFrame, text="Modifiers", font=self.fontBold  ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.modifierList = Listbox(modifiersListFrame, listvariable=self.currentModifiersList,  font=self.fontText)
        self.modifierList.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.modifierList.bind("<<ListboxSelect>>", self._modifierLoadModifier)
        Button(modifiersListFrame, text="-", command=self.delSelectedModifier, font=self.font).grid(row=2, column=0, sticky=N+S+W+E)
        Button(modifiersListFrame, text="+", command=self.newModifier, font=self.font).grid(row=2, column=1, sticky=N+S+W+E)

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
        ttk.Label(modifierDataFrame, text="Strength", font=self.font).grid(row=4, column=0, padx=10, pady=5, sticky=E+N)

        self.modId = Entry(modifierDataFrame, font=self.fontText)
        self.modName = Text(modifierDataFrame, height=3, font=self.fontText)
        self.modDesc = Text(modifierDataFrame, height=3, font=self.fontText)
        self.modEffect = Entry(modifierDataFrame, font=self.fontText)
        self.modStrength = Entry(modifierDataFrame, font=self.fontText)
        saveModifier = Button(modifierDataFrame, text="Save", command=self.saveModifier, font=self.font)

        self.modId.grid(row=0, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modName.grid(row=1, column=1, columnspan=1, padx=10, pady=5, sticky=N+S+E+W)
        self.modDesc.grid(row=2, column=1, columnspan=1, padx=10, pady=5, sticky=N+S+E+W)
        self.modEffect.grid(row=3, column=1, columnspan=1, padx=10, pady=5, sticky=E+W)
        self.modStrength.grid(row=4, column=1, columnspan=1, padx=10, pady=5, sticky=N+E+W)
        saveModifier.grid(row=5, column=0, columnspan=2, sticky=E+W)
        # self.packName.insert(END, self.metaFileData["name"])

        self.modName.configure(wrap='none')
        self.modDesc.configure(wrap='none')

        modifierDataFrame.columnconfigure(1, weight=1)
        modifierDataFrame.rowconfigure(1, weight=1)
        modifierDataFrame.rowconfigure(2, weight=1)


        # FINISHING TOUCHES
        canvas.create_window((0, 0), window=modifierFrame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        modifierFrame.rowconfigure(0, weight=1)
        modifierFrame.columnconfigure(0, weight=1)
        modifierFrame.columnconfigure(1, weight=0)
        modifierFrame.columnconfigure(2, weight=1)
        modifierFrame.columnconfigure(3, weight=0)
        modifierFrame.columnconfigure(4, weight=10)

        modifierFrame.pack(expand=1, fill="both")

        self.modifierInitialLoad()
    
    def create_enemiestab(self):
        self.enemytab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.enemytab, text = "  Enemies  ")

        enemyFrame = ttk.Frame(self.enemytab)
        enemyFrame.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky=E+W+N+S)
        
        # ELEMENT CREATION
        # Files display
        self.enemyFileList = StringVar(value=[])
        enemyFileFrame = Frame(enemyFrame)
        enemyFileFrame.grid(row=0, column=0, sticky=N+E+W+S)
        ttk.Label(enemyFileFrame, text="Enemies", font=self.font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.enemyFiles = Listbox(enemyFileFrame, listvariable=self.enemyFileList, font=self.fontText)
        self.enemyFiles.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.enemyFiles.bind("<<ListboxSelect>>", self._enemyLoadSelection)
        Button(enemyFileFrame, text="-", command=self.delEnemy, font=self.font).grid(row=2, column=0, sticky=N+S+W+E)
        Button(enemyFileFrame, text="+", command=self.newEnemy, font=self.font).grid(row=2, column=1, sticky=N+S+W+E)

        ttk.Separator(enemyFrame, orient=VERTICAL).grid(row=0, column=1, columnspan=1, sticky=N+S)

        enemyFileFrame.rowconfigure(1, weight=1)
        enemyFileFrame.columnconfigure(0, weight=1)
        enemyFileFrame.columnconfigure(1, weight=1)

        enemyFrame.rowconfigure(0, weight=1)
        enemyFrame.columnconfigure(0, weight=1)
        enemyFrame.columnconfigure(1, weight=0)
        enemyFrame.columnconfigure(2, weight=5)

        self.enemytab.rowconfigure(0, weight=1)
        self.enemytab.columnconfigure(0, weight=1)

    def create_weaponstab(self):
        self.weapontab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.weapontab, text = "  Weapons  ")

        weaponFrame = ttk.Frame(self.weapontab)
        weaponFrame.grid(row=0, column=0, columnspan=1, padx=0, pady=0, sticky=E+W+N+S)

        # ELEMENT CREATION
        # Files display
        self.weaponFileList = StringVar(value=[])
        weaponFileFrame = Frame(weaponFrame)
        weaponFileFrame.grid(row=0, column=0, sticky=N+E+W+S)
        ttk.Label(weaponFileFrame, text="Weapons", font=self.font).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+W+E)
        self.weaponFiles = Listbox(weaponFileFrame, listvariable=self.weaponFileList, font=self.fontText)
        self.weaponFiles.grid(row=1, column=0, columnspan=2, sticky=N+S+W+E)
        self.weaponFiles.bind("<<ListboxSelect>>", self._weaponLoadSelection)
        Button(weaponFileFrame, text="-", command=self.delWeapon, font=self.font).grid(row=2, column=0, sticky=N+S+W+E)
        Button(weaponFileFrame, text="+", command=self.newWeapon, font=self.font).grid(row=2, column=1, sticky=N+S+W+E)

        ttk.Separator(weaponFrame, orient=VERTICAL).grid(row=0, column=1, columnspan=1, sticky=N+S)

        weaponFileFrame.rowconfigure(1, weight=1)
        weaponFileFrame.columnconfigure(0, weight=1)
        weaponFileFrame.columnconfigure(1, weight=1)

        # Data display
        weaponDataFrame = Frame(weaponFrame)
        weaponDataFrame.grid(row=0, column=2, sticky=N+E+W+S)

        ttk.Label(weaponDataFrame, text="Weapon ID", font=self.fontBold).grid(row=0, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Name", font=self.fontBold).grid(row=1, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Description", font=self.fontBold).grid(row=2, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Action Text", font=self.fontBold).grid(row=3, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Damage", font=self.fontBold).grid(row=4, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Num Hands", font=self.font).grid(row=4, column=2, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Min Worth", font=self.font).grid(row=5, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Max Worth", font=self.font).grid(row=5, column=2, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Mod Chance", font=self.font).grid(row=6, column=0, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Mod Count", font=self.font).grid(row=6, column=2, padx=10, pady=5, sticky=E)
        ttk.Label(weaponDataFrame, text="Mods", font=self.font).grid(row=7, column=0, padx=10, pady=5, sticky=E+N)

        self.wepId = Entry(weaponDataFrame, font=self.fontText)
        self.wepName = Text(weaponDataFrame, height=3, font=self.fontText)
        self.wepDesc = Text(weaponDataFrame, height=3, font=self.fontText)
        self.wepActionText = Text(weaponDataFrame, height=3, font=self.fontText)
        self.wepDmg = Entry(weaponDataFrame, font=self.fontText)
        self.wepHand = Entry(weaponDataFrame, font=self.fontText)
        self.wepWorMin = Entry(weaponDataFrame, font=self.fontText)
        self.wepWorMax = Entry(weaponDataFrame, font=self.fontText)
        self.wepModChance = Entry(weaponDataFrame, font=self.fontText)
        self.wepModCnt = Entry(weaponDataFrame, font=self.fontText)
        self.wepMods = Text(weaponDataFrame, height=3, font=self.fontText)

        self.wepId.grid(row=0, column=1, columnspan=2, padx=0, pady=5, sticky=W+E)
        self.wepName.grid(row=1, column=1, columnspan=3, padx=0, pady=5, sticky=N+S+W)
        self.wepDesc.grid(row=2, column=1, columnspan=3, padx=0, pady=5, sticky=N+S+W+E)
        self.wepActionText.grid(row=3, column=1, columnspan=3, padx=0, pady=5, sticky=N+S+W+E)
        self.wepDmg.grid(row=4, column=1, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepHand.grid(row=4, column=3, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepWorMin.grid(row=5, column=1, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepWorMax.grid(row=5, column=3, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepModChance.grid(row=6, column=1, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepModCnt.grid(row=6, column=3, columnspan=1, padx=0, pady=5, sticky=W)
        self.wepMods.grid(row=7, column=1, columnspan=3, padx=0, pady=5, sticky=N+S+W+N)

        Button(weaponDataFrame, text="Save", command=self.saveWeapon, font=self.font).grid(row=8, column=0, columnspan=4, sticky=N+E+W+S)

        weaponDataFrame.rowconfigure(1, weight=1)
        weaponDataFrame.rowconfigure(2, weight=1)
        weaponDataFrame.rowconfigure(3, weight=1)
        weaponDataFrame.rowconfigure(7, weight=1)
        weaponDataFrame.columnconfigure(3, weight=1)
        
        weaponFrame.rowconfigure(0, weight=1)
        weaponFrame.columnconfigure(0, weight=1)
        weaponFrame.columnconfigure(1, weight=0)
        weaponFrame.columnconfigure(2, weight=5)

        self.weapontab.rowconfigure(0, weight=1)
        self.weapontab.columnconfigure(0, weight=1)

        self.weaponInitialLoad()
    
    def create_areastab(self):
        self.areatab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.areatab, text = "  Areas  ")
    
    def create_armorstab(self):
        self.armortab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.armortab, text = "  Armors  ")
    
    def create_eventstab(self):
        self.eventtab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.eventtab, text = "  Events  ")
    
    def create_misctab(self):
        self.misctab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.misctab, text = "  Misc  ")
    
    def create_npcstab(self):
        self.npcstab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.npcstab, text = "  NPCs  ")
    
    def create_queststab(self):
        self.queststab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.queststab, text = "  Quests  ")
    
    def create_racestab(self):
        self.racetab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.racetab, text = "  Races  ")
    
    def _close_button_event(self):
        self.window_is_open = False
        self.master.destroy()

    def newFile(self):
        pass

    def openFile(self):
        pass

    def savePack(self):
        packType = self.packType.get()
        packVers = self.packVers.get()

        self.metaFileData["name"] = self.packName.get()
        self.metaFileData["author"] = self.packAuth.get()
        self.metaFileData["desc"] = self.packDesc.get()
        self.metaFileData["packType"] = self.packType.get()
        try:
            version = self.packVers.get()
            version = float(version)
            self.metaFileData["version"] = version
        except:
            pass
        self.metaFileData["gameDesc"] = self.metadataGameDescGet()

        saveJson(self.fileLoc+"/meta.json", self.metaFileData)
        

    def saveModifier(self):
        currentModifierData = {}
        currentModifierData["name"] = self.modifierGetModName()
        currentModifierData["desc"] = self.modifierGetModDesc()
        currentModifierData["effect"] = self.modEffect.get()
        currentModifierData["strength"] = self.modStrength.get()
        currentModifierId = list(self.currentOpenCollection.keys())[self.selectedModifier]
        newModifierID = self.modId.get()
        if (currentModifierId != newModifierID):
            self.currentOpenCollection[newModifierID] = currentModifierData
            del self.currentOpenCollection[currentModifierId]
        else:
            self.currentOpenCollection[newModifierID] = currentModifierData
        modifierFiles = self.metaFileData["modifiers"]
        saveJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json", self.currentOpenCollection)
        self.modifierLoadCollection(self.selectedModFile)
        self.selectedModifier = list(self.currentOpenCollection.keys()).index(newModifierID)
        self.modifierLoadModifier(self.selectedModifier)

    def menuHelp(self):
        pass

    def menuAbout(self):
        pass

    def _enemyLoadSelection(self):
        pass

    def delEnemy(self):
        pass

    def newEnemy(self):
        pass

    def newModifierFile(self):
        newfilename = simpledialog.askstring("Modifier Collection Name", "Enter new modifier collection name", parent=self.master)
        if (newfilename):
            newfilename = newfilename.strip()
        if (newfilename and newfilename not in self.metaFileData["modifiers"]):
            saveJson(self.fileLoc+"/modifiers/"+newfilename+".json", {})
            self.metaFileData["modifiers"].append(newfilename)
            self.metaFileData["modifiers"] = sorted(self.metaFileData["modifiers"])
            saveJson(self.fileLoc+"/meta.json", self.metaFileData)
            self.modifierLoadCollection(self.metaFileData["modifiers"].index(newfilename))

    
    def delModifierFile(self):
        confirmation = messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete the current Modifier Collection? All modifiers in this collection will be deleted.\
            \nThis cannot be undone.")
        if (confirmation):
            collectionId = self.metaFileData["modifiers"].pop(self.selectedModFile)
            os.remove(self.fileLoc+"/modifiers/"+collectionId+".json")
            saveJson(self.fileLoc+"/meta.json", self.metaFileData)
            self.modifierLoadCollection(0)

    def delSelectedModifier(self):
        if (len(list(self.currentOpenCollection.keys())) > 0):
            confirmation = messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete the current Modifier?\
                \nThis cannot be undone.")
            if (confirmation):
                currentModifierId = list(self.currentOpenCollection.keys())[self.selectedModifier]
                del self.currentOpenCollection[currentModifierId]
                modifierFiles = self.metaFileData["modifiers"]
                saveJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json", self.currentOpenCollection)
                self.modifierLoadCollection(self.selectedModFile)  

    def newModifier(self):
        newModId = "UNNAMEDMODIFIER"
        if (newModId not in list(self.currentOpenCollection.keys())):
            newModifierData = {
                "name":[],
                "desc":[],
                "effect":"",
                "strength":""
            }
            self.currentOpenCollection[newModId] = newModifierData
            modifierFiles = self.metaFileData["modifiers"]
            saveJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json", self.currentOpenCollection)
            self.modifierLoadCollection(self.selectedModFile)
            self.selectedModifier = list(self.currentOpenCollection.keys()).index(newModId)
            

    def metadataGameDescFill(self):
        self.gameDesc.delete('1.0', END)
        lines = copy.copy(self.metaFileData["gameDesc"])
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
        self.currentOpenCollection = dict(sorted(loadJson(self.fileLoc+"/modifiers/"+modifierFiles[self.selectedModFile]+".json").items()))

        self.modifierFilesList.set(modifierFiles)
        self.modifierFiles.selection_clear(0, END)
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
        self.modifierList.selection_clear(0, END)
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

    def weaponInitialLoad(self):
        self.weaponLoadSelection(0)

    def _weaponLoadSelection(self, *args):
        if (len(self.weaponFiles.curselection()) == 1):
            idx = self.weaponFiles.curselection()[0]
            if (idx != self.selectedWeapon):
                self.weaponLoadSelection(idx)

    def weaponLoadSelection(self, idx):
        self.selectedWeapon = idx
        weaponFiles = self.metaFileData["weapons"]
        self.weaponFileList.set(weaponFiles)
        self.wepId.delete(0,END)
        self.wepId.insert(0, weaponFiles[self.selectedWeapon])
        self.currentWeapon = loadJson(self.fileLoc+"/weapons/"+weaponFiles[self.selectedWeapon]+".json")
        self.weaponSetNameField(self.currentWeapon["name"])
        self.weaponSetDescField(self.currentWeapon["desc"])
        self.weaponSetActionField(self.currentWeapon["actionText"])
        self.wepDmg.delete(0,END)
        self.wepDmg.insert(0, self.currentWeapon["damage"])
        self.wepHand.delete(0,END)
        if ("requiredHands" in self.currentWeapon.keys()):
            self.wepHand.insert(0, self.currentWeapon["requiredHands"])
        self.wepWorMin.delete(0,END)
        if ("worthMin" in self.currentWeapon.keys()):
            self.wepWorMin.insert(0, self.currentWeapon["worthMin"])
        self.wepWorMax.delete(0,END)
        if ("worthMax" in self.currentWeapon.keys()):
            self.wepWorMax.insert(0, self.currentWeapon["worthMax"])
        self.wepModChance.delete(0,END)
        if ("modifierChance" in self.currentWeapon.keys()):
            self.wepModChance.insert(0, self.currentWeapon["modifierChance"])
        self.wepModCnt.delete(0,END)
        if ("modifierCount" in self.currentWeapon.keys()):
            self.wepModCnt.insert(0, self.currentWeapon["modifierCount"])
        if ("modifiers" in self.currentWeapon.keys()):
            self.weaponSetModField(self.currentWeapon["modifiers"])
        else:
            self.weaponSetModField([])
        
    
    def saveWeapon(self):
        wepId = self.wepId.get().strip()

        self.currentWeapon = {}
        self.currentWeapon["name"] = self.weaponGetNameField()
        self.currentWeapon["damage"] = self.wepDmg.get()
        self.currentWeapon["desc"] = self.weaponGetDescField()
        self.currentWeapon["actionText"] = self.weaponGetActionField()
        if (self.wepModCnt.get().strip()):
            self.currentWeapon["modifierCount"] = self.wepModCnt.get().strip()
            self.currentWeapon["modifiers"] = self.weaponGetModField()
            if (self.wepModChance.get.strip()):
                try:
                    self.currentWeapon["modifierChance"] = int(self.wepModChance.get.strip())
                except:
                    pass
        if (self.wepWorMin.get().strip()):
            try:
                self.currentWeapon["worthMin"] = int(self.wepWorMin.get().strip())
            except:
                pass
        if (self.wepWorMax.get().strip()):
            try:
                self.currentWeapon["worthMax"] = int(self.wepWorMax.get().strip())
            except:
                pass
        if (self.wepHand.get().strip()):
            try:
                self.currentWeapon["requiredHands"] = int(self.wepHand.get().strip())
            except:
                pass
        
        # Check if weapon ID changed, update if needed
        if (wepId != self.metaFileData["weapons"][self.selectedWeapon]):
            oldID = self.metaFileData["weapons"].pop(self.selectedWeapon)
            self.metaFileData["weapons"].append(wepId)
            self.metaFileData["weapons"] = sorted(self.metaFileData["weapons"])
            self.selectedWeapon = self.metaFileData["weapons"].index(wepId)
            os.remove("{}/weapons/{}.json".format(self.fileLoc, oldID))
        saveJson("{}/weapons/{}.json".format(self.fileLoc, wepId), self.currentWeapon)
        self.weaponLoadSelection(self.selectedWeapon)

    def delWeapon(self):
        weaponId = self.metaFileData["weapons"][self.selectedWeapon]
        confirmation = messagebox.askokcancel("Confirm Delete", "Are you sure you want to delete %s?\
            \nThis cannot be undone." % (weaponId))
        if (confirmation):
            self.metaFileData["weapons"].pop(self.selectedWeapon)
            saveJson(self.fileLoc+"/meta.json", self.metaFileData)
            os.remove("{}/weapons/{}.json".format(self.fileLoc, weaponId))
            self.weaponLoadSelection(0)

    def newWeapon(self):
        newfilename = simpledialog.askstring("New Weapon ID", "Enter new modifier collection name", parent=self.master)
        if (newfilename):
            newfilename = newfilename.strip()
        if (newfilename and newfilename not in self.metaFileData["weapons"]):
            newWeaponData = {
                "name":[],
                "desc":[],
                "damage":[],
                "actionText":[]
            }
            saveJson(self.fileLoc+"/weapons/"+newfilename+".json", newWeaponData)
            self.metaFileData["weapons"].append(newfilename)
            self.metaFileData["weapons"] = sorted(self.metaFileData["weapons"])
            saveJson(self.fileLoc+"/meta.json", self.metaFileData)
            idx = self.metaFileData["weapons"].index(newfilename)
            self.weaponLoadSelection(idx)

    def weaponSetNameField(self, lines):
        self.wepName.delete("1.0", END)
        if (len(lines)>=1):
            self.wepName.insert(END, lines.pop(0))
        for line in lines:
            self.wepName.insert(END, "\n" + line)
    
    def weaponGetNameField(self):
        lines = self.wepName.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]

    def weaponSetDescField(self, lines):
        self.wepDesc.delete("1.0", END)
        if (len(lines)>=1):
            self.wepDesc.insert(END, lines.pop(0))
        for line in lines:
            self.wepDesc.insert(END, "\n" + line)
    
    def weaponGetDescField(self):
        lines = self.wepDesc.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]

    def weaponSetActionField(self, lines):
        self.wepActionText.delete("1.0", END)
        if (len(lines)>=1):
            self.wepActionText.insert(END, lines.pop(0))
        for line in lines:
            self.wepActionText.insert(END, "\n" + line)
    
    def weaponGetActionField(self):
        lines = self.wepActionText.get('1.0',END).split("\n")
        return [line for line in lines if line.strip()]

    def weaponSetModField(self, lines):
        self.wepMods.delete("1.0", END)
        if (len(lines)>=1):
            m = lines.pop(0)
            self.wepMods.insert(END, "{}, {}".format(m[0], m[1]))
        for line in lines:
            self.wepMods.insert(END, "\n{}, {}".format(line[0], line[1]))
    
    def weaponGetModField(self):
        lines = self.wepMods.get('1.0',END).split("\n")
        lines = [line for line in lines if line.strip()]
        modsList = []
        for line in lines:
            try:
                line = line.split(",")
                modEffect = line[0].strip()
                modLiklihood = line[1].strip()
                modsList.append([modEffect,modLiklihood])
            except:
                pass
        return modsList

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

