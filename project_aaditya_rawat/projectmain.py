from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox
from tkinter import filedialog
import os
import webbrowser
from pygame import mixer
import base64
import json
from requests import post, get
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Spotify API functions
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    token = json.loads(result.content)["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_song_and_get_track_url(token, song_name):
    headers = get_auth_header(token)
    search_url = "https://api.spotify.com/v1/search"
    query = f"?q={song_name}&type=track&limit=1"
    result = get(search_url + query, headers=headers)
    song_data = json.loads(result.content)

    if not song_data["tracks"]["items"]:
        raise Exception("Song not found")

    song = song_data["tracks"]["items"][0]
    track_url = song["external_urls"]["spotify"]
    return track_url

# Initialize mixer
mixer.init()

# GUI Class
class musicplayer:
    def __init__(self, Tk):
        self.root = Tk
        self.root.title('Spotipyy')
        self.root.geometry('1920x1080')
        self.root.configure(background='white')

        # Labels
        self.label1 = Label(self.root, text='Let\'s play', bg='black', fg='white', font=22)
        self.label1.pack(side=BOTTOM, fill=X)

        # Increase the font size for the "Select and Play" label
        self.filelabel = Label(text='Select and Play=>', font=("Arial",30), bg='black', fg='white')
        self.filelabel.place(x=300, y=860)

        # Entry for song
        self.song_entry = Entry(self.root, font=("Arial", 14), width=30)
        self.song_entry.place(x=1500, y=180)

        self.search_button = Button(self.root, text="Search Song on Spotify", bg="green", fg="white",
                                    font=("Arial", 12), command=self.search_song_from_input)
        self.search_button.place(x=1500, y=145)

        # Image resizing and display
        self.photo = Image.open('01.png')  # Load the image
        self.photo = self.photo.resize((900, 650))  # Resize the image (adjust size)
        self.photo = ImageTk.PhotoImage(self.photo)  # Convert the resized image to a Tkinter-compatible object
        Label(self.root, image=self.photo).place(x=580, y=150)  # Display the resized image at position (700, 200)

        # Play music function
        def playmusic():
            try:
                mixer.music.load(self.filename)
                mixer.music.play()
                self.label1['text'] = 'Music Playing...'
                songinf()
            except:
                tkinter.messagebox.showerror('ERROR', 'Please select music to be played')

        # Pause music function
        def pausemusic():
            mixer.music.pause()
            self.label1['text'] = 'Music Paused...'

        # Buttons
        self.photo_B1 = ImageTk.PhotoImage(file='02.png')  # Play
        Button(self.root, image=self.photo_B1, bd=0, command=playmusic).place(x=720, y=805)

        self.photo_B2 = ImageTk.PhotoImage(file='03.png')  # Pause
        Button(self.root, image=self.photo_B2, bd=0, command=pausemusic).place(x=920, y=805)

        # Volume control
        def volume(vol):
            mixer.music.set_volume(int(vol) / 100)

        self.scale = Scale(self.root, from_=100, to=0, length=300, width=50, orient=HORIZONTAL, command=volume)
        self.scale.place(x=1078, y=805)  # This places the horizontal scale on the window

        # Open file function
        def Openfile():
            self.filename = filedialog.askopenfilename()

        # Menu for file operations
        self.menubar = Menu(self.root)
        self.root.configure(menu=self.menubar)

        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.submenu)
        self.submenu.add_command(label='Open', command=Openfile)
        self.menubar.add_command(label='Exit', command=self.root.destroy)

        def About():
            tkinter.messagebox.showinfo('About us', 'MP3 offline music player')

        self.submenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.submenu2)
        self.submenu2.add_command(label='About', command=About)

        # Song information display
        def songinf():
            self.filelabel['text'] = 'Current Music: ' + os.path.basename(self.filename)

        # Dark mode toggle
        def toggle_dark_mode():
            if self.root["bg"] == "white":
                self.root.configure(background="black")
                self.label1.configure(bg="black", fg="white")
                self.filelabel.configure(bg="black", fg="white")
            else:
                self.root.configure(background="white")
                self.label1.configure(bg="white", fg="black")
                self.filelabel.configure(bg="white", fg="black")

        Button(self.root, text="Toggle Dark Mode",font=("Arial",16), bg='black', fg='white', command=toggle_dark_mode).place(x=1500, y=30)

    # Search for the song from the input field
    def search_song_from_input(self):
        song_name = self.song_entry.get().strip()
        if not song_name:
            tkinter.messagebox.showerror("Error", "Please enter a song name.")
            return

        token = get_token()
        try:
            track_url = search_song_and_get_track_url(token, song_name)
            self.play_song_from_spotify(track_url)
        except Exception as e:
            tkinter.messagebox.showerror("Error", f"Could not find song.\n\n{e}")
            return

    # Play the song from Spotify
    def play_song_from_spotify(self, track_url):
        webbrowser.open_new(track_url)
        self.label1['text'] = f"Playing song from Spotify: {track_url}"

# Launch the application
root = Tk()
obj = musicplayer(root)
root.mainloop()
