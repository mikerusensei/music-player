from playlist import ConcretePlaylist
import tkinter as tk

class Add_Playlist(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # Color varibles
        self.bg_color = "#660000"
        self.frame_color = "#6fa8dc"

        self.__configure_window()
        self.__add_frames()
        self.__add_buttons()

    def __configure_window(self):
        self.title("Add to Playlist")
        #self.resizable(False, False)
        #self.geometry("350x500")
    
    def __add_frames(self):
        self.root_frame = tk.LabelFrame(self, text="Root Frame", bg=self.bg_color)
        self.root_frame.pack(expand=True)

        self.main_frame = tk.LabelFrame(self.root_frame, text="Main Frame",bg=self.bg_color)
        self.main_frame.pack(expand=True)

    def __add_buttons(self):
        self.create_playlist = tk.Button(self.main_frame, text="Create Playlist")
        self.create_playlist.grid(column=0, row=0, sticky="ew")

    def destroy(self):
        super().destroy()
        if self.master:
            self.master.add_playlist_window = None