'''
An app that where you can make your own perfume.
Version 1: basic working program, functions, no optimisations, no validation at all
Version 2: optimised for efficiency, aesthetic changes, proper sizing
Version 3: Added Validation
'''

# Import modules
from tkinter import *
from tkinter import messagebox
import json

class FrameManager(Tk):
    '''This class serves as the main application window and it controls the switching between all frames'''
    def __init__(self):
        super().__init__()
        self.title("Perfuminator") 
        self.minsize(850, 575)

        # Takes up whole space and resizes with expanding
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialises dictionaries to store important
        self.scent_notes_data = {}  # Stores data for individual scent notes from the JSON file
        self.palettes_data = {}     # Stores data for preset scent palettes from the JSON file
        self.scent_totals = {}      # Stores the calculated totals of scent attributes to be passed to the checkout frame
        self.selected_scent_names = []
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
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Checks if the necessary keys are found in the file
            if "scent_notes" not in data or "palettes" not in data:
                messagebox.showerror("Data Error", "JSON data file is missing required 'scent_notes' or 'palettes' keys.")
                self.destroy()
                return

            self.scent_notes_data = data.get("scent_notes", {}) 
            self.palettes_data = data.get("palettes", {})

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file '{filename}' was not found. Please ensure it is in the correct folder.")
            self.destroy()
        except json.JSONDecodeError:
            messagebox.showerror("JSON Error", f"The file '{filename}' is not a valid JSON file.")
            self.destroy()
            
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

        # Check if all scent notes in the palette exist in the main scent data.
        try:
            for scent in selected_palette:
                if scent not in self.scent_notes_data:
                    raise KeyError(f"Scent note '{scent}' from the '{palette_type}' palette is missing data.")
        except KeyError:
            messagebox.showerror("Some Data is missing from chosen pallete. Please doublecheck file")
            self.destroy()
            return
        
        # Remakes a new instance of the the 'MainGame' frame with the selected palett
        self.frames["MainGame"] = MainGame(self.container, self, selected_palette)
        self.frames["MainGame"].grid(row=0, column=0, sticky=NSEW)
        self.show_frame("MainGame")

class BaseFrame(Frame):
    '''Base class for all frames to handle common grid configurations'''
    def __init__(self, parent, controller, grid_rows, grid_columns):
        super().__init__(parent)
        self.controller = controller
        self.grid(row=0, column=0, sticky=NSEW)
        self.configuring_grid(grid_rows, grid_columns)

    # Configures based on given rows and columns
    def configuring_grid(self, rows, columns):
        for i in range(rows):
            self.grid_rowconfigure(i, weight=1)
        for j in range(columns):
            self.grid_columnconfigure(j, weight=1)

class MainMenu(BaseFrame):
    '''MainMenu of the game, this is the starting screen which prompts the user into choosing if they want free-reign or a palette'''
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 4, 2)

        # Creates and places the main heading label
        heading = Label(self, text="Welcome to the Perfuminator", font="Verdana 24 bold")
        heading.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # Loads and displays image
        self.image = PhotoImage(file="perfume.png")
        image_label = Label(self, image=self.image)
        image_label.grid(row=1, column=0, pady=10, sticky="NSEW", columnspan=2)

        main_menu_text = Label(self, text="would you like to choose from", font="Verdana 11")
        main_menu_text.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=(30, 0))

        #Buttons for free reign and palette, commands takes them to their respective frames
        free_reign_button = self.create_styled_button("Free Reign", "lightgreen", lambda: self.controller.start_main_game("free_reign"))
        free_reign_button.grid(row=3, column=0, sticky=NSEW)

        preset_palette_button = self.create_styled_button("Preset Palette", "yellow", lambda: self.controller.show_frame("PaletteSelector"))
        preset_palette_button.grid(row=3, column=1, sticky=NSEW)
    
    def create_styled_button(self, text, bg_color, command):
        '''This Method Simplifies the Button creation'''
        return Button(self, text=text, bg=bg_color, font="Verdana 12 bold", command=command)


