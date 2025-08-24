'''
An app that where you can make your own perfume.
Version 1: basic working program, functions, no optimisations, no validation at all
'''

# Import modules
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import json

class FrameManager(Tk):
    '''This class serves as the main application window and it controls the switching between all frames'''
    def __init__(self):
        super().__init__()
        self.title("Perfuminator") 
        self.minsize(800, 550)
        
        # Takes up whole space and resizes with expanding
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialises dictionaries to store important
        self.scent_notes_data = {}  # Stores data for individual scent notes from the JSON file
        self.palettes_data = {}     # Stores data for preset scent palettes from the JSON file
        self.scent_totals = {}      # Stores the calculated totals of scent attributes to be passed to the checkout frame
        self.load_scent_data("scent_data.json")

        # Container frame to hold all the frames in it
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        # Places the container in the main window's grid, fills entire grid
        self.container.grid(row=0, column=0, sticky=NSEW)

        # A dictionary to hold each frame
        self.frames = {}
        # Creates instances of the initial frames and adds them to the dictionary
        # self.container is the parent widget for these frames, and 'self' is the controller. --> Very imporant for structuring 
        self.frames["MainMenu"] = MainMenu(self.container, self)
        self.frames["PaletteSelector"] = PaletteSelector(self.container, self)
        self.frames["Checkout"] = Checkout(self.container, self)

        # MainGame is initialised as None as it will be created based on free reign or palette choice
        self.frames["MainGame"] = None

        # Displays the MainMenu frame first
        self.show_frame("MainMenu")

    def load_scent_data(self, filename="scent_data.json"):
        '''Loads scent notes and palettes from a JSON file'''
        with open(filename, 'r') as f:
            data = json.load(f)
            self.scent_notes_data = data.get("scent_notes", {}) 
            self.palettes_data = data.get("palettes", {})

    def show_frame(self, name):
        '''Display the required frame from the dictionary'''
        frame = self.frames[name]
        frame.tkraise()
    
    def start_main_game(self, palette_type):
        '''Initialises and displays the MainGame frame with the selected palette.'''
        if palette_type == "free_reign":
            selected_palette = list(self.scent_notes_data.keys()) #Loads all notes
        else:
            selected_palette = self.palettes_data.get(palette_type, []) #Loads specific palette

        # Remakes a new instance of the the 'MainGame' frame with the selected palett
        self.frames["MainGame"] = MainGame(self.container, self, selected_palette)
        self.frames["MainGame"].grid(row=0, column=0, sticky=NSEW)
        self.show_frame("MainGame")

