from abc import ABC, abstractmethod

class InterfacePlaylist(ABC):
    @abstractmethod
    def get_playlist_title(self):
        pass

    @abstractmethod
    def get_play_count(self):
        pass

    @abstractmethod
    def get_songs(self):
        pass

class AbstractPlaylist(InterfacePlaylist):
    def __init__(self,playlist_title: str):
        self.__playlist_title = playlist_title
        self.__play_count = 0
        self.__songs = []

    def get_playlist_title(self):
        return self.__playlist_title

    def get_play_count(self):
        return self.__play_count

    def get_songs(self):
        return self.__songs

class ConcretePlaylist(AbstractPlaylist):
    def __init__(self, playlist_title: str):
        super().__init__(playlist_title)
