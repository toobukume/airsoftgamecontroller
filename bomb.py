from gpiozero import Button, LED
import time
import os
from pygame import mixer
import threading

##-------[SETUP VARS]---------

time_limit = 60.0*20.0 # round time limit
arm_time = 10.0 # hold red button for x seconds to arm bomb
defuse_time = 10.0 # hold blue button for x seconds to defuse bomb
bomb_time = 60.0*2.0  # once armed, bomb will explode in x seconds unless defused

##-------[END SETUP VARS]---------

#arm = red, defuse = blue
arm_button = Button(14, pull_up = False, hold_time = arm_time, hold_repeat = False)
defuse_button = Button(15, pull_up = False, hold_time = defuse_time, hold_repeat = False)

red_LED = LED(23)
blue_LED = LED(24)

bomb_status = "cold" # cold, ready, armed, defused, boom
armed_time = 0.0

#audio file player
mixer.init()

def keep_alive():
	playSound('/home/pi/sounds/ClockTick.mp3')
	threading.Timer(60.0, keep_alive).start()

#play sound effects
def playSound(soundfile, wait = False, skippable = False):
    if skippable == True and mixer.music.get_busy():
        return 0
    
    mixer.music.load(soundfile)
    mixer.music.play()
    
    if wait:
        while mixer.music.get_busy():
            continue

def arm_bomb_pressed():
	global bomb_status
	
	if bomb_status == "ready":
		playSound('/home/pi/sounds/BombArmStart.mp3')
	
def arm_bomb_held():
	global bomb_status
	global timeout
	global bomb_time
	global bomb_timeout
	
	if bomb_status == "ready":
		print("The bomb has been armed!")
		
		bomb_status = "armed"
		red_LED.blink(1,1)
		playSound('/home/pi/sounds/BombArmed.mp3', True)
		
		timeout.cancel()
		
		print("Bomb will go off in "+str(bomb_time)+" seconds unless defused!")
		
		bomb_timeout = threading.Timer(bomb_time, game_over)
	
def defuse_bomb_pressed():
	global bomb_status
	
	if bomb_status == "armed":
		playSound('/home/pi/sounds/BombDefuseStart.mp3')
	
def defuse_bomb_held():
	global bomb_status
	
	if bomb_status == "armed":
		bomb_status = "defused"
		game_over()
	
def game_over():
	global bomb_status
	
	print("Game over!")
	
	if bomb_status == "ready":
		print("The bomb wasn't planted! CT Wins!")
		blue_LED.on()
		playSound('/home/pi/sounds/CTWin.mp3', True)
    
	elif bomb_status == "defused":
		print("Bomb Defused! CT Wins!")
		red_LED.off()
		blue_LED.on()
		playSound('/home/pi/sounds/BombDefusedCTWin.mp3')
		
	elif bomb_status == "armed":
		print("bomb exploded!")
		red_LED.on()
		playSound('/home/pi/sounds/BombExplosionTWin.mp3')
		
	input("press enter to quit")
	exit(0)
		
arm_button.when_pressed = arm_bomb_pressed
defuse_button.when_pressed = defuse_bomb_pressed

arm_button.when_held = arm_bomb_held
defuse_button.when_held = defuse_bomb_held

#ROUND START

playSound('/home/pi/sounds/BombTDoThis.mp3',True)
time.sleep(1)
playSound('/home/pi/sounds/Airhorn.mp3',True)

bomb_status = "ready"

threading.Timer(60.0, keep_alive).start()

timeout = threading.Timer(time_limit, game_over)
timeout.start()

input("Press enter to quit")