# The MainMenu class represents the starting screen of the application
class MainMenu(Frame):
    '''MainMenu of the game, this is the starting screen which prompts the user into choosing if they want free-reign or a palette'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky=NSEW)

        # Configures the grid rows and columns of this frame to be resizable
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        for j in range(2):
            self.grid_columnconfigure(j, weight=1)      

        # Creates and places the main heading label
        heading = Label(self, text="Welcome to the Perfuminator", font="Verdana 16 bold")
        heading.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # Loads and displays image
        self.image = PhotoImage(file="placeholder.png")
        image_label = Label(self, image=self.image)
        image_label.grid(row=1, column=0, pady=10, sticky="NSEW", columnspan=2)

        main_menu_text = Label(self, text="would you like to choose from", font="Verdana 11")
        main_menu_text.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=(50, 0))

        #Buttons for free reign and palette, commands takes them to their respective frames
        free_reign_button = Button(self, text="Free Reign", bg="lightgreen", font="Verdana 12 bold", command=lambda: self.controller.start_main_game("free_reign"))
        free_reign_button.grid(row=3, column=0, sticky=NSEW)

        preset_palette_button = Button(self, text="Preset Palette", bg="yellow", font="Verdana 12 bold", command=lambda: self.controller.show_frame("PaletteSelector"))
        preset_palette_button.grid(row=3, column=1, sticky=NSEW)

class PaletteSelector(Frame):
    '''Palette Selector Frame, the user can choose from a preset palette'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky=NSEW)

        # Configures the grid of this frame to be resizable
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for j in range(1):
            self.grid_columnconfigure(j, weight=1)    

        # Heading
        heading = Label(self, text="Our Premade Palettes", font="Verdana 16 bold")
        heading.grid(row=0, column=0, sticky=NSEW)

        # Creates buttons for each preset palette, each button's command calls `start_main_game` with a different palette name
        summer_palette_button = Button(self, text="Summer Palette (more fruity scents)", bg="yellow", font="Verdana 12 bold", command=lambda: self.controller.start_main_game("summer"))
        summer_palette_button.grid(row=1, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        outdoors_palette_button = Button(self, text="Outdoors Palette (more woody scents)", bg="forest green", font="Verdana 12 bold", command=lambda: self.controller.start_main_game("outdoors"))
        outdoors_palette_button.grid(row=2, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        candy_palette_button = Button(self, text="Candy Palette (more sweet scents)", bg="hot pink", font="Verdana 12 bold", command=lambda: self.controller.start_main_game("candy"))
        candy_palette_button.grid(row=3, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        zesty_palette_button = Button(self, text="Zesty Palette (more Citrusy scents)", bg="orange", font="Verdana 12 bold", command=lambda: self.controller.start_main_game("zesty"))
        zesty_palette_button.grid(row=4, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        # Button to go back to MainMenu
        back_button = Button(self, text="BACK", bg="gray", font="Verdana 12 bold", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.grid(row=5, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

class MainGame(Frame):
    '''Main Game Class, This class is where the user will choose the scents for their perfume'''
    def __init__(self, parent, controller, scent_palette):
        super().__init__(parent)
        self.controller = controller
        # Stores the list of scents available from their choice 
        self.scent_palette = scent_palette
        # Defines the attributes for each scent
        self.attributes = ["fruity", "sweet", "citrus", "woody"]

        self.selected_scents=[]
        
        # Creates a list of `StringVar` objects to hold the selected scent names from the comboboxes
        self.selected_scent_vars = []
        for i in range(3):
            self.selected_scent_vars.append(StringVar(value=""))

        # Configures the main grid for this frame
        self.grid_columnconfigure(0, weight=4)  # Left column (scent boxes) gets more space
        self.grid_columnconfigure(1, weight=1)  # Right column (selectors, totals) gets less space
        self.grid_rowconfigure(1, weight=1)     # Allows the totals to expand

        # A Frame to contain the scrollable list of scent notes
        scents_container = Frame(self)
        scents_container.grid(row=0, column=0, rowspan=3, sticky="NSEW", padx=10, pady=10)
        scents_container.grid_rowconfigure(0, weight=1)
        scents_container.grid_columnconfigure(0, weight=1)

        # Creates a  widget, which is necessary for adding a scrollbar
        self.canvas = Canvas(scents_container)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        # Creates a vertical scrollbar and links it to the canvas and links the canvas to the scrollbar
        vertical_scrollbar = Scrollbar(scents_container, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky=NS)
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)

        self.scents_grid_frame = Frame(self.canvas)

        # Creates a window in the canvas to hold the frame
        self.window_scroll = self.canvas.create_window((0, 0), window=self.scents_grid_frame, anchor="nw")
        # Binds configure events on the fame to adjust the scroll region, and adjust width of inner window
        self.scents_grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.create_scent_boxes_grid(columns=4)

        # A LabelFrame widget to group the scent selection comboboxes
        selectors_labelframe = LabelFrame(self, text="Select 3 Scents", padx=10, pady=10)
        selectors_labelframe.grid(row=0, column=1, sticky="NWE", padx=10, pady=10)
        selectors_labelframe.grid_columnconfigure(0, weight=1)

        # Loops to create three sets of labels and comboboxes
        for i in range(3):
            label = Label(selectors_labelframe, text=(f"Scent {i + 1}:"))
            label.grid(row=i * 2, column=0, sticky="W") #x2 as label on every other line


        # A LabelFrame for displaying the combined attribute totals
        totals_labelframe = LabelFrame(self, text="Combined Totals", padx=10, pady=10)
        totals_labelframe.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
        totals_labelframe.grid_columnconfigure(0, weight=1)
    
        self.total_labels = {}
        # Loops through each attributes to create a label for each one
        for i, attribute in enumerate(self.attributes):
            label = Label(totals_labelframe, text=f"{attribute.capitalize()}: 0", font=("Verdana", 10))
            label.grid(row=i, column=0, sticky="w", pady=(2, 2))
            self.total_labels[attribute] = label

        # A frame to hold the buttons and the buttons
        button_frame = Frame(self)
        button_frame.grid(row=2, column=1, sticky="NSEW", pady=(10,10), padx=(20,20))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        back_button = Button(button_frame, text="BACK", bg="gray", font="Verdana 12 bold", command=self.go_back)
        back_button.grid(row=0, column=0, sticky="NSEW", padx=(0, 5))
        
        reset_button = Button(button_frame, text="RESET", bg="orange", font="Verdana 12 bold", command=self.reset_selections)
        reset_button.grid(row=0, column=1, sticky="NSEW", padx=(5, 5))

        checkout_button = Button(button_frame, text="CHECKOUT", bg="lightgreen", font="Verdana 12 bold", command=self.go_to_checkout)
        checkout_button.grid(row=0, column=1, sticky="NSEW", padx=(5, 0))
    
    # def reset_selections(self):

    #     self.selected_scents = []
    #     for label in self.###:
    #         label.config(text=f"Scent {self.###.index(label) + 1}: (None)")
    #     self.update_totals()

    def go_to_checkout(self):
        '''This method is linked to the checkout button. It is  used to pass the totals for the checkout and raise the frame'''
        confirmation = messagebox.askyesno("Confirm Checkout", "Are you sure you want to proceed to checkout? You will not be able to change your notes")
        
        if confirmation:
            self.update_totals() #Update Totals before going to checkout
            # Creates a dictionary of the final totals by extracting the value from each label's text
            # Doing it this way ensures that the totals extracted are the same as the combined totals shown
            totals_to_pass = {attr: int(label.cget("text").split(": ")[1]) for attr, label in self.total_labels.items()}
            # Stores the final totals in the FrameManager to then access in checkout
            self.controller.scent_totals = totals_to_pass
            self.controller.show_frame("Checkout")

    def update_totals(self, event=None):
        '''This method is for when a scent is chosen using a combobox. It calculates each attributes values'''
        # Initializes a dictionary to store the totals for each attribute (all start at 0)
        totals = {attr: 0 for attr in self.attributes}
        
        for var in self.selected_scent_vars:
            # Gets the name of the selected scent
            scent_name = var.get()
            #If not empty, reads data and adds the values to EACH attributes totals
            if scent_name: #If not empty
                scent_data = self.controller.scent_notes_data.get(scent_name, {})
                for attr in self.attributes:
                    totals[attr] += scent_data.get(attr, 0)
        
        # Updates text
        for attr, total in totals.items():
            self.total_labels[attr].config(text=f"{attr.capitalize()}: {total}")

    def on_canvas_configure(self, event):
        '''This method is for when the canvas is resized'''
        # It updates the width of the scents_grid frame to match the canvas's width so nothing gets cut off
        canvas_width = event.width
        self.canvas.itemconfigure(self.window_scroll, width=canvas_width)

    def create_scent_boxes_grid(self, columns):
        '''This method crates all the boxes for all of the scents'''
        # Loops through each scent name in the selected palette
        for i, scent_name in enumerate(self.scent_palette):
            # Calculates the row and column for the scent box in the grid
            row_number = i // columns
            column_number = i % columns
            #Makes each 'box' is it's own frame and places it according to it's calculated row and column
            scent_box = Frame(self.scents_grid_frame, width=150, height=120, padx=5, pady=5, borderwidth=1, relief="solid") 
            scent_box.grid(row=row_number, column=column_number, sticky="NSEW", padx=5, pady=5)  
            scent_box.grid_propagate(False) #Prevents Resizing
            scent_box.grid_columnconfigure(0, weight=1)

            # Configures the rows inside the scent box to be resizable, depending on the name and attributes length
            for j in range(len(self.attributes) + 1):
                scent_box.grid_rowconfigure(j, weight=1)

            scent_name_label = Label(scent_box, text=scent_name, font=("Verdana", 10, "bold"))
            scent_name_label.grid(row=0, column=0, sticky="EW")

            # Gets attribute data and creates a label, for each one, displaying its value
            scent_attributes = self.controller.scent_notes_data.get(scent_name, {})
            
            for j, attribute in enumerate(self.attributes):
                value = scent_attributes.get(attribute)
                attribute_label = Label(scent_box, text=f"{attribute.capitalize()}: {value}")
                attribute_label.grid(row=j + 1, column=0, sticky="W")

            add_button = Button(scent_box, text="Add", bg="red", fg="black", font=("Verdana", 10, "bold"),
                                command="")
            add_button.grid(row=len(self.attributes) + 1, column=0, sticky="NSEW", pady=(5, 0))

        # Makes the columns and rows of the scents_grid_frame resizable
        for i in range(columns):
            self.scents_grid_frame.grid_columnconfigure(i, weight=1, minsize=100)
            self.scents_grid_frame.grid_rowconfigure(i, weight=1)

    def go_back(self):
        '''This method is linked to the back button. Depending if the user chose free reign or palette takes them back to that frame'''
        if self.scent_palette == list(self.controller.scent_notes_data.keys()):
            self.controller.show_frame("MainMenu")
        else:
            self.controller.show_frame("PaletteSelector")

class Checkout(Frame):
    '''Checkout Frame. This frame gets the user to pick a name for their perfume and then displays their final order'''
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky=NSEW)

        self.scent_name_var = StringVar()

        self.grid_columnconfigure(0, weight=1)
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)

        heading = Label(self, text="CHECKOUT", font=("Verdana", 24, "bold"))
        heading.grid(row=0, column=0, pady=(20, 10))

        # Loads and displays the image
        self.image = PhotoImage(file="placeholder.png")
        image_label = Label(self, image=self.image)
        image_label.grid(row=1, column=0, pady=10)

        # Creates a label and entry, prompting the user to name the scent
        name_label = Label(self, text="Name your scent!", font=("Verdana", 14))
        name_label.grid(row=2, column=0, pady=(20, 5))

        self.name_entry = Entry(self, textvariable=self.scent_name_var, width=50)
        self.name_entry.grid(row=3, column=0, pady=(0, 10))

        # Binds the return or enter key to the show_final_scent_name method, running it when it's pressed
        self.name_entry.bind("<Return>", self.show_final_scent_name)
        
        # A label to display the final scent name and totals
        self.final_scent_label = Label(self, text="", font=("Verdana", 12), justify=LEFT)
        self.final_scent_label.grid(row=4, column=0, sticky="w", padx=20, pady=10)
        
        self.final_totals_label = Label(self, text="", font=("Verdana", 10), justify=LEFT)
        self.final_totals_label.grid(row=5, column=0, sticky="w", padx=20, pady=5)

    def show_final_scent_name(self, event=None):
        '''This method updates the labels with the entered scent name and the combined totals.'''

        scent_name = self.scent_name_var.get()
        self.final_scent_label.config(text=f"Your Final Scent: {scent_name}")

        # Retrieves the scent totals from the FrameManager
        totals = self.controller.scent_totals

        #Puts each attribute and it's value on a seperate line and updates
        totals_text = "\n".join([f"{key.capitalize()}: {value}" for key, value in totals.items()]) 
        self.final_totals_label.config(text=totals_text)

# Runs and creates an instance of the Framemanager, which controls everything.
if __name__ == "__main__":
    app = FrameManager()
    app.mainloop()