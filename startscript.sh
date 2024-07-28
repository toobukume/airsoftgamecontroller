#!/bin/bash

clear

#echo "Waiting for bluetooth to finish loading"
#sleep 20s

echo "Connect to speaker"
#figure out how to start a loop and escape on connect...

#Blue Speaker
#5C:FB:7C:24:2C:BD

#Pyle Speakers
#C8:3F:C7:AB:4E:C4

#Bluetooth sometimes isn't fully started right after boot. So you attempt to connect to the speaker. If it can't connect, the script will keep trying every 5 seconds. Once connected, it continues to start the game.

while :
do
	btattempt=`bluetoothctl -- connect C8:3F:C7:AB:4E:C4`
	echo $btattempt
	if [[ "$btattempt" =~ "Connection successful" ]]
	then
		break
	else
		echo "Waiting for bluetooth to load..."
		sleep 5s
	fi
done

#end loop

echo "Launch game"
python3 /home/pi/koth.py


#Bluetooth Adapters
#Internal: DC:A6:32:50:06:EA
#USB: E8:48:B8:C8:20:00


#read game selector switch

#gpio mode 25 in

#gametype=$(gpio read 25)

#if [ $gametype -eq 0 ]; then
#	echo "KOTH2"
#	python3 /home/pi/koth.py
#elif [ $gametype -eq 1 ]; then
#	echo "KOTH2"
#	python3 /home/pi/koth.py
#fi