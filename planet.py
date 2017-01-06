#! /usr/bin/python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim

class Planet(object):
	def __init__(self):
		self.mass	= 0.0
		self.x		= 0.0
		self.y		= 0.0
		self.vx		= 0.0
		self.vy		= 0.0
		self.ax		= 0.0
		self.ay		= 0.0

	def step(self, dt):
		self.vx	= self.vx + (self.ax * dt)
		self.vy = self.vy + (self.ay * dt)
		
		self.x	= self.x + (self.vx * dt)
		self.y	= self.y + (self.vy * dt)

	def dx(self, other):
		return self.x - other.x

	def dy(self, other):
		return self.y - other.y

	def dx2(self, other):
		dx = self.dx(other)
		return dx**2

	def dy2(self, other):
		dy = self.dy(other)
		return dy**2

def init(planets, nP):
	if len(planets) != 0:
		return
	for i in range(0, nP):
		planets.append(Planet())

def sim_step(planets, dt):
	nP = len(planets)
	#ここで加速度計算
	G  = 1
	for i in range(0,nP):
		x  = planets[i].x
		y  = planets[i].y
		ax = 0.0
		ay = 0.0
		for j in range(0,nP):
			if i == j:
				continue
			m  = planets[j].mass
			m  = m*10
			dx = planets[j].x - x
			dy = planets[j].y - y
			dx2= dx**2
			dy2= dy**2
			r2 = dx2 + dy2
			r  = math.sqrt(r2)
			if r >= 10000:
				continue	#あんまり遠かったら計算しない
			cx = 1
			if dx < 0.0:
				cx = -1
			cy = -1
			if dy < 0.0:
				cy = -1
			
			if dx2 < 0.000001:
				if dy2 < 0.000001:
					print('衝突:' + str(i) + ',' + str(j))
				if dy2 != 0.0:
					ay = ay + (m * cy / dy2)
			elif dy2 < 0.000001:
				ax = ax + (m * cx / dx2)
			else:
				aa = m / r2
				ax = ax + (aa*dx / r)
				ay = ay + (aa*dy / r)
		
		planets[i].ax = ax
		planets[i].ay = ay
	
#	print('x:' + str(planets[1].vx) + ', y:' + str(planets[1].vy))
	
	for i in range(0,nP):
		planets[i].step(dt)
	

def plot(data, planets, dt, endtime):
	plot.count += 1
	if plot.count == 3:
		input('>>')
	if plot.time > endtime:
		return
	
	sim_step(planets, dt)
	plot.time += dt
	
	if plot.count%1 == 0:
		plt.cla()
		plt.title('planet time=' + str(round(plot.time,6)))
		plt.xlim(-1000, 1000)
		plt.ylim(-1000, 1000)
	
		nP = len(planets)
		for i in range(0,nP):
			plt.plot(planets[i].x, planets[i].y, 'o')

plot.time = 0.0
plot.count= 0

def main():
	nP = 5
	dt = 0.1
	endtime = 10000
	
	planets = []
	init(planets, nP)
	
	planets[0].mass	= 1000
	planets[1].x	= 600
	planets[1].y	= 0
	planets[1].vy	= 4
	planets[1].mass = 10
	planets[2].x	= 0
	planets[2].y	= 250
	planets[2].vx	= -6
	planets[2].vy	= 0
	planets[2].mass	= 5
	planets[3].x	= 0
	planets[3].y	= 400
	planets[3].vx	= -5
	planets[3].mass	= 5
	planets[4].mass = 5000
	planets[4].x	= 1000
	planets[4].y	= 500
	planets[4].vx	= 2
	planets[4].vy	= -2

	
	for i in range(4, nP):
		planets[i].mass = 0.01
		planets[i].x = i*10
		planets[i].y = 30
		planets[i].vx= 10
	
	fig = plt.figure()
	ani = anim.FuncAnimation(fig, plot, fargs = (planets, dt, endtime), interval=10)
#	ani.save('output.gif', writer='imagemagick')
	plt.show()

if __name__ == '__main__':
	main()
