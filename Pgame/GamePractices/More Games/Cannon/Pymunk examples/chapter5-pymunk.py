import pygame, pymunk
from pygame.locals import *
from pygame.color import *
from pymunk import Vec2d
import math, sys, random

def to_pygame(position):
    return int(position.x), int(-position.y+screen_y)

def line_to_pygame(line):
	body = line.body
	point_1 = body.position + line.a.rotated(body.angle)
	point_2 = body.position + line.b.rotated(body.angle)
	return to_pygame(point_1), to_pygame(point_2)
	
###options####
screen_x = 600
screen_y = 400
num_balls = 10


pygame.init()
screen = pygame.display.set_mode((screen_x, screen_y))
clock = pygame.time.Clock()
running = True

space = pymunk.Space()
space.gravity = (0.0, -200.0)

#create the base segment
base = pymunk.Segment(pymunk.Body(),(0,50), (screen_x, 0), 0)
base.elasticity = 0.90
space.add(base)

#create the spinner
spinner_points = [(0,0), (100, -50), (-100,-50)]
spinner_body = pymunk.Body(100000, 100000)
spinner_body.position = 300, 200
spinner_shape = pymunk.Poly(spinner_body, spinner_points)
spinner_shape.elasticity = 0.5
spinner_joint_body = pymunk.Body()
spinner_joint_body.position = spinner_body.position 
joint = pymunk.PinJoint(spinner_body, spinner_joint_body, (0,0), (0,0))
space.add(joint, spinner_body, spinner_shape)

#create the balls
balls = []
for i in range(1,num_balls):
	ball_x = int(screen_x/2)
	radius = random.randint(7,20)
	inertia = pymunk.moment_for_circle(radius, 0, radius, (0,0))
	body = pymunk.Body(radius, inertia)
	body.position = ball_x, screen_y
	shape = pymunk.Circle(body, radius, (0,0))
	shape.elasticity = 0.99
	space.add(body, shape)
	balls.append(shape)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.fill((0,0,0))
#draw the ball
    for ball in balls:
        pygame.draw.circle(screen,(100,100,100), to_pygame(ball.body.position), int(ball.radius), 0)

#draw the spinner        
    points = spinner_shape.get_vertices()
    points.append(points[0])
    pygame_points = []
    for point in points:
        x,y = to_pygame(point)
        pygame_points.append((x,y))    
    color = THECOLORS["red"]
    pygame.draw.lines(screen, color, False, pygame_points)

#draw the line
    pygame.draw.lines(screen, THECOLORS["lightgray"], False, line_to_pygame(base))
        
    space.step(1.0/50.0)
    pygame.display.flip()
    clock.tick(50)