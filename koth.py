from gpiozero import Button, LED
import datetime
import time
import os
from pygame import mixer
import threading

##-------[SETUP VARS]---------

round_start_delay = 45.0 #seconds before round start
time_to_win = 60.0*5.0 #first team to hold for x seconds wins
max_hold_time = (60.0*2.5)+5 #max time a team can hold the point before returning to neutral
button_hold_time = 2.5 #hold button for x seconds to capture hill

##-------[HID SETUP]---------

red_button = Button(14, pull_up = False, hold_time = button_hold_time, hold_repeat = False)
blue_button = Button(15, pull_up = False, hold_time = button_hold_time, hold_repeat = False)

red_LED = LED(23)
blue_LED = LED(24)

##-------[INIT VARS]---------
red_time = 0.0
blue_time = 0.0

point_holder = "none"
last_check = 0.0
last_change = 0.0

start_time = 0.0

mixer.init()

def play_sound(soundfile, wait = False, skippable = False):
	if skippable == True and mixer.music.get_busy():
		return 0
	
	if wait:
		while mixer.music.get_busy():
			continue
	
	mixer.music.load(soundfile)
	mixer.music.play()

#get elapsed time since start of round
def total_time():
	global start_time
	return time.monotonic()-start_time

#get time since last check
def interval_time():
	global last_check
	
	current_time = time.monotonic()
	
	interval_time = current_time-last_check
	
	last_check = current_time
	
	return interval_time


def holder_change(new_holder):
	global point_holder
	global last_change
	global last_check
	
	current_time = time.monotonic()
	
	last_change = current_time
	last_check = current_time
	
	point_holder = new_holder
	
	if new_holder == "none":
		blue_LED.off()
		red_LED.off()
		
		play_sound('/home/pi/sounds/BombDefused.mp3', True)
	
	if new_holder == "red":
		blue_LED.off()
		red_LED.on()
		
		play_sound('/home/pi/sounds/RedTeamCap.mp3', True)
		
	elif new_holder == "blue":
		red_LED.off()
		blue_LED.on()
	
		play_sound('/home/pi/sounds/BlueTeamCap.mp3', True)
		
def gameover():
	global red_time
	global blue_time
	
	os.system('clear')
	
	log=open("kothlog.txt","a")
	
	play_sound('/home/pi/sounds/Airhorn.mp3', True)
	play_sound('/home/pi/sounds/GameOver.mp3', True)
	
	if red_time > blue_time:
		play_sound('/home/pi/sounds/RedTeamWins.mp3', True)
		
		win_message = "Red Team Wins! "
		
	elif blue_time > red_time:
		play_sound('/home/pi/sounds/BlueTeamWins.mp3', True)
		
		win_message = "Blue Team Wins! "
		
	win_message = win_message + time_display()
		
	print(win_message)
	log.write(win_message)
	log.write("\n")
	log.close()
	input("press enter to end...")
	exit()

def time_display():
	global point_holder
	global red_time
	global blue_time
	
	elapsed_time_display = str(round(total_time()))
	red_time_display = str(round(red_time))
	blue_time_display = str(round(blue_time))
	
	display = "Elapsed Time: "+elapsed_time_display+" | Red: "+red_time_display+" | Blue: "+blue_time_display
		
	return display
	
def roundstart():
	global start_time
	global last_change
	
	play_sound('/home/pi/sounds/Airhorn.mp3', True)
	
	start_time = time.monotonic()
	last_change = start_time
	
	main()
	
def main():
	global point_holder
	global red_time
	global blue_time
	global last_change
	global max_hold_time
	
	current_time = time.monotonic()
	
	
	if point_holder == "red":
		red_time = red_time + interval_time()
	
	if point_holder == "blue":
		blue_time = blue_time + interval_time()
		
	if (((time.monotonic() - last_change) > max_hold_time) and (point_holder != "none")):
		holder_change("none")
		
	if red_time > time_to_win or blue_time > time_to_win:
		gameover()
	
	#os.system('clear')
	print(time_display())
	
	threading.Timer(1, main).start()

red_button.when_held = lambda: holder_change("red")
blue_button.when_held = lambda: holder_change("blue")

play_sound('/home/pi/sounds/PowerNodeUnderConstruction.mp3', True)
print("Game will start in "+str(round_start_delay)+" seconds")
threading.Timer(round_start_delay, roundstart).start()
