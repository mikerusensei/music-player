from command import *

import tkinter as tk
import os
import pygame
import random

class Prototype(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.add_playlist_window = None

        pygame.init()
        pygame.mixer.init()
        
        # Color varibles
        self.bg_color = "#660000"
        self.frame_color = "#6fa8dc"
        self.playlists = Load_JSON("playlist.json").execute()

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
        self.__add_entry()
        self.__add_labels()
        self.__add_scrollbar()
        self.__add_listbox()
        self.__add_buttons()

        self.load_songs()

        # Bind Keyboard events
        self.bind("<Up>", self.stop_song)
        self.bind("<Down>", self.play_song)
        self.bind("<Right>", self.play_next)
        self.bind("<Left>", self.play_prev)

        # Here dito is padding sya kung baga is yung layo ng widgets sa isat isa
        Config_WidgetPadding(self.root_frame, 10, 10).execute()
        Config_WidgetPadding(self.main_frame, 10, None).execute()
        Config_WidgetPadding(self.currently_playing_frame, 20, 10).execute()
        Config_WidgetPadding(self.main_menu_frame, 20, 10).execute()
        Config_WidgetPadding(self.main_menu_btn_frame, 20, 15).execute()
        Config_WidgetPadding(self.all_btn_frame, 10, 10).execute()

        # Font Size
        Config_WidgetFontSize(self.main_menu_btn_frame, "Arial", 15).execute()
        Config_WidgetFontSize(self.btn_control_frame, "Arial", 15).execute()

        self.main_menu_frame.tkraise()

        self.run()

    def __configure_window(self):
        self.title("Mellifluous")
        self.resizable(False, False)
        self.configure(bg="#660000")

    def __add_frames(self):
        # Root Frame
        self.root_frame = tk.Frame(self, bg=self.bg_color)
        self.root_frame.pack(expand=True)

        # Main Frame
        self.main_frame = tk.Frame(self.root_frame, bg=self.bg_color)
        self.main_frame.pack(expand=True)

        ##### Main Menu Frame #####
        self.main_menu_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.main_menu_frame.grid(column=0, row=1, sticky="ns")

        self.main_menu_btn_frame = tk.Frame(self.main_menu_frame, bg=self.frame_color)
        self.main_menu_btn_frame.grid(column=0, row=0)

        self.frequently_played_frame = tk.LabelFrame(self.main_menu_frame, text="Frequenlty")
        self.frequently_played_frame.grid(column=0, row=1)
        ###########################

        ##### Currently Playing Frame #####
        self.currently_playing_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.currently_playing_frame.grid(column=1, row=1, sticky="ns")

        self.song_details_frame = tk.Frame(self.currently_playing_frame, bg=self.frame_color)
        self.song_details_frame.grid(column=0, row=0,sticky="ew")

        self.all_btn_frame = tk.Frame(self.currently_playing_frame, bg= self.frame_color)
        self.all_btn_frame.grid(column=0, row=1)

        self.btn_control_frame = tk.Frame(self.all_btn_frame, bg=self.frame_color)
        self.btn_control_frame.grid(column=1, row=1)

        self.add_on_btn_frame = tk.LabelFrame(self.all_btn_frame, bg=self.frame_color)
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
        self.album_frame = tk.Frame(self.main_frame,  bg=self.frame_color)
        self.album_frame.grid(column=0, row=1, sticky="ns")

        self.album_song_frame = tk. Frame(self.main_frame,  bg=self.frame_color)
        self.album_song_frame.grid(column=0, row=1, sticky="ns")
        ############################

        ##### Genre Frame #####
        self.genre_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.genre_frame.grid(column=0, row=1, sticky="ns")

        self.genre_song_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.genre_song_frame.grid(column=0, row=1, sticky="ns")
        #######################

        ##### Playlist Frame #####
        self.create_add_playlist_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.create_add_playlist_frame.grid(column=0, row=1, sticky="nsew")

        self.playlist_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.playlist_frame.grid(column=0, row=1, sticky="ns")

        self.playlist_song_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.playlist_song_frame.grid(column=0, row=1, sticky="ns")

        self.create_playlist_frame = tk.Frame(self.create_add_playlist_frame, bg= self.frame_color)
        self.create_playlist_frame.pack(fill=tk.BOTH, expand=True)

        self.add_playlist_frame = tk.Frame(self.create_add_playlist_frame, bg=self.frame_color)
        self.add_playlist_frame.pack(fill=tk.BOTH, expand=True )
        ##########################

        ##### Mood Frame #####
        self.mood_frame = tk.Frame(self.main_frame, bg= self.frame_color)
        self.mood_frame.grid(column=0, row=1, sticky="nsew")

        self.mood_btn_frame = tk.Frame(self.mood_frame, bg=self.frame_color)
        self.mood_btn_frame.pack(fill="both", expand=True)

        self.mood_songs_frame = tk.Frame(self.main_frame, bg=self.frame_color)
        self.mood_songs_frame.grid(column=0, row=1, sticky="ns")
        ######################

    def __add_buttons(self):
        ##### Buttons Main Menu Frame [Main Menu BTN Frame] #####
        all_songs_btn = tk.Button(self.main_menu_btn_frame, image=self.all_songs_img, command=lambda: Show_Frame(self.all_songs_frame).execute())
        all_songs_btn.grid(column=0, row=0, sticky="ew")

        favorites_btn = tk.Button(self.main_menu_btn_frame, image=self.favorites_img, command=lambda: Show_Frame(self.fav_songs_frame).execute())
        favorites_btn.grid(column=1, row=0, sticky="ew")

        albums_btn = tk.Button(self.main_menu_btn_frame, image=self.albums_img, command=lambda: Show_Frame(self.album_frame).execute())
        albums_btn.grid(column=0, row=1, sticky="ew")

        playlist_btn = tk.Button(self.main_menu_btn_frame, image=self.playlist_img, command=lambda: Show_Frame(self.playlist_frame).execute())
        playlist_btn.grid(column=1, row=1, sticky="ew")

        genre_btn = tk.Button(self.main_menu_btn_frame, image=self.genre_img, command=lambda: Show_Frame(self.genre_frame).execute())
        genre_btn.grid(column=0, row=2, sticky="ew")

        mood_btn = tk.Button(self.main_menu_btn_frame, image=self.mood_img, command=lambda: Show_Frame(self.mood_frame).execute())
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

        add_to_playlist_btn = tk.Button(self.add_on_btn_frame, image=self.add_playlist_img, command=lambda: Show_Frame(self.create_add_playlist_frame).execute())
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

        ##### Playlist Frame #####
        backbtn7 = tk.Button(self.playlist_frame, text="Back", command=lambda:Hide_Frame(self.playlist_frame).execute(),
                            width=14, height=2)
        backbtn7.pack(side=tk.BOTTOM)
        openbtn7 = tk.Button(self.playlist_frame, text="Open", command=self.check_selected,
                            width=14, height=2)
        openbtn7.pack(side=tk.BOTTOM)

        self.create_playlist_btn = tk.Button(self.create_playlist_frame, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_btn.pack(fill=tk.BOTH, expand=True)

        self.add_playlist_btn = tk.Button(self.add_playlist_frame, text="Add to Playlist", command=self.add_playlist)
        self.add_playlist_btn.pack(fill=tk.BOTH, expand=True)

        backbtn8 = tk.Button(self.create_add_playlist_frame, text="Back", command=lambda:Hide_Frame(self.create_add_playlist_frame).execute(),
                            width=14, height=2)
        backbtn8.pack(side=tk.BOTTOM)

        backbtn9 = tk.Button(self.playlist_song_frame, text="Back", command=lambda:Hide_Frame(self.playlist_song_frame).execute(),
                            width=14, height=2)
        backbtn9.pack(side=tk.BOTTOM)
        ##########################

        ########## Mood BTN ################
        happy_btn = tk.Button(self.mood_btn_frame, text="Happy", command=self.make_mood_happy)
        happy_btn.pack()

        sad_btn = tk.Button(self.mood_btn_frame, text="Sad", command= self.make_mood_sad)
        sad_btn.pack()

        chill_btn = tk.Button(self.mood_btn_frame, text="Chill", command=self.make_mood_chill)
        chill_btn.pack()

        sexy_btn = tk.Button(self.mood_btn_frame, text="Sexy", command=self.make_mood_sexy)
        sexy_btn.pack()

        travel_btn = tk.Button(self.mood_btn_frame, text="Travel", command=self.make_mood_travel)
        travel_btn.pack()

        backbtn10 = tk.Button(self.mood_btn_frame, text="Back", command=lambda:Hide_Frame(self.mood_frame).execute(),
                            width=14, height=2)
        backbtn10.pack(side=tk.BOTTOM)
        ####################################

        ##### Mood Songs Frame #####
        backbtn11 = tk.Button(self.mood_songs_frame, text="Back", command=lambda:Hide_Frame(self.mood_songs_frame).execute(),
                            width=14, height=2)
        backbtn11.pack(side=tk.BOTTOM)
        ############################
        
    def __add_labels(self):
        brand = tk.Label(self.main_frame, text="MELLIFLUOUS", font=("Arial", 15, "bold"), bg=self.bg_color, fg="white")
        brand.grid(column=0, row=0, sticky="w")

        music_cover = tk.Label(self.song_details_frame, image=self.music_cover_img, bg=self.frame_color)
        music_cover.pack()

        music_title = tk.Label(self.song_details_frame, textvariable=self.music_title, bg=self.frame_color)
        music_title.pack(anchor="w")

        music_album = tk.Label(self.song_details_frame, textvariable=self.music_album, bg=self.frame_color)
        music_album.pack(anchor="w")

        music_start = tk.Label(self.all_btn_frame, textvariable=self.music_start_length, bg=self.frame_color)
        music_start.grid(column=0, row=1)

        music_legth = tk.Label(self.all_btn_frame, textvariable=self.music_length, bg=self.frame_color)
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

        self.playlist_listbox = tk.Listbox(self.playlist_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y6.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.playlist_listbox.pack(fill="both")

        self.playlist_song_listbox = tk.Listbox(self.playlist_song_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y7.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.playlist_song_listbox.pack(fill="both")

        self.mood_song_listbox = tk.Listbox(self.mood_songs_frame,width=46, height=20, font=("Arial", 12, "bold"),
                                            yscrollcommand=self.scroll_y8.set, selectmode=tk.SINGLE, relief=tk.GROOVE)
        self.mood_song_listbox.pack(fill="both")

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

        self.scroll_y6 = tk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL)
        self.scroll_y6.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y7 = tk.Scrollbar(self.playlist_song_frame, orient=tk.VERTICAL)
        self.scroll_y7.pack(side=tk.RIGHT, fill=tk.Y)

        self.scroll_y8 = tk.Scrollbar(self.mood_songs_frame, orient=tk.VERTICAL)
        self.scroll_y8.pack(side=tk.RIGHT, fill=tk.Y)

    def __add_entry(self):
        self.create_playlist_name_entry = tk.Entry(self.create_playlist_frame)
        self.create_playlist_name_entry.pack(fill=tk.BOTH, expand=True)

        self.add_playlist_name_entry = tk.Entry(self.add_playlist_frame)
        self.add_playlist_name_entry.pack(fill=tk.BOTH, expand=True)

    def load_songs(self):
        if os.path.exists("music_data.json"):
            existing_songs = Load_JSON("music_data.json").execute()
            new_songs = Load_Dir().execute()

            for key, value in new_songs.items():
                if key not in existing_songs:
                    existing_songs[key] = value

            sorted_data = dict(sorted(existing_songs.items()))

            for song_title, song_data in sorted_data.items():
                if song_data.get("album") is None:
                    song_data["album"] = "Unknown Album"
                if song_data.get("genre") is None:
                    song_data["genre"] = "Unknown Genre"
                    
            Save_JSON(sorted_data, "music_data.json").execute()

            self.music_data = sorted_data
            
        else:   
            Load_Save_to_JSON().execute()
            self.music_data = Load_JSON("music_data.json").execute()
        
        self.genres_file = Load_JSON("genre.json").execute()

        for song_title, song_data in self.music_data.items():
            if song_data["is_favorite"] == True and song_data["title"] not in self.fav_song_listbox.get(0, tk.END):
                self.fav_song_listbox.insert(0, song_data["title"])
            
            if song_data["title"] not in self.all_songs_listbox.get(0, tk.END):
                self.all_songs_listbox.insert(tk.END, song_data["title"])

            if song_data["album"] not in self.album_listbox.get(0, tk.END):
                self.album_listbox.insert(tk.END, song_data["album"])
            
            if song_data["genre"] not in self.genre_listbox.get(0, tk.END):
                self.genre_listbox.insert(tk.END, song_data["genre"])
                self.genres_file.update({song_data["genre"]: [song_data["title"]]})

            if song_data["title"] not in self.genres_file[song_data["genre"]]:
                self.genres_file[song_data["genre"]].append(song_data["title"])

        self.load_playlist()
        self.load_frequently_played()
    
        Save_JSON(self.music_data, "music_data.json").execute()
        Save_JSON(self.genres_file, "genre.json").execute()

        self.after(1000, self.load_songs)

    def load_playlist(self):
        self.playlists = Load_JSON("playlist.json").execute()
            
        for playlist_title, playlist_data in self.playlists.items():
            if playlist_title not in self.playlist_listbox.get(0, tk.END):
                self.playlist_listbox.insert(tk.END, playlist_title)

        #self.after(1000, self.load_playlist)

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
                elif self.mood_song_listbox.curselection():
                    self.load_song_to_pygame(self.mood_song_listbox)
                elif self.playlist_song_listbox.curselection():
                    self.load_song_to_pygame(self.playlist_song_listbox)
                    Add_Count_Playist(self.playlists, self.selected_playlist, "playlist.json").execute()
                else:
                    MsgBx_ShowWarning("Please select a song!").execute()
            else:
                self.unpause_song()
        else:
            self.pause_song()

    def load_song_to_pygame(self, listbox:tk.Listbox):
        self.play_text.set(value="\u23f8")

        self.selected_index = listbox.curselection()[0]

        self.song_data = self.music_data[listbox.get(self.selected_index)]

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

        Add_Count(self.song_data, self.music_data, "music_data.json").execute()

        # Update playing status and reset counter
        self.is_playing = True
        self.from_start = True

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
        elif self.playlist_song_listbox.curselection():
            listbox = self.playlist_song_listbox
        elif self.mood_song_listbox.curselection():
            listbox = self.mood_song_listbox
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
            # Retrieve the file path of the selected song
            file_path = self.song_data["file_path"]
            self.music_title.set(self.song_data["title"])
            self.music_album.set(self.song_data["album"])
            self.music_length.set(self.song_data["duration"])
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.is_playing = True
            self.from_start = True

            Add_Count(self.song_data, self.music_data, "music_data.json").execute()
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
        elif self.playlist_song_listbox.curselection():
            listbox = self.playlist_song_listbox
        elif self.mood_song_listbox.curselection():
            listbox = self.mood_song_listbox
        else:
            listbox = self.all_songs_listbox
            
        self.stop_song()
        self.after_cancel(self.update_counter_id)

        self.selected_index += 1
        
        if self.selected_index < listbox.size():
            self.song_data = self.music_data[listbox.get(self.selected_index)]

            file_path = self.song_data["file_path"]
            self.music_title.set(self.song_data["title"])
            self.music_album.set(self.song_data["album"])
            self.music_length.set(self.song_data["duration"])

            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            self.is_playing = True
            self.from_start = True

            Add_Count(self.song_data, self.music_data, "music_data.json").execute()

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
        elif self.playlist_listbox.curselection():
            self.load_playlist_song()
            Show_Frame(self.playlist_song_frame).execute()
        else:
            MsgBx_ShowWarning("Please select a selection").execute()

    def load_album(self):
        self.album_song_listbox.delete(0, tk.END)
        if self.album_listbox.curselection():
            selected_album_index = self.album_listbox.curselection()[0]
            selected_album = self.album_listbox.get(selected_album_index)

            for song_title, song_data in self.music_data.items():
                if song_data["album"] == selected_album:
                    self.album_song_listbox.insert(tk.END, song_data["title"])
        else:
            print("No album selected")

    def load_genre(self):
        self.genre_song_listbox.delete(0, tk.END)

        if self.genre_listbox.curselection():
            selected_genre_index = self.genre_listbox.curselection()[0]
            selected_genre = self.genre_listbox.get(selected_genre_index)
            print(selected_genre)

            for genre_title, genre_songs in self.genres_file.items():
                if genre_title == selected_genre:
                    for song in genre_songs:
                        self.genre_song_listbox.insert(tk.END, song)

    def load_playlist_song(self):
        self.playlists = Load_JSON("playlist.json").execute()

        self.playlist_song_listbox.delete(0, tk.END)

        if self.playlist_listbox.curselection():
            selected_playlist_index = self.playlist_listbox.curselection()[0]
            self.selected_playlist = self.playlist_listbox.get(selected_playlist_index)

            for playlist_title, playlist_data in self.playlists.items():
                if playlist_title == self.selected_playlist:
                    songs = playlist_data["songs"]
                    print(songs)
                    for song in songs:
                        self.playlist_song_listbox.insert(tk.END, song)
                    break
        
    def load_frequently_played(self):
        selected_index = self.frequently_played_listbox.curselection()
        
        self.frequently_played_listbox.delete(0, tk.END)

        frequently_played = {}
        self.music_data = Load_JSON("music_data.json").execute()

        for song_title, song_data in self.music_data.items():
            frequently_played.update({song_title: song_data["play_counter"]})

        sorted_frequently = Bubble_Sort(frequently_played).execute()
        for key, val in sorted_frequently.items():
            if val != 0:
                self.frequently_played_listbox.insert(tk.END, key)

        if selected_index:
            if selected_index[0] < self.frequently_played_listbox.size():
                # Reselect the item
                self.frequently_played_listbox.selection_set(selected_index)
                self.frequently_played_listbox.activate(selected_index)

        # Schedule the function to run again after 30 seconds
        self.after(20000, self.load_frequently_played)

    def create_playlist(self):
        entry = self.create_playlist_name_entry.get()

        exisiting_playlists = Load_JSON("playlist.json").execute()

        exisiting_playlists.update({entry:{"play_count": 0, "songs": [self.song_data["title"]]}})

        Save_JSON(exisiting_playlists, "playlist.json").execute()

        MsgBx_ShowInfo(f"Succesfully created {entry} playlist!").execute()
        self.create_playlist_name_entry.delete(0, 'end')
        Hide_Frame(self.create_add_playlist_frame).execute()

    def add_playlist(self):
        self.playlists = Load_JSON("playlist.json").execute()
        entry = self.add_playlist_name_entry.get()

        playlist_found = False

        for playlist_name, playlist_data in self.playlists.items():
            if playlist_name.lower() == entry.lower():
                playlist_found = True
                if self.song_data["title"] not in playlist_data["songs"]:
                    playlist_data["songs"].append(self.song_data["title"])
                    Save_JSON(self.playlists, "playlist.json").execute()
                    MsgBx_ShowInfo(f"Successfully added to {playlist_name}").execute()
                    self.add_playlist_name_entry.delete(0, 'end')
                    Hide_Frame(self.create_add_playlist_frame).execute()
                else:
                    self.add_playlist_name_entry.delete(0, 'end')
                    MsgBx_ShowInfo("Song is in the playlist").execute()
                    Hide_Frame(self.create_add_playlist_frame).execute()
                break

        if not playlist_found:
            MsgBx_ShowWarning("No playlist found").execute()
    
    def update_counter(self):
        if self.is_playing:
            # Increment counter and update start length label
            self.music_start_counter += 1
            minutes = self.music_start_counter // 60
            seconds = self.music_start_counter % 60
            self.music_start_length.set(f"{minutes:02d}:{seconds:02d}")
            total_duration_seconds = int(self.music_length.get().split(":")[0]) * 60 + int(self.music_length.get().split(":")[1])

            if self.music_start_counter > total_duration_seconds:
                self.stop_song()
                self.play_next()
            else:
                self.update_counter_id = self.after(1000, self.update_counter)  

        else:
            self.after_cancel(self.update_counter)

    def make_mood(self, mood:str, genres:list):
        mood_songs = []

        for genre_title, genre_songs in self.genres_file.items():
            if genre_title in genres:
                mood_songs.extend(genre_songs)

        print(f"Not Shuffled {mood_songs}")

        random.shuffle(mood_songs)

        print(f"Shuffled {mood_songs}")

        return mood_songs
    
    def make_mood_happy(self):
        self.mood_song_listbox.delete(0, tk.END)

        Show_Frame(self.mood_songs_frame).execute()

        songs = self.make_mood("Happy", ["Pop", "Rock", "Hip Hop", "Disco"])
        
        for song in songs:
            self.mood_song_listbox.insert(tk.END, song)

    def make_mood_sad(self):
        self.mood_song_listbox.delete(0, tk.END)

        Show_Frame(self.mood_songs_frame).execute()

        songs = self.make_mood("Sad", ["Classical", "Blues", "Rock"])

        for song in songs:
            self.mood_song_listbox.insert(tk.END, song)

    def make_mood_chill(self):
        self.mood_song_listbox.delete(0, tk.END)

        Show_Frame(self.mood_songs_frame).execute()

        songs = self.make_mood("Chill", ["Classical", "Jazz"])

        for song in songs:
            self.mood_song_listbox.insert(tk.END, song)

    def make_mood_sexy(self):
        self.mood_song_listbox.delete(0, tk.END)

        Show_Frame(self.mood_songs_frame).execute()

        songs = self.make_mood("Sexy", ["Pop", "Classical", "Hip Hop", "Jazz", "Disco"])

        for song in songs:
            self.mood_song_listbox.insert(tk.END, song)

    def make_mood_travel(self):
        self.mood_song_listbox.delete(0, tk.END)

        Show_Frame(self.mood_songs_frame).execute()

        songs = self.make_mood("Travel", ["Pop", "Jazz"])

        for song in songs:
            self.mood_song_listbox.insert(tk.END, song)

    def run(self):
        self.mainloop()