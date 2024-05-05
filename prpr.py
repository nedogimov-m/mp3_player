import time
from threading import Thread
from tkinter import *
import pygame

import os


class CheckableTk(Tk):
    def __init__(self, *args, **kwargs):
        self.running = True
        super().__init__(*args, **kwargs)

    def mainloop(self, *args, **kwargs):
        self.running = True
        try:
            return super().mainloop(*args, **kwargs)
        finally:
            self.running = False


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("1000x200+200+200")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar(value="-Не играет")

        self.SONG_END = pygame.USEREVENT + 1

        trackframe = LabelFrame(self.root, text="Играет песня", font=("Arial", 15, "bold"), bg="Navyblue",
                                fg="white", bd=5, relief=GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)

        Label(trackframe, textvariable=self.track, width=20, font=("Arial", 24, "bold"),
              bg="Orange", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        Label(trackframe, textvariable=self.status, font=("Arial", 18, "bold"), bg="orange",
              fg="gold").grid(row=0, column=1, padx=1, pady=5)

        buttonframe = LabelFrame(self.root, text="Панель управления", font=("Arial", 15, "bold"), bg="grey",
                                 fg="white", bd=5, relief=GROOVE)
        buttonframe.place(x=0, y=100, width=600, height=100)

        Button(buttonframe, text="Проигрывать", command=self.playsong, width=10, height=1,
               font=("Arial", 16, "bold"), fg="navyblue", bg="pink").grid(row=0, column=0,
                                                                          padx=10, pady=5)

        self.pause = Button(buttonframe, text="Пауза", command=self.pausesong, width=8, height=1,
                            font=("Arial", 16, "bold"), fg="navyblue", bg="pink")

        self.pause.grid(row=0, column=1, padx=10, pady=5)

        songsframe = LabelFrame(self.root, text="Плейлист", font=("Arial", 15, "bold"), bg="grey",
                                fg="white", bd=5, relief=GROOVE)
        songsframe.place(x=600, y=0, width=400, height=200)
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="gold", selectmode=SINGLE,
                                font=("Arial", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=GROOVE)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        os.chdir("songs/")

    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Играет")
        self.pause.config(text="Пауза", command=self.pausesong, width=8, height=1,
                          font=("Arial", 16, "bold"), fg="navyblue", bg="pink")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.set_endevent(self.SONG_END)
        pygame.mixer.music.play()

    def pausesong(self):
        if not pygame.mixer.music.get_busy():
            return
        self.status.set("-Пауза")
        pygame.mixer.music.pause()
        self.pause.config(text="Возобновить", command=self.unpausesong, width=10, height=1,
                          font=("Arial", 16, "bold"), fg="navyblue", bg="pink")

    def unpausesong(self):
        self.status.set("-Играет")
        pygame.mixer.music.unpause()
        self.pause.config(text="Пауза", command=self.pausesong, width=8, height=1,
                          font=("Arial", 16, "bold"), fg="navyblue", bg="pink")

    def check_playing(self):
        while True:
            if not self.root.running:
                break
            for event in pygame.event.get():
                if event.type == self.SONG_END:
                    self.status.set("-Не играет")

    def check_dir(self):
        old = []
        while True:
            if not self.root.running:
                break
            songtracks = os.listdir()
            if old != songtracks:
                self.playlist.delete(0, 9999)
                for track in songtracks:
                    self.playlist.insert(END, track)
            old = songtracks
            time.sleep(0.5)


root_tk = CheckableTk()  # костыль
mp = MusicPlayer(root_tk)

threads = [mp.check_playing,
           mp.check_dir]

for thread in threads:
    Thread(target=thread).start()

root_tk.mainloop()
