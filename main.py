import customtkinter
import threading
from backend.utils import download_batch

# Configurations
LINKS = [
    "https://i.example.net/galleries/",
    "https://i3.example.net/galleries/",
    "https://i5.example.net/galleries/",
    "https://i7.example.net/galleries/",
]
ITYPES = ['.jpg', '.png', '.gif']

# Set appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Bulk Image Downloader")
        self.geometry(f"{800}x{190}")
        self.maxsize(width=800, height=200)

 
        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Start", command=self.sidebar_button_event1)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Stop", command=self.sidebar_button_event2)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Logo label
        self.status_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Standby ...",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Input frame
        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")

        self.inner_frame = customtkinter.CTkFrame(self.input_frame, fg_color = "transparent")
        self.inner_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.entry_1 = customtkinter.CTkEntry(master=self.inner_frame, placeholder_text="Folder ID", width=240)
        self.entry_1.grid(row=0, column=0, padx=10, pady=10)
        self.entry_2 = customtkinter.CTkEntry(master=self.inner_frame, placeholder_text="Name (Optional)", width=240)
        self.entry_2.grid(row=1, column=0, padx=10, pady=10)
        
        self.inner_frame2 = customtkinter.CTkFrame(self.input_frame, fg_color = "transparent")
        self.inner_frame2.grid(row=2, column=0, sticky="nsew")
        self.entry_3 = customtkinter.CTkEntry(master=self.inner_frame2, placeholder_text="Start")
        self.entry_3.grid(row=0, column=0, padx=10, pady=10)
        self.label_1 = customtkinter.CTkLabel(master=self.inner_frame2, text=" to ")
        self.label_1.grid(row=0, column=1, padx=10, pady=10)
        self.entry_4 = customtkinter.CTkEntry(master=self.inner_frame2, placeholder_text="End")
        self.entry_4.grid(row=0, column=2, padx=10, pady=10)

        # Setting frame
        self.setting_frame = customtkinter.CTkFrame(self)
        self.setting_frame.grid(row=0, column=4, rowspan=4, sticky="nsew")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.setting_frame, values=LINKS, width=240)
        self.optionmenu_1.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.optionmenu_1.set("CDN Source")

        self.optionmenu_2 = customtkinter.CTkOptionMenu(self.setting_frame, values=ITYPES)
        self.optionmenu_2.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.optionmenu_2.set("Image Type")

        self.checkbox_1 = customtkinter.CTkCheckBox(self.setting_frame, text="Save Logs")
        self.checkbox_1.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.checkbox_2 = customtkinter.CTkCheckBox(self.setting_frame, text="Open Destination")
        self.checkbox_2.grid(row=3, column=0, padx=10, pady=10, sticky='w')

    def get_variables(self):
        # Download Server and Image type
        cdn_source = self.optionmenu_1.get()
        image_type = self.optionmenu_2.get()
        
        # Source Folder location and Custom Download Name
        directory = self.entry_1.get()
        fname = self.entry_2.get() if  self.entry_2.get() != "" else None 

        # Page Range
        start = int(self.entry_3.get())
        end= int(self.entry_4.get())

        return cdn_source, image_type, directory, fname, start, end
        

    # Start
    def sidebar_button_event1(self):
        cdn_source, image_type, directory, fname, start, end = self.get_variables()
        thread = threading.Thread(target=download_batch,args=(cdn_source, image_type, directory, fname, start, end))
        thread.start()

    # End
    def sidebar_button_event2(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
