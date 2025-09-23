
# easing.py
# cleure
# https://gist.github.com/cleure/e5ba94f94e828a3f5466
# Simple easing/tweening example in Python 

# ported from http://www.gizma.com/easing/
# based on Robert Penner's Easing Functions (http://robertpenner.com/easing/)
# see chapter 7 of his book


import math

# function inputs:
# t == specific time
# b == beginning position
# c == total change in position  (end position - begin position)
# d == total time duration
# function returns the position as the specified time


def linear(t, b, c, d):
    # linear velocity v = c/d
    return c*t/d + b    # == vt + b


def easeInQuad(t, b, c, d):
	t /= d
	return c*t*t + b


def easeOutQuad(t, b, c, d):
	t /= d
	return -c * t*(t-2) + b

def easeInOutQuad(t, b, c, d):
	t /= d/2
	if t < 1:
		return c/2*t*t + b
	t-=1
	return -c/2 * (t*(t-2) - 1) + b


def easeInOutCubic(t, b, c, d):
	t /= d/2
	if t < 1:
		return c/2*t*t*t + b
	t -= 2
	return c/2*(t*t*t + 2) + b

def easeInQuart(t, b, c, d):
	t /= d
	return c*t*t*t*t + b

def easeOutQuart(t, b, c, d):
	t /= d
	t -= 1
	return -c * (t*t*t*t - 1) + b

def easeInOutQuart(t, b, c, d):
	t /= d/2
	if t < 1:
		return c/2*t*t*t*t + b
	t -= 2
	return -c/2 * (t*t*t*t - 2) + b

def easeInQuint(t, b, c, d):
	t /= d
	return c*t*t*t*t*t + b

def easeOutQuint(t, b, c, d):
	t /= d
	t -= 1
	return c*(t*t*t*t*t + 1) + b

def easeInOutQuint(t, b, c, d):
	t /= d/2
	if t < 1:
		return c/2*t*t*t*t*t + b
	t -= 2
	return c/2*(t*t*t*t*t + 2) + b

def easeInSine(t, b, c, d):
	return -c * math.cos(t/d * (math.pi/2)) + c + b

def easeOutSine(t, b, c, d):
	return c * math.sin(t/d * (math.pi/2)) + b


def easeInOutSine(t, b, c, d):
	return -c/2 * (math.cos(math.pi*t/d) - 1) + b

def easeInExpo(t, b, c, d):
	return c * math.pow( 2, 10 * (t/d - 1) ) + b

def easeOutExpo(t, b, c, d):
	return c * ( -math.pow( 2, -10 * t/d ) + 1 ) + b


def easeInOutExpo(t, b, c, d):
	t /= d/2
	if t < 1: 
		return c/2 * math.pow( 2, 10 * (t - 1) ) + b
	t -= 1
	return c/2 * ( -math.pow( 2, -10 * t) + 2 ) + b

def easeInCirc(t, b, c, d):
	t /= d
	return -c * (math.sqrt(1 - t*t) - 1) + b

def easeOutCirc(t, b, c, d):
	t /= d;
	t -= 1
	return c * math.sqrt(1 - t*t) + b

def easeInOutCirc(t, b, c, d):
	t /= d/2
	if t < 1:
		return -c/2 * (math.sqrt(1 - t*t) - 1) + b
	t -= 2
	return c/2 * (math.sqrt(1 - t*t) + 1) + b



# ---------------------------------------------------

# from easing import *


# start = 100
# finish = 400
# duration = 60
# 
# for i in range(duration):
#     x = (480/duration) * i
# 
#     y1 = easeOutCirc(i, start, finish - start, duration)
#     y2 = easeInSine(i, start, finish - start, duration)
#     y3 = linear(i, start, finish - start, duration)
#     
#     print(int(x), int(y3))


