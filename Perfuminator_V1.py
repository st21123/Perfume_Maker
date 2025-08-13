'''
An app that where you can make your own perfume

Version 1: basic working program, functions, no optimisations, no validation at all
 '''

from tkinter import *
from tkinter.ttk import Combobox
import json

class FrameManager(Tk):
    def __init__(self):
        super().__init__()
        self.title("Perfumantor")
        self.minsize(800,550)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.scent_notes_data ={}
        self.palettes_data ={}
        self.load_scent_data("scent_data.json")

        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames ={}
        self.frames["MainMenu"] = MainMenu(self.container, self)
        self.frames["PaletteSelector"] = PaletteSelector(self.container, self)
        self.frames["Checkout"] = Checkout(self.container, self)

        self.show_frame("MainMenu")

    def load_scent_data(self, filename):
        '''Loads scent notes and palettes from a JSON file.'''
        with open(filename, 'r') as f:
            data = json.load(f)
            self.scent_notes_data = data.get("scent_notes", {})
            self.palettes_data = data.get("palettes", {})

    def show_frame(self, name):
        '''Display the required frame from the dictionary'''
        frame = self.frames[name]
        frame.tkraise()
    
    def start_main_game(self, palette_type):
        '''Initializes and displays the MainGame frame with the selected palette.'''
        if palette_type == "free_reign":
            selected_palette = list(self.scent_notes_data.keys())
        else:
            selected_palette = self.palettes_data.get(palette_type, [])

        self.frames["MainGame"] = MainGame(self.container, self, selected_palette)
        self.frames["MainGame"].grid(row=0, column=0, sticky=NSEW)
        self.show_frame("MainGame")

class MainMenu:
    '''Set up the GUI'''
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky=NSEW)

        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.grid_columnconfigure(j, weight=1)       

        heading = Label(self, text="Welcome to the Perfumanator", font="Verdana 16 bold")
        heading.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        main_menu_text = Label(self, text="would you like to choose from", font="Verdana 11")
        main_menu_text.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=(50, 0))

        free_reign_button = Button(self, text="Free Reign", bg="lightgreen", font="Verdana 12 bold",command=lambda: self.start_main_game("free_reign"))
        free_reign_button.grid(row=3, column=0, sticky=NSEW)
    
        preset_palette_button= Button(self, text="Preset Palette", bg="yellow", font="Verdana 12 bold",command=lambda: self.show_frame("PaletteSelector"))
        preset_palette_button.grid(row=3, column=1, sticky=NSEW)

class PaletteSelector:
    pass
    # def create_palette_selector(self):
    #     frame = Frame(self.container)
    #     frame.grid(row=0, column=0, sticky=NSEW)

    #     for i in range(5):
    #         frame.grid_rowconfigure(i, weight=1)
    #     for j in range(1):
    #         frame.grid_columnconfigure(j, weight=1)    
        
    #     heading = Label(frame, text="Our Premade Palettes", font="Verdana 16 bold")
    #     heading.grid(row=0, column=0, sticky=NSEW)

    #     summer_palette_button= Button(frame, text="Summer Palette (more fruity scents)", bg="yellow", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
    #     summer_palette_button.grid(row=1, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

    #     outdoors_palette_button= Button(frame, text="Outdoors Palette (more woody scents)", bg="forest green", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
    #     outdoors_palette_button.grid(row=2, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

    #     candy_palette_button= Button(frame, text="Candy Palette (more sweet scents)", bg="hot pink", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
    #     candy_palette_button.grid(row=3, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

    #     zesty_palette_button= Button(frame, text="Zesty Palette (more Citrusy scents)", bg="orange", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
    #     zesty_palette_button.grid(row=4, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

    #     back_button= Button(frame, text="BACK", bg="gray", font="Verdana 12 bold",command=lambda: self.show_frame("MainMenu"))
    #     back_button.grid(row=5, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))
    #     return frame


class MainGame(Frame):
    def __init__(self, root, scent_palette):
        super().__init__(root)
        self.scent_palette = scent_palette
        self.attributes = ["fruity", "sweet", "citrus", "woody"]

        for i in range(3):
            self.selected_scent_vars = [StringVar(value="")]

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        #frame to hold canvas widget to create scrollbar and then frame inside canvas for the notes  ###ugly comment change it later when putting proper comments in
        scents_container = Frame(self)
        scents_container.grid(row=0, column=0, rowspan=3, sticky="NSEW", padx=10, pady=10)

        canvas = Canvas(scents_container)
        vertical_scrollbar = Scrollbar(scents_container, orient="vertical", command=canvas.yview)

        self.scents_grid_frame = Frame(canvas)

        canvas.create_window((0, 0), window=self.scents_grid_frame, anchor="NW") #keeps top left
        canvas.configure(yscrollcommand=vertical_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        vertical_scrollbar.pack(side="right", fill="y")

        self.create_scent_boxes_grid(columns=4) #### this def is not created yet

        selectors_labelframe = LabelFrame(self, text="Select 3 Scents", padx=10, pady=10)
        selectors_labelframe.grid(row=0, column=1, sticky="NWE", padx=10, pady=10)
        selectors_labelframe.grid_columnconfigure(0, weight=1)  # Allow comboboxes to expand horizontally

        self.comboboxes = []

        # 3 labels and comboboxes
        for i in range(3):
            label = Label(selectors_labelframe, text=(f"Scent {i + 1}:"))
            label.grid(row=i * 2, column=0, sticky="W") #x2 because label then combobox on then another label 2 rows down

            combobox = self.Combobox(selectors_labelframe, textvariable=self.selected_scent_vars[i], values=[""] + scent_palette, state="readonly", width=20)
            combobox.grid(row=i * 2 + 1, column=0, sticky="we", pady=2) #each created combobox is under each label

            self.comboboxes.append(combobox) #saves to list

        #combined totals labelframe
        totals_labelframe = LabelFrame(self, text="Combined Totals", padx=10, pady=10)
        totals_labelframe.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
        totals_labelframe.grid_columnconfigure(0, weight=1)
        totals_labelframe.grid_rowconfigure(0, weight=1)

class Checkout:
    pass

if __name__ == "__main__":
    app = FrameManager()
    app.mainloop()