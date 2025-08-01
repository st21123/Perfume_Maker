'''
An app that where you can make your own perfume

Version 1: basic working program, functions, no optimisations, no validation at all
 '''

from tkinter import *

class PerfumeMaker:
    '''Set up the GUI'''
    def __init__(self):
        self.root = Tk()
        self.root.title("Perfumantor")
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)
        self.root.geometry("500x500")

        # Container for frames
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky=NSEW)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        # Dictionary to hold frames
        self.frames = {}
        self.frames["MainMenu"] = self.create_main_menu()
        self.frames["PaletteSelector"] = self.create_palette_selector()
        self.frames["MainGame"] = self.create_main_game()
        self.frames["Checkout"] = self.create_checkout()

        # Show the initial frame
        self.show_frame("MainMenu")


    def run(self):
        '''runs the program'''
        self.root.mainloop()

    def show_frame(self, name):
        '''Display the required frame from the dictionary'''
        frame = self.frames[name]
        frame.tkraise()

    def create_main_menu(self):
        '''Create the mainframe'''
        
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky=NSEW)
        
        for i in range(4):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(2):
            frame.grid_columnconfigure(j, weight=1)            

        heading = Label(frame, text="Welcome to the Perfumanator", font="Verdana 16 bold")
        heading.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # photo_label= Label(image="placeholder.png")
        # photo_label.grid(row=1, column=0, columnspan=2, sticky=NSEW)

        main_menu_text = Label(frame, text="would you like to choose from", font="Verdana 11")
        main_menu_text.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=(50, 0))

        free_reign_button = Button(frame, text="Free Reign", bg="lightgreen", font="Verdana 12 bold",command=lambda: self.show_frame("MainGame"))
        free_reign_button.grid(row=3, column=0, sticky=NSEW)
    
        preset_palette_button= Button(frame, text="Preset Palette", bg="yellow", font="Verdana 12 bold",command=lambda: self.show_frame("PaletteSelector"))
        preset_palette_button.grid(row=3, column=1, sticky=NSEW)

        return frame
    
    def create_palette_selector(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky=NSEW)

        for i in range(5):
            frame.grid_rowconfigure(i, weight=1)
        for j in range(1):
            frame.grid_columnconfigure(j, weight=1)    
        
        heading = Label(frame, text="Our Premade Palettes", font="Verdana 16 bold")
        heading.grid(row=0, column=0, sticky=NSEW)

        summer_palette_button= Button(frame, text="Summer Palette (more fruity scents)", bg="yellow", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
        summer_palette_button.grid(row=1, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        outdoors_palette_button= Button(frame, text="Outdoors Palette (more woody scents)", bg="forest green", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
        outdoors_palette_button.grid(row=2, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        candy_palette_button= Button(frame, text="Candy Palette (more sweet scents)", bg="hot pink", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
        candy_palette_button.grid(row=3, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        zesty_palette_button= Button(frame, text="Zesty Palette (more Citrusy scents)", bg="orange", font="Verdana 12 bold",command=lambda: ["PLACEHOLDER METHOD(),",self.show_frame("MainGame")])
        zesty_palette_button.grid(row=4, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))

        back_button= Button(frame, text="BACK", bg="gray", font="Verdana 12 bold",command=lambda: self.show_frame("MainMenu"))
        back_button.grid(row=5, column=0, sticky=NSEW, pady=(10,10), padx=(20,20))
        return frame

    def create_main_game(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky=NSEW)
        return frame


    def create_checkout(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky=NSEW)
        return frame
    
    def save_palette_type(self):
        return 

    
if __name__ == "__main__":
    app = PerfumeMaker()
    app.run()
