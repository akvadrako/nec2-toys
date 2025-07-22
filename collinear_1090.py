#!/usr/bin/env python

'''
Copyright 2015 Chris Kuethe (https://github.com/ckuethe)
MIT License
'''

# Inspiration:
#   http://adsb.alle.bg/antenna/collinear/
#   http://wiki.modesbeast.com/images/a/a5/ADS-B-antenna-drawing.gif
#   http://www.sprut.de/electronic/pic/projekte/adsb/adsb_en.html#antenne
#   http://martybugs.net/wireless/collinear.cgi

cm  = 'CM -------------------------------------------------------------------\n'
cm += 'CM collinear wire antenna for 1090MHz using 14AWG solid copper wire \n'
cm += 'CM \n'

cm += 'CM                       _                        _ \n'
cm += 'CM                      / \                      / \  \n'
cm += 'CM                     |   |                    |   | \n'
cm += 'CM                      \ /                      \ / \n'
cm += 'CM (feed)________________X________________________X________________________  ... \n'
cm += 'CM                   ^              ^ \n'
cm += 'CM                   |   ^          |             # Repeat these loops and wires \n'
cm += 'CM  l/2 wire --------+   |          |             # as much as is desired \n'
cm += 'CM  l/4 loop ------------+          |             # 5-7 stages are good \n'
cm += 'CM 3l/4 loop -----------------------+ \n'

cm += 'CM \n'
cm += 'CM -------------------------------------------------------------------\n'
cm += 'CE'

from nec2utils import *
from copy import copy

freq = 1090e6
vf = 1.0 # the internet says to try 0.9512 for HF antennas
wl = vf * 3e8 / freq
wire_radius = AWG(14)/2.0

m = Model(wire_radius, wl, freq, vf)

segs = 24
a1 = Point(0,0,0)
a2 = Point(0,0, wl * 0.5)


# L/2 wire
m.addWire(segs, a1, a2).feedAtStart()

# set up for a number of phase loop + wire stages
R=Rotation(deg(0),deg(0),deg(180))
loopscale = 1.00 # tweak to optimize antenna by varying phase loop size

for stages in range(0,5):
	# L/4 loop
	P=Point(loopscale * wl / 8 / math.pi ,0 , a2.z)
	helix_params = {'length': wl * 0.25 * loopscale, 'height': 2*AWG(14), 'turns': 1}
	m.addHelix(segs, a2, helix_params, rotate=R, translate=P)

	# 3L/4 wire
	a1 = copy(a2)
	a1.z += 2*AWG(14)
	a2.z = a1.z + wl * 0.75
	m.addWire(segs, a1, a2)

stepsize = 0.05 #MHz
steps = 2.0 / stepsize
startfreq = 1089 #MHz
cardStack = m.getText(start=startfreq, stepSize=stepsize, stepCount=steps)


fileName = 'collinear_1090.nec'
writeCardsToFile(fileName, cm, cardStack)
copyCardFileToConsole(fileName)
