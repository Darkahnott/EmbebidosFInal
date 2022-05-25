#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ## #########################################################################################################################################
# MultimediaCenter.py
#
# Authors:  Saúl Abraham Esparza Rivera & Paul Jaime Félix Flores
# 
# Date:    21/05/2022
# 
# A multimedia center that allows you to connect to your
# favorite streaming sites and also let's you enjoy your
# own media files (music, video and images) on it.
#
# Licence: MIT
# ## #########################################################################################################################################


from tkinter import *
from pygame import mixer
import webbrowser
import ctypes
import os
import vlc
import time
 
#Loading the cdll for display porpuses
x11 = ctypes.cdll.LoadLibrary('libX11.so')
x11.XInitThreads()

############################################################### MAIN ########################################################################


#Function to desplay the welcome screen
def main():

	#Window dimmensions and other properties
	usr = os.getlogin()
	wind0 = Tk()
	wind0.title("Media Center - Welcome "+usr)
	wind0.geometry('500x400')
	
	bg=(PhotoImage(file = "Resources/img/back/1.png"))

	#Setting up the label
	Start=Label(wind0,text="Media Center",image=bg)
	Start.pack()
	
	#Creating a button to call the other fuctions adn the rest of the program
	StartIMG=PhotoImage(file='Resources/img/buttons/Inicio.png')
	StartBTTN=Button(wind0,image=StartIMG,command=lambda:MainMenu(wind0),width=90,height=50,bg='black')
	StartBTTN.place(x=200,y=200)  

	wind0.mainloop()



############################################################### SERVICES ###################################################################