class PaletteSelector(BaseFrame):
    '''Palette Selector Frame, the user can choose from a preset palette'''
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 6, 1)

        # Heading
        heading = Label(self, text="Our Premade Palettes", font="Verdana 24 bold")
        heading.grid(row=0, column=0, sticky=NSEW)

        # Creates buttons for each preset palette by calling method
        self.create_palette_button("Summer Palette (more fruity scents)", "yellow", "summer").grid(row=1, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))
        self.create_palette_button("Outdoors Palette (more woody scents)", "forest green", "outdoors").grid(row=2, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))
        self.create_palette_button("Candy Palette (more sweet scents)", "hot pink", "candy").grid(row=3, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))
        self.create_palette_button("Zesty Palette (more Citrusy scents)", "orange", "zesty").grid(row=4, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        # Button to go back to MainMenu
        back_button = Button(self, text="BACK TO MAIN MENU", bg="gray", font="Verdana 12 bold", command=lambda: self.controller.show_frame("MainMenu"))
        back_button.grid(row=5, column=0, sticky=NSEW, pady=(10,20), padx=(20,20))

    def create_palette_button(self, text, color, palette_name):
        return Button(self, text=text, bg=color, font="Verdana 12 bold", command=lambda: self.controller.start_main_game(palette_name))

class MainGame(Frame):
    '''Main Game Class, This class is where the user will choose the scents for their perfume'''
    def __init__(self, parent, controller, scent_palette):
        super().__init__(parent)
        self.controller = controller
        # Stores the list of scents available from their choice 
        self.scent_palette = scent_palette
        # Defines the attributes for each scent
        self.attributes = ["fruity", "sweet", "citrus", "woody"]
        
        self.selected_scents =[]

        # Configures the main grid for this frame
        self.grid_columnconfigure(0, weight=5)  # Left column (scent boxes) gets more space
        self.grid_columnconfigure(1, weight=1)  # Right column (selectors, totals) gets less space

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # A Frame to contain the scrollable list of scent notes
        scents_container = Frame(self)
        scents_container.grid(row=0, column=0, rowspan=3, sticky="NSEW", padx=10, pady=10)
        scents_container.grid_rowconfigure(0, weight=1)
        scents_container.grid_columnconfigure(0, weight=1)

        # Creates a  widget, which is necessary for adding a scrollbar
        self.canvas = Canvas(scents_container)
        self.canvas.grid(row=0, column=0, sticky=NSEW)

        # Creates a vertical scrollbar and links it to the canvas and links the canvas to the scrollbar
        vertical_scrollbar = Scrollbar(scents_container, orient="vertical", command=self.canvas.yview)
        vertical_scrollbar.grid(row=0, column=1, sticky=NS)

        self.scents_grid_frame = Frame(self.canvas)
        self.canvas.configure(yscrollcommand=vertical_scrollbar.set)

        # Creates a window in the canvas to hold the frame
        self.window_scroll = self.canvas.create_window((0, 0), window=self.scents_grid_frame, anchor="nw")
        # Binds configure events on the fame to adjust the scroll region, and adjust width of inner window
        self.scents_grid_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.create_scent_boxes_grid(columns=4)

        # A LabelFrame widget to group the selected scents
        selectors_labelframe = LabelFrame(self, text="Selected Scents", padx=10, pady=10)
        selectors_labelframe.grid(row=0, column=1, sticky="NSEW", padx=10, pady=10)
        selectors_labelframe.grid_columnconfigure(0, weight=1)

        #List to hold labels
        self.selected_scent_labels = []

        # Create Labels With Base Text
        for i in range(3):
            label = Label(selectors_labelframe, text=f"Scent {i + 1}: (None)", font=("Verdana", 12))
            label.grid(row=i, column=0, sticky="W", pady=2)
            self.selected_scent_labels.append(label)
        
        # A LabelFrame widget to group the totals 
        totals_labelframe = LabelFrame(self, text="Combined Totals", padx=10, pady=10)
        totals_labelframe.grid(row=1, column=1, sticky="NSEW", padx=10, pady=10)
        totals_labelframe.grid_columnconfigure(0, weight=1)

        self.total_labels = {}

        # Create Attribute Labels 
        for i, attribute in enumerate(self.attributes):
            label = Label(totals_labelframe, text=f"{attribute.capitalize()}: 0", font=("Verdana", 12))
            label.grid(row=i, column=0, sticky="w", pady=(2, 2))
            self.total_labels[attribute] = label

        # A frame to hold the buttons and the buttons
        button_frame = Frame(self)
        button_frame.grid(row=2, column=1, sticky="NSEW", pady=(10,10), padx=(20,20))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        back_button = Button(button_frame, text="BACK", bg="gray", font="Verdana 12 bold", command=self.go_back)
        back_button.grid(row=0, column=0, sticky="NSEW", padx=(0, 5))

        reset_button = Button(button_frame, text="RESET", bg="orange", font="Verdana 12 bold", command=self.reset_selections)
        reset_button.grid(row=0, column=1, sticky="NSEW", padx=(5, 5))

        checkout_button = Button(button_frame, text="CHECKOUT", bg="lightgreen", font="Verdana 12 bold", command=self.go_to_checkout)
        checkout_button.grid(row=0, column=2, sticky="NSEW", padx=(5, 0))

    def select_scent(self, scent_name):
        '''This method adds the chosen scent to the list and calls other methods to update'''
        if len(self.selected_scents) < 3:
            self.selected_scents.append(scent_name)
            self.update_selection_display()
            self.update_totals()
        else:
            messagebox.showinfo("Limit Reached", "You can only select a maximum of 3 scents.")

    def update_selection_display(self):
        '''This method updates the labels to chosen scent'''
        for i, scent_name in enumerate(self.selected_scents):
            self.selected_scent_labels[i].config(text=f"Scent {i + 1}: {scent_name}")

    def reset_selections(self):
        '''This method resets users selections, emptying the list'''
        confirmation = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset choices?")
        
        if confirmation:
            self.selected_scents = []
            for label in self.selected_scent_labels:
                label.config(text=f"Scent {self.selected_scent_labels.index(label) + 1}: (None)")
            self.update_totals()

    def go_to_checkout(self):
        '''This method is linked to the checkout button. It is used to pass the totals for the checkout and raise the frame'''
        
        if not self.selected_scents:
            messagebox.showerror("No Scents Selected", "Please select at least one scent before proceeding to checkout.")
            return
    
        confirmation = messagebox.askyesno("Confirm Checkout", "Are you sure you want to proceed to checkout? You will not be able to change your chosen scents")
        
        if confirmation:
            self.update_totals() #Update Totals before going to checkout
            # Creates a dictionary of the final totals by extracting the value from each label's text
            # Doing it this way ensures that the totals extracted are the same as the combined totals shown
            totals_to_pass = {attr: int(label.cget("text").split(": ")[1]) for attr, label in self.total_labels.items()}
            # Stores the final totals in the FrameManager to then access in checkout
            self.controller.scent_totals = totals_to_pass
            self.controller.selected_scent_names = self.selected_scents
            self.controller.show_frame("Checkout")

    def go_back(self):
        '''This method is linked to the back button. Depending if the user chose free reign or palette takes them back to that frame'''
        # Messagebox
        confirmation = messagebox.askyesno("Confirm Back", "Are you sure you want to go back? Your choices will not be saved")
        if confirmation:
            if self.scent_palette == list(self.controller.scent_notes_data.keys()):
                self.controller.show_frame("MainMenu")
            else:
                self.controller.show_frame("PaletteSelector")

    def update_totals(self, event=None):
        '''This method adds all the chosen scents attribute values together'''
        totals = {attr: 0 for attr in self.attributes}
        
        # Loop to go through all selected scents
        for scent_name in self.selected_scents:
            scent_data = self.controller.scent_notes_data.get(scent_name, {})
            for attr in self.attributes:
                totals[attr] += scent_data.get(attr, 0)
        
        #Loop to loop through all attributes
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
            scent_box = Frame(self.scents_grid_frame, width=150, height=160, padx=5, pady=5, borderwidth=1, relief="solid") 
            scent_box.grid(row=row_number, column=column_number, sticky="NSEW", padx=5, pady=5)  
            scent_box.grid_propagate(False) #Prevents Resizing
            scent_box.grid_columnconfigure(0, weight=1)
            # Configures the rows inside the scent box to be resizable, depending on the name and attributes length
            for j in range(len(self.attributes)):
                scent_box.grid_rowconfigure(j, weight=1)
            scent_box.grid_rowconfigure(len(self.attributes) + 1, weight=1)

            scent_name_label = Label(scent_box, text=scent_name, font=("Verdana", 10, "bold"))
            scent_name_label.grid(row=0, column=0, sticky="EW")

            # Gets attribute data and creates a label, for each one, displaying its value
            scent_attributes = self.controller.scent_notes_data.get(scent_name, {})
            for j, attribute in enumerate(self.attributes):
                value = scent_attributes.get(attribute)
                attribute_label = Label(scent_box, text=f"{attribute.capitalize()}: {value}")
                attribute_label.grid(row=j + 1, column=0, sticky="W")
            
            add_button = Button(scent_box, text="Add", bg="red", fg="black", font=("Verdana", 10, "bold"),
                                command=lambda s=scent_name: self.select_scent(s))
            add_button.grid(row=len(self.attributes) + 1, column=0, sticky="NSEW", pady=(5, 0))

        # Makes the columns and rows of the scents_grid_frame resizable
        for i in range(columns):
            self.scents_grid_frame.grid_columnconfigure(i, weight=1, minsize=100)
            self.scents_grid_frame.grid_rowconfigure(i, weight=1)

class Checkout(BaseFrame):
    '''Checkout Frame. This frame gets the user to pick a name for their perfume and then displays their final order'''
    def __init__(self, parent, controller):
        super().__init__(parent, controller, 7, 2)
        self.perfume_name_var = StringVar()

        heading = Label(self, text="Your Created Perfume", font=("Verdana", 24, "bold"))
        heading.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Loads and displays the image
        self.image = PhotoImage(file="perfume.png")
        image_label = Label(self, image=self.image)
        image_label.grid(row=1, column=0, columnspan=2, pady=10)

        # Creates a label and entry, prompting the user to name the scent
        name_label = Label(self, text="Name your scent!", font=("Verdana", 16))
        name_label.grid(row=2, column=0, columnspan=2, pady=(20, 5))

        char_limit_label = Label(self, text="(max 24 characters)", font=("Verdana", 10))
        char_limit_label.grid(row=3, column=0, columnspan=2)

        self.name_entry = Entry(self, textvariable=self.perfume_name_var, width=50)
        self.name_entry.grid(row=4, column=0, columnspan=2, pady=(10, 10))

        # Binds the return or enter key to the show_final_scent_name method, running it when it's pressed
        self.name_entry.bind("<Return>", self.show_final_scent_name)
        
        # A label to display the final scent name, totals and chosen scents
        self.final_scent_label = Label(self, text="", font=("Verdana", 13), justify=CENTER)
        self.final_scent_label.grid(row=5, column=0, columnspan=2, sticky="n", pady=(10, 10))

        self.final_totals_label = Label(self, text="", font=("Verdana", 11), justify=CENTER)
        self.final_totals_label.grid(row=6, column=1, sticky="ns", padx=(30, 13), pady=10)
        
        self.final_selected_scents_label = Label(self, text="", font=("Verdana", 11), justify=CENTER)
        self.final_selected_scents_label.grid(row=6, column=0, sticky="ns", padx=(10, 30), pady=10)
    
    def show_final_scent_name(self, event=None):
        '''This method updates the labels with the entered scent name and the combined totals.'''

        perfume_name = self.perfume_name_var.get()

        #Checks if name is empty and if it is then shows message.
        if not perfume_name.strip():
            messagebox.showerror("Error", "Scent name cannot be empty.")
            return
        
        #Replaces spaces for empty then checks if the name is alphabetical
        if not perfume_name.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Scent name can only contain alphabetic characters and spaces.")
            return
        
        # Checks if characters are less than 24
        if len(perfume_name) > 24:
            messagebox.showerror("Error", "Scent name cannot exceed 24 characters.")
            return

        self.final_scent_label.config(text=f"Your Final Scent: {perfume_name}")

        # Finds totals and sets the text to it all on seperate lines
        totals = self.controller.scent_totals
        totals_list = [f"{key.capitalize()}: {value}" for key, value in totals.items()]
        totals_text = "Fragrance Profile: \n" + "\n".join(totals_list)
        self.final_totals_label.config(text=totals_text)
        
        # Finds scents and sets the text to it all on seperate lines
        selected_scents = self.controller.selected_scent_names
        selected_scents_text = "Selected Scents:\n" + "\n".join(selected_scents)
        self.final_selected_scents_label.config(text=selected_scents_text)

# Runs and creates an instance of the Framemanager, which controls everything.
if __name__ == "__main__":
    app = FrameManager()
    app.mainloop()