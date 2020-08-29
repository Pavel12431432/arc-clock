import pygame
import pygame.gfxdraw
import colors
import datetime
import math

# define window size(length and width)
WINSIZE = 900
# define the radius of each arc
ArcRadius = 400
# define the width of each arc
ArcWidth = 70
# define arc offset(ArcWidth - ArcOffset = distance between arcs)
ArcOffset = 75
# define size to use for font rendering
fontSize = 70

# initialize display with dimensions WINSIZE x WINSIZE
pygame.init()
screen = pygame.display.set_mode((WINSIZE, WINSIZE), 0, 32)
# set window caption
pygame.display.set_caption('Clock')
# define font
font = pygame.font.SysFont('consolas', fontSize)

# function to handle input
def inp():
	# check every input event
	for event in pygame.event.get():
		# check if window is closed
		if event.type == pygame.QUIT:
			# exit program
			quit()

# function to convert degrees to radians
def degreesToRadians(deg):
	return deg / 180.0 * math.pi

# function to draw arc
# default pygame function doesnt work
def drawArc(surface, x, y, r, th, start, stop, color):
	# define inner and outer vertices
	points_outer = []
	points_inner = []
	# if arc starts and stops at the same place then
	# draw full circle
	if abs(stop - start) == 0:
		stop = degreesToRadians(270)
	# get number of vertices
	n = round(r * abs(stop - start) / 1)
	# create inner/outer vertices
	for i in range(n):
		delta = i / (n - 1)
		phi0 = start + (stop - start) * delta
		x0 = round(x + r * math.cos(phi0))
		y0 = round(y + r * math.sin(phi0))
		points_outer.append([x0, y0])
		phi1 = stop + (start - stop) * delta
		x1 = round(x + (r - th) * math.cos(phi1))
		y1 = round(y + (r - th) * math.sin(phi1))
		points_inner.append([x1, y1])
	# draw a polygon between those vertices
	points = points_outer + points_inner
	pygame.gfxdraw.aapolygon(surface, points, color)
	pygame.gfxdraw.filled_polygon(surface, points, color)

# main draw function
# called at every loop
def draw():
	# reset screen to black
	screen.fill(colors.BLACK)
	# get the time
	now = datetime.datetime.now()
	# draw digital time in the center formatted to 2 digits (padded with zeros)
	screen.blit(font.render('{:02d}:{:02d}:{:02d}'.format(now.hour % 12, now.minute, now.second),
							True, colors.WHITE), (WINSIZE // 2 - int(fontSize * 2.2), WINSIZE // 2 - fontSize // 3))
	# draw second/minute/hour arc
	# draw green arc (seconds)
	drawArc(screen, WINSIZE // 2, WINSIZE // 2, ArcRadius, ArcWidth, degreesToRadians(-90),
			degreesToRadians(now.second / 60 * 360 - 90), colors.GREEN)
	# draw purple arc (minutes)
	drawArc(screen, WINSIZE // 2, WINSIZE // 2, ArcRadius - ArcOffset, ArcWidth, degreesToRadians(-90),
			degreesToRadians(now.minute / 60 * 360 - 90), colors.PURPLE)
	# draw orange arc (hours)
	drawArc(screen, WINSIZE // 2, WINSIZE // 2, ArcRadius - 2 * ArcOffset, ArcWidth, degreesToRadians(-90),
			degreesToRadians(now.hour % 12 / 12 * 360 - 90), colors.ORANGE)
	# update the display
	pygame.display.update()

# main loop
while True:
	# draw clock every loop
	draw()
	# check for input()
	inp()