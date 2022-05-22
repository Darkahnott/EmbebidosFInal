#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #############################################################
# MultimediaCenter.py
#
# Authors:  Saúl Abraham Esparza Rivera & Paul Jaime Félix Flores
# Licence: MIT
# Date:    21/05/2022
# 
# A multimedia center that allows you to connect to your
# favorite streaming sites and also let's you enjoy your
# own media files (music, video and images) on it.
#
# ## #############################################################

from tkinter import *
from tkinter import ttk
from pygame import mixer
import webbrowser
import ctypes
import os
import vlc
import time
 
#Loading the cdll for display porpuses
x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XInitThreads()


#Function to open the desired service using the default web browser
def Spotify():
	webbrowser.open("https://www.spotify.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Deezer():
	webbrowser.open("https://www.deezer.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Tidal():
	webbrowser.open("https://www.tidal.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Netflix():
	webbrowser.open("https://www.netflix.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def PrimeVideo():
	webbrowser.open("https://www.primevideo.com/",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Disneyplus():
	webbrowser.open("https://www.disneyplus.com/login",new=2, autoraise=True)


#Function to show the available USB directories
def USBNav(root):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind2 = Tk()
	wind2.title("USB Selection Screen")
	wind2.geometry('500x500')
	wind2.config(bg="#8dc3d5")

	#Managing the USB filesystems

	#For use on a raspberryPI uncomment the following line
	#path = "/media/pi/"

	#For use on a linux filesystem uncomment the following line
	path = "/media/"+os.getlogin()+"/"

	#Listing all the files on the USB
	USBS = os.listdir(path)

	#Counting the number of USB devices
	numUsb = len(USBS)

	if len(USBS) > 0:
		#Creating and styling the button to "Enter the USB"
		USBButton1=Button(wind2,text= "Device: "+USBS[0],bg="#F64A5C",command=lambda:EnterUSB(wind2,USBS[0]))
		USBButton1.place(x=100,y=100)

		if len(USBS) > 1:
			#Creating and styling the button to "Enter the USB"
			USBButton2=Button(wind2,text= "Device: "+USBS[0],bg="#4AD55F",command=lambda:EnterUSB(wind2,USBS[1]))
			USBButton2.place(x=200,y=100)

			if len(USBS) > 2:
				#Creating and styling the button to "Enter the USB"
				USBButton3=Button(wind2,text= "Device: "+USBS[0],bg="#ECEA4E",command=lambda:EnterUSB(wind2,USBS[2]))
				USBButton3.place(x=300,y=100)

	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(wind2,text="Return to prevoius menu",bg="#F3CA65",command=lambda:MainMenu(wind2))
	GoBack.place(x=180,y=200)

	#New device detecting cycle
	try:
		while True:
			#Once again, we create the device(s) list 
			FindUSB = os.listdir(path)
			#If there's no new devices then we do nothing
			if numUsb == len(FindUSB):
				wind2.update_idletasks()
				wind2.update()
			else:
				#Else we create a new window with the retrieved info
				USBNav(wind2)
	except:
		print("Hello there!")

#Function to show the different media players
def EnterUSB(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind3 = Tk()
	wind3.title("Reproductor")
	wind3.geometry('500x500')
	wind3.config(bg="#66D8C6")
	
	#Show the button to choose to play "Music"
	botonMusica=Button(wind3,text="Music",bg="#66D863",command=lambda:playMusic(wind3,usb))
	botonMusica.place(x=90,y=30) 
	
	#Show the button to choose to play "Videos"
	botonVideo=Button(wind3,text="Videos",bg="#A272E4",command=lambda:playVideo(wind3,usb))
	botonVideo.place(x=240,y=30)
	
	#Show the button to choose to watch "Images"
	botonImagen=Button(wind3,text="Photos",bg="#69A6E7",command=lambda:playImage(wind3,usb))
	botonImagen.place(x=360,y=30)

	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(wind3,text="Return to prevoius menu",bg="#F3CA65",command=lambda:USBNav(wind3))
	GoBack.place(x=150,y=150)


#Function that manages the use cases for wether the device was disconnected or its empty
def Unplugged(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	windTemp = Tk()
	windTemp.title("Device offline")
	windTemp.geometry('500x500')
	windTemp.config(bg="#5FCC8F")

	#Error message
	textoTemp=Label(windTemp,text="Error while reading the device: "+usb+"\nCheck if it contains valid files or if it is still connected.")
	textoTemp.place(x=150,y=100)

	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(windTemp,text="Regresar",bg="#F64A5C",command=lambda:USBNav(windTemp))
	GoBack.place(x=250,y=200)


#Function Music player
def playMusic(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind4 = Tk()
	wind4.title("Musica")
	wind4.geometry('500x500')
	wind4.config(bg="#66D863")

	try:
		#Getting all the files from the device

		#For use on a raspberryPI uncomment the following line
		#path = "/media/pi/" + usb

		#For use on a linux filesystem uncomment the following line
		path = "/media/"+os.getlogin()+"/"+ usb


		#Creating the list of contents
		files = os.listdir(path)

		#Making an array to keep the playing file
		NumSong = [0]

		#Making a list of all the valid files
		MusicList = []

		#Close the window and return
		def ExitMedia(root,usb):
			mixer.music.stop()
			EnterUSB(root,usb)

		#Creating an array of all the .mp3 files available
		for item in files:
			if item.endswith(".mp3"): 
				MusicList.append(item)

		#List control
		if len(MusicList) == 0:

			#Error message
			NoMusic=Label(wind4,text="The current device does not contain music")
			NoMusic.pack()

			#Control buttons, allows you to go back to the previous menu
			GoBack=Button(wind4,text="Elegir otro reproductor",command=lambda:EnterUSB(wind4,usb))
			GoBack.pack()

		else:

			#Listing the labeled array
			for song in MusicList:
				TextSong=Label(wind4,text=song)
				TextSong.pack()

			#Initializing the player with the first song of the list
			mixer.init()

			#For use on a raspberryPI uncomment the following line
			#mixer.music.load("/media/pi/"+usb+"/"+MusicList[NumSong[0]])

			#For use on a linux filesystem uncomment the following line
			mixer.music.load("/media/"+os.getlogin()+"/"+usb+"/"+MusicList[NumSong[0]])
			

			mixer.music.set_volume(0.5)
			mixer.music.play()

			#Stopping the current song and starting the previous one
			def PrevSong(NumSong):

				#If we are at the last song, go back to the first one
				if NumSong[0] == 0:
					NumSong[0] = len(MusicList)-1
				else:
					NumSong[0] -= 1

				#Stop
				mixer.music.stop()

				#Routing the player

				#For use on a raspberryPI uncomment the following line
				#mixer.music.load("/media/pi/"+usb+"/"+MusicList[NumSong[0]])

				#For use on a linux filesystem uncomment the following line
				mixer.music.load("/media/"+os.getlogin()+"/"+usb+"/"+MusicList[NumSong[0]])

				#Play the file
				mixer.music.play()

			#Stopping the current song and play the next one

			def NextSong(NumSong):
				#If we are playing the first song, go to the last one
				if NumSong[0] == len(MusicList)-1:
					NumSong[0] = 0
				else:
					NumSong[0] +=1

				#Stop
				mixer.music.stop()

				#Routing the player

				#For use on a raspberryPI uncomment the following line
				#mixer.music.load("/media/pi/"+usb+"/"+MusicList[NumSong[0]])

				#For use on a raspberryPI uncomment the following line
				mixer.music.load("/media/"+os.getlogin()+"/"+usb+"/"+MusicList[NumSong[0]])


				#Play the file
				mixer.music.play()

			#Creating and styling the button to "Play previous song"
			PrevSongButton=Button(wind4,text="<<",bg="#F1C659",command=lambda:PrevSong(NumSong))
			PrevSongButton.place(x=20,y=90)

			#Creating and styling the button to "Pause song"
			PauseButton=Button(wind4,text="||",bg="#F1C659",command=lambda:mixer.music.pause())
			PauseButton.place(x=150,y=90)

			#Creating and styling the button to "Play"
			ResumeButton=Button(wind4,text=" > ",bg="#F1C659",command=lambda:mixer.music.unpause())
			ResumeButton.place(x=250,y=90)

			#Creating and styling the button to "Play next song"
			NextSongButton=Button(wind4,text=">>",bg="#F1C659",command=lambda:NextSong(NumSong))
			NextSongButton.place(x=400,y=90)

			#Creating and styling the button to "Exit the media player"
			ExitButton=Button(wind4,text="Return to media selection",bg="#66D8C6",command=lambda:ExitMedia(wind4,usb))
			ExitButton.place(x=200,y=200)
	except:
		#In case we cannot access the USB
		Unplugged(wind4,usb)




#Main menu funtion, works as the event handler and hub that calls the specific function when needed
def MainMenu(root):
	root.destroy()
	#Creating and styling window
	wind1 = Tk()
	wind1.title("Media Center")
	wind1.geometry('500x500')
	wind1.config(bg="#8dc3d5")
    
    #Creating the button and styling it, the calling the function of the service: Spotify
	SpotifyIMG=PhotoImage(file='Resources/img/buttons/')
	SpotifyButton=Button(wind1,image=SpotifyIMG,command=Spotify)
	SpotifyButton.place(x=20,y=30) #Marcamos las coordenadas del boton
	
	#Creating the button and styling it, the calling the function of the service: Deezer
	DeexerIMG=PhotoImage(file='Resources/img/buttons/')
	DeexerButton=Button(wind1,image=DeexerIMG,command=Deezer)
	DeexerButton.place(x=200,y=30)
	
	#Creating the button and styling it, the calling the function of the service: Tidal
	TidalIMG=PhotoImage(file='Resources/img/buttons/')
	TidalButton=Button(wind1,image=TidalIMG,command=Tidal)
	TidalButton.place(x=380,y=30)
    
    #Creating the button and styling it, the calling the function of the service: Netflix
	NetflixIMG=PhotoImage(file='Resources/img/buttons/')
	NetflixButton=Button(wind1,image=NetflixIMG,command=Netflix)
	NetflixButton.place(x=20,y=90)
	
	#Creating the button and styling it, the calling the function of the service: Prime
	PrimeIMG=PhotoImage(file='Resources/img/buttons/') 
	PrimeButton=Button(wind1,image=PrimeIMG,command=PrimeVideo)
	PrimeButton.place(x=200,y=90)
	
	#Creating the button and styling it, the calling the function of the service: D+
	DPlusIMG=PhotoImage(file='Resources/img/buttons/')
	DPlusButton=Button(wind1,image=DPlusIMG,command=Disneyplus)
	DPlusButton.place(x=380,y=90)
	
	##Creating the button and styling it, the calling the function of the service: USB handler
	USBIMG=PhotoImage(file='Resources/img/buttons/')
	USBButton=Button(wind1,image=USBIMG,command=lambda:USBNav(wind1))
	USBButton.place(x=220,y=170) 
	   
	#Creating the button and styling it, the calling the function of the service: Close and kill
	ExitIMG=PhotoImage(file='Resources/img/buttons/') 
	ExitButton=Button(wind1,image=ExitIMG,command=lambda:wind1.destroy())
	ExitButton.place(x=180,y=270) 

	wind1.mainloop()


#Function to desplay the welcome screen
def main():

	#Window dimmensions and other properties
	usr = os.getlogin()
	wind0 = Tk()
	wind0.title("Media Center - Welcome "+usr)
	wind0.geometry('500x500')
	
	bg=(PhotoImage(file = "Resources/img/back/1.png"))

	#Setting up the label
	Start=Label(wind0,text="Media Center",image=bg)
	Start.pack()
	
	#Creating a button to call the other fuctions adn the rest of the program
	StartIMG=PhotoImage(file='inicio.png')
	StartBTTN=Button(wind0,image=StartIMG,command=lambda:MainMenu(wind0))
	StartBTTN.place(x=200,y=200)  

	wind0.mainloop()

main()
