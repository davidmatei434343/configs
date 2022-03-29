#!/bin/bash
if pgrep -x "picom" > /dev/null
then
	killall picom
else
	picom --experimental-backend  -b --config ~/.config/qtile/scripts/picom.conf
fi
