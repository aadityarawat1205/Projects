from tkinter import*
from PIL import Image,ImageTk
import tkinter.messagebox
from tkinter import filedialog
import os
import mutagen
import time
from mutagen.mp3 import MP3  #for length
from pygame import mixer
mixer.init()

class musicplayer:
    def __init__(self,Tk):
        self.root=Tk
        self.root.title('Spotipyy')
        self.root.geometry('1920x1200')
        self.root.configure(background='white')

        #label
        self.label1=Label(self.root,text='Lets play',bg='black',fg='white',font=22)
        self.label1.pack(side=BOTTOM,fill=X)
        
        self.filelabel=Label(text='Select and Play',font=100,bg='black',fg='white')
        self.filelabel.place(x=300,y=1030)
#adding image
        self.photo=ImageTk.PhotoImage(file='01.png')
        photo=Label(self.root,image=self.photo).place(x=700,y=700)
#function button
 
        def pausemusic():
            global paused
            paused=TRUE
            mixer.music.pause()  
            self.label1['text']='Music Paused...'

        def playmusic():
            try:
                paused
            except NameError:
                try:
                    mixer.music.load(filename)
                    mixer.music.play()
                    self.label1['text']='Music Playing...'
                    songinf()
                except:
                    tkinter.messagebox.showerror('ERROR','Please select music to be played')
                else:
                    mixer.music.unpause 

#creating buttons
#play button
        self.photo_B1=ImageTk.PhotoImage(file='02.png')
        photo_B1=Button(self.root,image=self.photo_B1,bd=0,command=playmusic).place(x=760,y=540)

#pause button
        self.photo_B2=ImageTk.PhotoImage(file='03.png')
        photo_B2=Button(self.root,image=self.photo_B2,bd=0,command=pausemusic).place(x=920,y=550)

        def volume(vol):
            volume=int(vol)/100
            mixer.music.set_volume(volume)
#volume bar
        self.scale=Scale(self.root,from_=100,to_=0,length=300,width=50,command=volume)
        self.scale.place(x=1243,y=750)

#mute
        def mute():
            self.scale.set(0)
            self.mute=ImageTk.PhotoImage(file='mute.png')
            mute=Label(self.root,image=self.mute).place(x=1400,y=700)

#openfile-
        def Openfile():
            global filename 
            filename=filedialog.askopenfilename()
#menu-
        self.menubar=Menu(self.root)
        self.root.configure(menu=self.menubar)

        self.submenu=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='File',menu=self.submenu)
        self.submenu.add_command(label='Open',command=Openfile)
        self.menubar.add_command(label='Exit',command=self.root.destroy)

        def About():
            tkinter.messagebox.showinfo('About us','MP3 offline music player')

        self.submenu2=Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label='Help',menu=self.submenu2)
        self.submenu2.add_command(label='About',command=About)

        def songinf():
            self.filelabel['text']='Current Music' + os.path.basename(filename)

        def toggle_dark_mode():
            if self.root["bg"] == "white":
                self.root.configure(background="black")
                self.label1.configure(bg="black", fg="white")
                self.filelabel.configure(bg="black", fg="white")
            else:
                self.root.configure(background="white")
                self.label1.configure(bg="white", fg="black")
                self.filelabel.configure(bg="white", fg="black")
            self.dark_mode_button=ImageTk.PhotoImage(file='02.png')
        photo_B1=Button(self.root,image=self.photo_B1,font=10,bd=0,command=toggle_dark_mode).place(x=1750,y=1030)
        

root=Tk()
obj=musicplayer(root)
root.mainloop()
