from command import *
from playlist import Add_Playlist

import tkinter as tk
import os
import pygame

class Prototype(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.add_playlist_window = None

        pygame.init()
        pygame.mixer.init()

        #self.focused_listbox = self.focus_get()
        
        # Color varibles
        self.bg_color = "#660000"
        self.frame_color = "#6fa8dc"

        self.music_title = tk.StringVar(value="Music Title")
        self.music_album = tk.StringVar(value="Music Album")
        self.music_start_length = tk.StringVar(value="00:00")
        self.music_length = tk.StringVar(value="00:00")

        self.play_text = tk.StringVar(value="\u23F5")

        self.is_playing = False
        self.from_start = False

        self.music_start_counter = 0
        self.selected_index = 0

        self.__configure_window()
        self.__add_pictures()
        self.__add_frames()
        self.__add_labels()
        self.__add_scrollbar()
        self.__add_listbox()
        self.__add_buttons()

        self.load_songs()

        # Bind Keyboard events
        self.bind("<s>", self.stop_song)
        self.bind("<space>", self.play_song)
        self.bind("<Right>", self.play_next)
        self.bind("<Left>", self.play_prev)

        # Here dito is padding sya kung baga is yung layo ng widgets sa isat isa
        Config_WidgetPadding(self.root_frame, 10, 10).execute()
        Config_WidgetPadding(self.main_frame, 10, None).execute()
        Config_WidgetPadding(self.currently_playing_frame, 20, 10).execute()
        Config_WidgetPadding(self.main_menu_frame, 20, 10).execute()
        Config_WidgetPadding(self.main_menu_btn_frame, 20, 15).execute()
        
        # Here naman yung widget size
        # Config_WidgetSize(self.main_menu_btn_frame, 20, 2).execute()
        # #Config_WidgetSize(self.btn_control_frame, 5, 2).execute()
        # Config_WidgetSize(self.add_on_btn_frame, 20, 3).execute()

        # Font Size
        Config_WidgetFontSize(self.main_menu_btn_frame, "Arial", 15).execute()
        Config_WidgetFontSize(self.btn_control_frame, "Arial", 15).execute()

        self.main_menu_frame.tkraise()
        # Note babaguhin lang yung numbers and yung unag number is width
        # and yug second is height. Sa padding naman padx yung una and pady
        # yung paalawa

        self.run()

    def __configure_window(self):
        self.title("Mellifluous")
        #self.geometry("700x500")
        #self.resizable(False, False)
        self.configure(bg="#660000")

    def __add_frames(self):
        # Root Frame
        self.root_frame = tk.Frame(self, bg=self.bg_color)
        self.root_frame.pack(expand=True)

        # Main Frame
        self.main_frame = tk.Frame(self.root_frame, bg=self.bg_color)
        self.main_frame.pack(expand=True)

        ##### Main Menu Frame #####
        self.main_menu_frame = tk.LabelFrame(self.main_frame, text="Main Menu", bg=self.frame_color)
        self.main_menu_frame.grid(column=0, row=1, sticky="ns")

        self.main_menu_btn_frame = tk.LabelFrame(self.main_menu_frame,text="BTn", bg=self.frame_color)
        self.main_menu_btn_frame.grid(column=0, row=0)

        self.frequently_played_frame = tk.LabelFrame(self.main_menu_frame, text="Frequenlty")
        self.frequently_played_frame.grid(column=0, row=1)
        ###########################

        ##### Currently Playing Frame #####
        self.currently_playing_frame = tk.LabelFrame(self.main_frame, text="Currently Playing Frame", bg=self.frame_color)
        self.currently_playing_frame.grid(column=1, row=1, sticky="ns")

        self.song_details_frame = tk.LabelFrame(self.currently_playing_frame, text="Music Details", bg=self.frame_color)
        self.song_details_frame.grid(column=0, row=0,sticky="ew")

        self.all_btn_frame = tk.LabelFrame(self.currently_playing_frame, text="All BTN frame")
        self.all_btn_frame.grid(column=0, row=1)

        self.btn_control_frame = tk.LabelFrame(self.all_btn_frame, text="BTN Control")
        self.btn_control_frame.grid(column=1, row=1)

        self.add_on_btn_frame = tk.LabelFrame(self.all_btn_frame, text="Add On Frame")
        self.add_on_btn_frame.grid(column=0, row=2, columnspan=3)
        ###################################

        ##### All Songs Frame #####
        self.all_songs_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.all_songs_frame.grid(column=0, row=1, sticky="ns")
        ###########################

        ##### Favorites Frame #####
        self.fav_songs_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.fav_songs_frame.grid(column=0, row=1, sticky="ns")
        ###########################

        ##### Album Song Frame #####
        self.album_frame = tk.LabelFrame(self.main_frame, text="Album Frame", bg=self.frame_color)
        self.album_frame.grid(column=0, row=1, sticky="ns")

        self.album_song_frame = tk.LabelFrame(self.main_frame, text="Albumsongs", bg=self.frame_color)
        self.album_song_frame.grid(column=0, row=1, sticky="ns")
        ############################

        ##### Genre Frame #####
        self.genre_frame = tk.LabelFrame(self.main_frame,text="Genre Frame",bg=self.frame_color)
        self.genre_frame.grid(column=0, row=1, sticky="ns")

        self.genre_song_frame = tk.LabelFrame(self.main_frame,text="Genre Song", bg=self.frame_color)
        self.genre_song_frame.grid(column=0, row=1, sticky="ns")
        #######################

    def __add_buttons(self):
        ##### Buttons Main Menu Frame [Main Menu BTN Frame] #####
        all_songs_btn = tk.Button(self.main_menu_btn_frame, image=self.all_songs_img, command=lambda: Show_Frame(self.all_songs_frame).execute())
        all_songs_btn.grid(column=0, row=0, sticky="ew")

        favorites_btn = tk.Button(self.main_menu_btn_frame, image=self.favorites_img, command=lambda: Show_Frame(self.fav_songs_frame).execute())
        favorites_btn.grid(column=1, row=0, sticky="ew")

        albums_btn = tk.Button(self.main_menu_btn_frame, image=self.albums_img, command=lambda: Show_Frame(self.album_frame).execute())
        albums_btn.grid(column=0, row=1, sticky="ew")

        playlist_btn = tk.Button(self.main_menu_btn_frame, image=self.playlist_img)
        playlist_btn.grid(column=1, row=1, sticky="ew")

        genre_btn = tk.Button(self.main_menu_btn_frame, image=self.genre_img, command=lambda: Show_Frame(self.genre_frame).execute())
        genre_btn.grid(column=0, row=2, sticky="ew")

        mood_btn = tk.Button(self.main_menu_btn_frame, image=self.mood_img)
        mood_btn.grid(column=1, row=2, sticky="ew")

        ###################################

        ##### Buttons Currently Playing Frame [BTN Frame] #####
        prev_btn = tk.Button(self.btn_control_frame, text="\u23ee", command=self.play_prev)
        prev_btn.grid(column=0, row=0)

        stop_btn = tk.Button(self.btn_control_frame, text="\u23f9", command=self.stop_song)
        stop_btn.grid(column=1,row=0)

        play_btn = tk.Button(self.btn_control_frame, textvariable=self.play_text, command=self.play_song)
        play_btn.grid(column=2, row=0)

        next_btn = tk.Button(self.btn_control_frame, text="\u23ed", command=self.play_next)
        next_btn.grid(column=3, row=0)

        fave_btn = tk.Button(self.add_on_btn_frame, image=self.add_fav_img, command=lambda: Add_To_Favorites(self.song_data, self.music_data, self.fav_song_listbox).execute()) #self.add_to_favorites(self.song_data)
        fave_btn.grid(column=0, row=0, sticky="ew")

        add_to_playlist_btn = tk.Button(self.add_on_btn_frame, image=self.add_playlist_img, command=self.add_to_playlist)
        add_to_playlist_btn.grid(column=1, row=0, sticky="ew")

        #######################################################

        ##### All songs Frame #####
        backbtn = tk.Button(self.all_songs_frame, image= self.back_btn_img, command=lambda: Hide_Frame(self.all_songs_frame).execute())
        backbtn.pack(side=tk.BOTTOM)
        ###########################

        ##### Fave Songs Frame #####
        backbtn2 = tk.Button(self.fav_songs_frame, text="Back", command=lambda:Hide_Frame(self.fav_songs_frame).execute(),
                            width=14, height=2)
        backbtn2.pack(side=tk.BOTTOM)
        ############################

        ##### Album Frame #####
        backbtn3 = tk.Button(self.album_frame, text="Back", command=lambda:Hide_Frame(self.album_frame).execute(),
                            width=14, height=2)
        backbtn3.pack(side=tk.BOTTOM)
        openbtn3 = tk.Button(self.album_frame, text="Open", command=self.check_selected,
                            width=14, height=2)
        openbtn3.pack(side=tk.BOTTOM)
        #######################

        ###### Album Song Frame #####
        backbtn4 = tk.Button(self.album_song_frame, text="Back", command=lambda:Hide_Frame(self.album_song_frame).execute(),
                            width=14, height=2)
        backbtn4.pack(side=tk.BOTTOM)
        #############################

        ##### Genre Frame #####
        backbtn5 = tk.Button(self.genre_frame, text="Back", command=lambda:Hide_Frame(self.genre_frame).execute(),
                            width=14, height=2)
        backbtn5.pack(side=tk.BOTTOM)
        openbtn5 = tk.Button(self.genre_frame, text="Open", command=self.check_selected,
                            width=14, height=2)
        openbtn5.pack(side=tk.BOTTOM)
        #######################

        ##### Genre song Frame #####
        backbtn6 = tk.Button(self.genre_song_frame, text="Back", command=lambda:Hide_Frame(self.genre_song_frame).execute(),
                            width=14, height=2)
        backbtn6.pack(side=tk.BOTTOM)
        ############################

    def __add_labels(self):
        brand = tk.Label(self.main_frame, text="MELLIFLUOUS", font=("Arial", 15, "bold"), bg=self.bg_color, fg="white")
        brand.grid(column=0, row=0, sticky="w")

        music_cover = tk.Label(self.song_details_frame, image=self.music_cover_img, bg=self.frame_color)
        music_cover.pack()

        music_title = tk.Label(self.song_details_frame, textvariable=self.music_title)
        music_title.pack(anchor="w")

        music_album = tk.Label(self.song_details_frame, textvariable=self.music_album)
        music_album.pack(anchor="w")

        music_start = tk.Label(self.all_btn_frame, textvariable=self.music_start_length)
        music_start.grid(column=0, row=1)

        music_legth = tk.Label(self.all_btn_frame, textvariable=self.music_length)
        music_legth.grid(column=2, row=1)

    def __add_pictures(self):
        # Assets
        music_cover_path = os.path.join("assets", "albumart.png")
        albums_path = os.path.join("assets", "albums.png")
        all_songs_path = os.path.join("assets", "all_songs.png")
        favorites_path = os.path.join("assets", "favorites.png")
        genre_path = os.path.join("assets", "genres.png")
        mood_path = os.path.join("assets", "mood.png")
        playlist_path = os.path.join("assets", "playlists.png")
        back_btn_path = os.path.join("assets", "back.png")
        add_fav_path = os.path.join("assets", "add_to_favorites.png")
        add_playlist_path = os.path.join("assets", "add_to_playlist.png")

        self.music_cover_img = tk.PhotoImage(file=music_cover_path)
        self.albums_img = tk.PhotoImage(file=albums_path)
        self.all_songs_img = tk.PhotoImage(file=all_songs_path)
        self.favorites_img = tk.PhotoImage(file=favorites_path)
        self.genre_img = tk.PhotoImage(file=genre_path)
        self.mood_img = tk.PhotoImage(file=mood_path)
        self.playlist_img = tk.PhotoImage(file=playlist_path)
        self.back_btn_img = tk.PhotoImage(file=back_btn_path)
        self.add_fav_img = tk.PhotoImage(file=add_fav_path)
        self.add_playlist_img = tk.PhotoImage(file=add_playlist_path)

        # Media Controls
        play_path = os.path.join("assets", "play.png")
        pause_path = os.path.join("assets", "pause.png")
        next_path = os.path.join("assets", "next.png")
        prev_path = os.path.join("assets", "prev.png")

        self.play_img = tk.PhotoImage(file=play_path)
        self.pause_img = tk.PhotoImage(file=pause_path)
        self.next_img = tk.PhotoImage(file=next_path)
        self.preve_img = tk.PhotoImage(file=prev_path)

    def __add_listbox(self):
        self.all_songs_listbox = tk.Listbox(self.all_songs_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.all_songs_listbox.pack(fill="both")

        self.fav_song_listbox = tk.Listbox(self.fav_songs_frame, width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y1.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.fav_song_listbox.pack(fill="both")

        self.album_listbox = tk.Listbox(self.album_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y2.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.album_listbox.pack(fill="both")

        self.album_song_listbox = tk.Listbox(self.album_song_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y3.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.album_song_listbox.pack(fill="both")

        self.genre_listbox = tk.Listbox(self.genre_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y4.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.genre_listbox.pack(fill="both")

        self.genre_song_listbox = tk.Listbox(self.genre_song_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y5.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.genre_song_listbox.pack(fill="both")

        self.frequently_played_listbox = tk.Listbox(self.frequently_played_frame,width=43, height=6, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y5.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.frequently_played_listbox.pack(fill="both")

    def __add_scrollbar(self):
        self.scroll_y = tk.Scrollbar(self.all_songs_frame, orient=tk.VERTICAL)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y1 = tk.Scrollbar(self.fav_songs_frame, orient=tk.VERTICAL)
        self.scroll_y1.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y2 = tk.Scrollbar(self.album_frame, orient=tk.VERTICAL)
        self.scroll_y2.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y3 = tk.Scrollbar(self.album_song_frame, orient=tk.VERTICAL)
        self.scroll_y3.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y4 = tk.Scrollbar(self.genre_frame, orient=tk.VERTICAL)
        self.scroll_y4.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y5 = tk.Scrollbar(self.genre_song_frame, orient=tk.VERTICAL)
        self.scroll_y5.pack(side=tk.RIGHT, fill=tk.Y)

    def load_songs(self):
        if os.path.exists("music_data.json"):
            self.music_data = Load_JSON().execute()
        else:   
            Load_Save_to_JSON().execute()
            self.music_data = Load_JSON().execute()

        self.all_songs_listbox.delete(0, tk.END)

        for song_title, song_data in self.music_data.items():
            if song_data["is_favorite"] == True:
                self.fav_song_listbox.insert(0, song_data["title"])

            self.all_songs_listbox.insert(tk.END, song_data["title"])

            if song_data["album"] not in self.genre_listbox.get(0, tk.END):
                if song_data["album"] is None:
                    song_data["album"] = "Unknown Album"
                self.album_listbox.insert(tk.END, song_data["album"])


            if song_data["genre"] not in self.genre_listbox.get(0, tk.END):
                if song_data["genre"] is None:
                    song_data["genre"] = "Unknown Genre"
                self.genre_listbox.insert(tk.END, song_data["genre"])

        self.load_frequently_played()
        #self.after(60000, self.load_songs)

    def play_song(self, event=None):
        if not self.is_playing:
            if not self.from_start:
                if self.all_songs_listbox.curselection():
                    self.load_song_to_pygame(self.all_songs_listbox)
                elif self.fav_song_listbox.curselection():
                    self.load_song_to_pygame(self.fav_song_listbox)
                elif self.album_song_listbox.curselection():
                    self.load_song_to_pygame(self.album_song_listbox)
                elif self.genre_song_listbox.curselection():
                    self.load_song_to_pygame(self.genre_song_listbox)
                elif self.frequently_played_listbox.curselection():
                    self.load_song_to_pygame(self.frequently_played_listbox)
                else:
                    # If no item is selected, print a message or handle it as per your requirement
                    MsgBx_ShowWarning("Please select a song!").execute()
            else:
                self.unpause_song()
        else:
            self.pause_song()

    def load_song_to_pygame(self, listbox:tk.Listbox):
        self.play_text.set(value="\u23f8")
        # Get the index of the selected item
        self.selected_index = listbox.curselection()[0]
        # Get the corresponding song data from the JSON
        self.song_data = self.music_data[listbox.get(self.selected_index)]
        print(f"Song data play btn {self.song_data}\n")

        title = self.song_data["title"]
        album = self.song_data["album"]
        duration = self.song_data["duration"]
        file_path = self.song_data["file_path"]

        self.music_title.set(title)
        self.music_album.set(album)
        self.music_length.set(duration)
        
        # Load and play the selected song
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        Add_Count(self.song_data, self.music_data).execute()

        # Update playing status and reset counter
        self.is_playing = True
        self.from_start = True

        #self.check(self.song_data, self.music_data)
        # Start the counter updater
        self.update_counter()

    def unpause_song(self):
        pygame.mixer.music.unpause()
        self.is_playing = True
        self.play_text.set(value="\u23f8")
        self.update_counter()

    def pause_song(self):
        pygame.mixer.music.pause()
        self.is_playing = False
        self.play_text.set(value="\u23f5")

    def stop_song(self, event=None):
        self.after_cancel(self.update_counter_id)
        pygame.mixer.music.stop()
        self.is_playing = False
        self.from_start = False
        self.music_start_counter = 0
        self.music_start_length.set(value="00:00")
        self.play_text.set(value="\u23f5")

    def play_prev(self, event=None):
        if self.all_songs_listbox.curselection():
            listbox = self.all_songs_listbox
        elif self.fav_song_listbox.curselection():
            listbox = self.fav_song_listbox
        elif self.album_song_listbox.curselection():
            listbox = self.album_song_listbox
        elif self.genre_song_listbox.curselection():
            listbox = self.genre_song_listbox
        elif self.frequently_played_listbox.curselection():
            listbox = self.frequently_played_listbox
        else:
            listbox = self.all_songs_listbox

        pygame.mixer.music.stop()
        self.is_playing = False
        self.from_start = False
        self.music_start_length.set(value="00:00")
        self.music_start_counter = 0

        self.selected_index -= 1

        if self.selected_index >= 0:
            # Get the selected item from the listbox
            self.song_data = self.music_data[listbox.get(self.selected_index)]
            print(f"Song data playnext btn {self.song_data}\n")
            # Retrieve the file path of the selected song
            file_path = self.song_data["file_path"]
            self.music_title.set(self.song_data["title"])
            self.music_album.set(self.song_data["album"])
            self.music_length.set(self.song_data["duration"])
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.from_start = True

            Add_Count(self.song_data, self.music_data).execute()
            self.play_text.set(value="⏸")

            listbox.selection_clear(0, tk.END)  # Clear previous selection
            listbox.selection_set(self.selected_index)  # Set new selection
            listbox.activate(self.selected_index)
            self.update_counter()
        else:
            self.stop_song()
            self.selected_index = 0

    def play_next(self, event=None):
        if self.all_songs_listbox.curselection():
            listbox = self.all_songs_listbox
        elif self.fav_song_listbox.curselection():
            listbox = self.fav_song_listbox
        elif self.album_song_listbox.curselection():
            listbox = self.album_song_listbox
        elif self.genre_song_listbox.curselection():
            listbox = self.genre_song_listbox
        elif self.frequently_played_listbox.curselection():
            listbox = self.frequently_played_listbox
        else:
            listbox = self.all_songs_listbox
            
        self.stop_song()
        self.after_cancel(self.update_counter_id)

        self.selected_index += 1
        
        if self.selected_index < listbox.size():
            # Get the selected item from the listbox
            self.song_data = self.music_data[listbox.get(self.selected_index)]
            print(f"Song data playnext btn {self.song_data}\n")
            # Retrieve the file path of the selected song
            file_path = self.song_data["file_path"]
            self.music_title.set(self.song_data["title"])
            self.music_album.set(self.song_data["album"])
            self.music_length.set(self.song_data["duration"])
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.from_start = True

            Add_Count(self.song_data, self.music_data).execute()
            self.play_text.set(value="⏸")

            listbox.selection_clear(0, tk.END)  # Clear previous selection
            listbox.selection_set(self.selected_index)  # Set new selection
            listbox.activate(self.selected_index)
            self.update_counter()
        else:
            self.stop_song()
            self.selected_index = 0

    def check_selected(self):
        if self.album_listbox.curselection():
            self.load_album()
            Show_Frame(self.album_song_frame).execute()
        elif self.genre_listbox.curselection():
            self.load_genre()
            Show_Frame(self.genre_song_frame).execute()
        else:
            MsgBx_ShowWarning("Please select a selection").execute()

    def load_album(self):
        self.album_song_listbox.delete(0, tk.END)
        if self.album_listbox.curselection():
            selected_album_index = self.album_listbox.curselection()[0]
            selected_album = self.album_listbox.get(selected_album_index)

            for song_title, song_data in self.music_data.items():
                if song_data["album"] == selected_album:
                    # Insert the song title into the album songs listbox
                    self.album_song_listbox.insert(tk.END, song_data["title"])
        else:
            print("No album selected")

    def load_genre(self):
        self.genre_song_listbox.delete(0, tk.END)

        if self.genre_listbox.curselection():
            selected_genre_index = self.genre_listbox.curselection()[0]
            selected_genre = self.genre_listbox.get(selected_genre_index)
            print(selected_genre)

            for song_title, song_data in self.music_data.items():
                if song_data["genre"] == selected_genre:
                    # Insert the song title into the album songs listbox
                    self.genre_song_listbox.insert(tk.END, song_data["title"])

    def load_frequently_played(self):
        frequently_played = {}

        for song_title, song_data in self.music_data.items():
            frequently_played.update({song_title: song_data["play_counter"]})

        sorted_frequently = self.bubble_sort(frequently_played)
        print(sorted_frequently)
        for item in sorted_frequently:
            self.frequently_played_listbox.insert(tk.END, item)
    
    def bubble_sort(self, dict1:dict):
        items = list(dict1.items())
        length = len(items)

        for i in range(length):
            swapped = False
            for j in range(0, length-i-1):
                if items[j][1] < items[j+1][1]: 
                    items[j], items[j+1] = items[j+1], items[j]
                    swapped = True

            if not swapped:
                break

        return dict(items)
    
    def add_to_playlist(self):
        if not self.add_playlist_window:
            self.add_playlist_window = Add_Playlist(self)
        
        self.iconify()
        self.add_playlist_window.lift()

    def update_counter(self):
        if self.is_playing:
            # Increment counter and update start length label
            self.music_start_counter += 1
            minutes = self.music_start_counter // 60
            seconds = self.music_start_counter % 60
            self.music_start_length.set(f"{minutes:02d}:{seconds:02d}")
            total_duration_seconds = int(self.music_length.get().split(":")[0]) * 60 + int(self.music_length.get().split(":")[1])

            # Schedule the function to run again after 1 second
            if self.music_start_counter > total_duration_seconds:
                self.stop_song()
                self.play_next()

            # elif not self.is_playing:   
            #     self.after_cancel(1000, self.update_counter)
            else:
                self.update_counter_id = self.after(1000, self.update_counter)  

        else:
            self.after_cancel(self.update_counter)


    def run(self):
        self.mainloop()

if __name__ == '__main__':
    proto = Prototype()