#Function to open the desired service using the default web browser
def HBO():
	webbrowser.open("https://play.hbomax.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Deezer():
	webbrowser.open("https://www.deezer.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Youtube():
	webbrowser.open("https://www.youtube.com/",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Netflix():
	webbrowser.open("https://www.netflix.com/login",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def PrimeVideo():
	webbrowser.open("https://www.primevideo.com/",new=2, autoraise=True)

#Function to open the desired service using the default web browser
def Disneyplus():
	webbrowser.open("https://www.disneyplus.com/login",new=2, autoraise=True)

############################################################### USB ###################################################################


#Function to show the available USB directories
def USBNav(root):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind2 = Tk()
	wind2.title("USB Selection Screen")
	wind2.geometry('500x400')
	wind2.config(bg="#8dc3d5")

	bg=(PhotoImage(file = "Resources/img/back/logo3.png"))
	#Setting up the label
	Start=Label(wind2,text="Media Center",image=bg)
	Start.pack()

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
		USBButton1.place(x=190,y=100)

		if len(USBS) > 1:
			#Creating and styling the button to "Enter the USB"
			USBButton2=Button(wind2,text= "Device: "+USBS[0],bg="#4AD55F",command=lambda:EnterUSB(wind2,USBS[1]))
			USBButton2.place(x=190,y=180)

			if len(USBS) > 2:
				#Creating and styling the button to "Enter the USB"
				USBButton3=Button(wind2,text= "Device: "+USBS[0],bg="#ECEA4E",command=lambda:EnterUSB(wind2,USBS[2]))
				USBButton3.place(x=190,y=260)

	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(wind2,text="Return to previous menu",bg="#F3CA65",command=lambda:MainMenu(wind2))
	GoBack.place(x=160,y=340)

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
		print("Hello there! A window has been refreshed")

#Function to show the different media players
def EnterUSB(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind3 = Tk()
	wind3.title("Media Player")
	wind3.geometry('500x400')

	bg1=(PhotoImage(file = "Resources/img/back/logo2.png"))
	#Setting up the label
	Test=Label(wind3,image=bg1)
	Test.pack()
	
	
	#Show the button to choose to play "Music"
	MusicIMG=PhotoImage(file='Resources/img/buttons/Music.png')
	MusicButton=Button(wind3,image=MusicIMG,command=lambda:playMusic(wind3,usb),width=90,height=50,bg='black')
	MusicButton.place(x=90,y=150) 
	
	#Show the button to choose to play "Videos"
	VideoIMG=PhotoImage(file='Resources/img/buttons/Video.png')
	VideoButton=Button(wind3,image=VideoIMG,command=lambda:playVideo(wind3,usb),width=90,height=50,bg='black')
	VideoButton.place(x=220,y=150)
	
	#Show the button to choose to watch "Images"
	PhotoIMG=PhotoImage(file='Resources/img/buttons/Photo.png')
	PhotoButton=Button(wind3,image=PhotoIMG,command=lambda:playImage(wind3,usb),width=90,height=50,bg='black')
	PhotoButton.place(x=350,y=150)



	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(wind3,text="Return to usb selector",bg="#F3CA65",command=lambda:USBNav(wind3))
	GoBack.place(x=160,y=340)

	wind3.mainloop()


#Function that manages the use cases for wether the device was disconnected or its empty
def Unplugged(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	windTemp = Tk()
	windTemp.title("Device offline")
	windTemp.geometry('500x400')
	windTemp.config(bg="#5FCC8F")

	#Error message
	errorMSG=Label(windTemp,text="Error while reading the device: "+usb+"\nCheck if it contains valid files or if it is still connected.")
	errorMSG.place(x=60,y=100)

	#Control buttons, allows you to go back to the previous menu
	GoBack=Button(windTemp,text="Return to previous menu",bg="#F64A5C",command=lambda:USBNav(windTemp))
	GoBack.place(x=160,y=340)

############################################################### MUSIC ###################################################################


#Function Music player
def playMusic(root,usb):

	#Deletes the recieved window
	root.destroy()

	#Starting the window with the desired styling
	wind4 = Tk()
	wind4.title("Music library")
	wind4.geometry('500x400')

	bg=(PhotoImage(file = "Resources/img/back/logo5.png"))

	#Setting up the label
	Start=Label(wind4,text="Media Center",image=bg)
	Start.pack()

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
			GoBack=Button(wind4,text="Return to media selection",command=lambda:EnterUSB(wind4,usb))
			GoBack.pack()

		else:

			#Listing the labeled array
			for song in MusicList:
				TextSong=Label(wind4,text=song)
				NameSong = song
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
			PrevSongIMG=PhotoImage(file='Resources/img/buttons/Prev.png')
			PrevSongButton=Button(wind4,image=PrevSongIMG,command=lambda:PrevSong(NumSong),width=30,height=30,bg='black')
			PrevSongButton.place(x=150,y=200)

			#Creating and styling the button to "Pause song"
			PauseSongIMG=PhotoImage(file='Resources/img/buttons/Pause.png')
			PauseButton=Button(wind4,image=PauseSongIMG,command=lambda:mixer.music.pause(),width=30,height=30,bg='black')
			PauseButton.place(x=200,y=200)

			#Creating and styling the button to "Play"
			PlaySongIMG=PhotoImage(file='Resources/img/buttons/Play.png')
			ResumeButton=Button(wind4,image=PlaySongIMG,command=lambda:mixer.music.unpause(),width=30,height=30,bg='black')
			ResumeButton.place(x=250,y=200)

			#Creating and styling the button to "Play next song"
			NextSongIMG=PhotoImage(file='Resources/img/buttons/Next.png')
			NextSongButton=Button(wind4,image=NextSongIMG,command=lambda:NextSong(NumSong),width=30,height=30,bg='black')
			NextSongButton.place(x=300,y=200)

			#Listening to
			NameSongButton=Button(wind4,text="You are listening to: "+NameSong,bg="black",state=DISABLED)
			NameSongButton.place(x=7,y=10)

			#Creating and styling the button to "Exit the media player"
			ExitButton=Button(wind4,text="Return to media selection",bg="#66D8C6",command=lambda:ExitMedia(wind4,usb))
			ExitButton.place(x=160,y=340)

			
			wind4.mainloop()

	except:
		#In case we cannot access the USB
		Unplugged(wind4,usb)

############################################################### VIDEO ###################################################################


#Video player
def playVideo(root,usb):
	root.destroy()
	#Styling and creating window
	wind5 = Tk()
	wind5.title("Video Player")
	wind5.geometry('500x400')
	wind5.config(bg="#A272E4")

	

	try:
		#Getting all the files from the device

		#For use on a raspberryPI uncomment the following line
		#path = "/media/pi/" + usb

		#For use on a linux filesystem uncomment the following line
		path = "/media/"+os.getlogin()+"/" + usb

		#Creamos una lista con todos los files dentro de la usb
		files = os.listdir(path)

		#Creating an aray to save the files
		VidList = []

		#Looking for valid files
		for item in files:
			#Filtering all .mp4 files
			if item.endswith(".mp4"):
				VidList.append(item)
	        

		#Array control
		if len(VidList) == 0:
			#Error message
			NoIMG=Label(wind5,text="The device has no valid video files")
			NoIMG.pack()

			#Control buttons, allows you to go back to the previous menu
			GoBack=Button(wind5,text="Go back to media selection",command=lambda:EnterUSB(wind5,usb))
			GoBack.pack()

		else:

			#Make an array of functions for the player
			MediaP=[]
			#Start the player
			media = vlc.MediaPlayer(path+"/"+VidList[0])
			MediaP.append(media)

			#Video Player
			def PlayVid(lista,path,MediaP):
				#Stop video
				MediaP[0].stop()
				#Assign the route
				MediaP[0] = vlc.MediaPlayer(path+"/"+typeV.get())
				#Play the file
				MediaP[0].play()

			#Stop the media player
			def ExitMedia(root,usb,MediaP):
				#Stop video
				MediaP[0].stop()
				#Exit to media menu
				EnterUSB(root,usb)

			#Listing the labeled array
			typeV=StringVar(value="a")
			for video in VidList:
				Radiobutton(wind5,text=video,variable=typeV,value=video,command=lambda:PlayVid(VidList,path,MediaP)).pack()


			bg=(PhotoImage(file = "Resources/img/back/logo4.png"))
			#Setting up the label
			Start=Label(wind5,image=bg)
			Start.pack()

			#Creating and styling the button to "Exit the media player"
			ExitButton=Button(wind5,text="Return to media selection",bg="#66D8C6",command=lambda:ExitMedia(wind5,usb,MediaP))
			ExitButton.place(x=160,y=340)

			wind5.mainloop()

	except:
		#In case we cannot access the USB
		Unplugged(wind5,usb)

############################################################### PHOTOS ###################################################################

#Image player
def playImage(root,usb):
	root.destroy()
	#Styling and creating window
	wind6 = Tk()
	wind6.title("Photo Player")
	wind6.geometry('500x400')
	wind6.config(bg="#69A6E7")

	bg=(PhotoImage(file = "Resources/img/back/logo6.png"))
	#Setting up the label
	Start=Label(wind6,text="Photos",image=bg)
	Start.pack()



	try:
		#Getting all the files from the device

		#For use on a raspberryPI uncomment the following line
		#path = "/media/pi/" + usb

		#For use on a linux filesystem uncomment the following line
		path = "/media/"+os.getlogin()+"/" + usb


		#Listing all the files
		files = os.listdir(path)

		#Filtered list
		IMGList = []

		#lookin for files
		for item in files:
			#Filtering all .jpg & .png files
			if item.endswith((".jpg",".png")):
				IMGList.append(item)

		#List control
		if len(IMGList) == 0:

			#Error message
			NoIMG=Label(wind6,text="The current device has no valid images.")
			NoIMG.pack()

			#Control buttons, allows you to go back to the previous menu
			GoBack=Button(wind6,text="Return to media selection",command=lambda:EnterUSB(wind6,usb))
			GoBack.pack()

		else:
			#Img Player
			def ShowIMG(album):
				for img in IMGList:
					media = vlc.MediaPlayer(path+"/"+img)
					media.play()
					#A little delay
					time.sleep(3)
					#Stop the player
					media.stop()
            
            #Creating and styling the button to "Start slideshow"
			botonRepetir=Button(wind6,text="Slideshow",bg="#F3CA65",command=lambda:ShowIMG(IMGList))
			botonRepetir.place(x=220,y=160)

			#Control buttons, allows you to go back to the previous menu
			ExitButton=Button(wind6,text="Return to media selection",bg="#66D8C6",command=lambda:EnterUSB(wind6,usb))
			ExitButton.place(x=160,y=340)


			wind6.mainloop()
	except:
		#In case we cannot access the USB
		Unplugged(wind6,usb)

############################################################### PRINCIPAL ###########################################################

#Main menu funtion, works as the event handler and hub that calls the specific function when needed
def MainMenu(root):
	root.destroy()
	#Creating and styling window
	wind1 = Tk()
	wind1.title("Media Center")
	wind1.geometry('500x400')

	bg=(PhotoImage(file = "Resources/img/back/logo.png"))
	#Setting up the label
	Start=Label(wind1,text="Media Center",image=bg)
	Start.pack()
    
    #Creating the button and styling it, the calling the function of the service: HBO
	HBOIMG=PhotoImage(file='Resources/img/buttons/HBO.png')
	HBOButton=Button(wind1,image=HBOIMG,command=HBO,width=90,height=50,bg='black')
	HBOButton.place(x=20,y=30)
	
	#Creating the button and styling it, the calling the function of the service: Deezer
	DeexerIMG=PhotoImage(file='Resources/img/buttons/Deezer.png')
	DeexerButton=Button(wind1,image=DeexerIMG,command=Deezer,width=90,height=50,bg='black')
	DeexerButton.place(x=200,y=30)
	
	#Creating the button and styling it, the calling the function of the service: Youtube
	YoutubeIMG=PhotoImage(file='Resources/img/buttons/Youtube.png')
	YoutubeButton=Button(wind1,image=YoutubeIMG,command=Youtube,width=90,height=50,bg='black')
	YoutubeButton.place(x=380,y=30)
    
    #Creating the button and styling it, the calling the function of the service: Netflix
	NetflixIMG=PhotoImage(file='Resources/img/buttons/Netflix.png')
	NetflixButton=Button(wind1,image=NetflixIMG,command=Netflix,width=90,height=50,bg='black')
	NetflixButton.place(x=20,y=150)
	
	#Creating the button and styling it, the calling the function of the service: Prime
	PrimeIMG=PhotoImage(file='Resources/img/buttons/Prime.png') 
	PrimeButton=Button(wind1,image=PrimeIMG,command=PrimeVideo,width=90,height=50,bg='black')
	PrimeButton.place(x=200,y=150)
	
	#Creating the button and styling it, the calling the function of the service: D+
	DPlusIMG=PhotoImage(file='Resources/img/buttons/Disney+.png')
	DPlusButton=Button(wind1,image=DPlusIMG,command=Disneyplus,width=90,height=50,bg='black')
	DPlusButton.place(x=380,y=150)
	
	##Creating the button and styling it, the calling the function of the service: USB handler
	USBIMG=PhotoImage(file='Resources/img/buttons/USB.png')
	USBButton=Button(wind1,image=USBIMG,command=lambda:USBNav(wind1),width=90,height=50,bg='black')
	USBButton.place(x=200,y=250) 
	   
	#Creating the button and styling it, the calling the function of the service: Close and kill
	ExitIMG=PhotoImage(file='Resources/img/buttons/Exit.png') 
	ExitButton=Button(wind1,image=ExitIMG,command=lambda:wind1.destroy(),width=90,height=50,bg='black')
	ExitButton.place(x=200,y=340)

	wind1.mainloop()

main()


