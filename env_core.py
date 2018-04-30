import numpy as np
import random

class env2048:
	'''
		for i ...
			for j ...
				print(i, j)
		 ------ ------ ------ ------
		|  0  0|  0  1|  0  2|  0  3|
		 ------ ------ ------ ------
		|  1  0|  1  1|  1  2|  1  3|
		 ------ ------ ------ ------
		|  2  0|  2  1|  2  2|  2  3|
		 ------ ------ ------ ------
		|  3  0|  3  1|  3  2|  3  3|
		 ------ ------ ------ ------
	'''
	def __init__(self, n=4):
		self.n = n
		self.mat = np.zeros((n,n))
	
	
	def clean(self):
		'''
			Set self.mat to zeros
		'''
		self.mat = np.zeros((self.n, self.n))
	
	
	def add_blocks(self, max_pow=2, add_=1): 
		'''
			Add add_ numbers range(2, 2**(max_pow+1)) to self.mat
			If add_ is bigger than numbers of empty slot, then add=len(empty_slot)
		'''
		empty = np.array(np.where(self.mat==0)).transpose()
		if len(empty) < add_: add_ = len(empty)
		idx = np.random.choice(range(len(empty)), size=add_, replace=False)
		for i in idx:
			r, c = empty[i]
			fill_with = 2**np.random.randint(1, max_pow+1)
			self.mat[r][c] = fill_with		
	
	
	def start(self, max_pow=2, add_=3):
		'''
			Start Game
		'''
		self.clean()
		self.add_blocks(max_pow=max_pow, add_=add_)

		
	def Action_Top(self):
		'''
			Calculate Top Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		pass
						
	def Action_Bottom(self):
		'''
			Calculate Bottom Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		pass
		
	def Action_Left(self):
		'''
			Calculate Left Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		pass
		
	def Action_Right(self):
		'''
			Calculate Right Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		pass
		
	def check_empty(self):
		'''
			Return 
				n: integer, numbers of empty slot
		'''
		return np.count_nonzero(self.mat==0)
		
	
	def __str__(self):
		str = ' '
		for i in range(0, self.n): str += '------ '
		for i in range(0, self.n):
			str += '\n|'
			for j in range(0, self.n):
				str += '%3d%3d' % (i, j)
				#if self.mat[i][j] == 0: str += ' ' * 6
				#else: str += '%6d' % self.mat[i][j]
				
				str += '|'
			str += '\n '
			for i in range(0, self.n): str += '------ '
		return str



class env_wrapper(env2048):
	'''
		Wrap env2048 to gym-like api
	'''
	
	def __init__(self):
		super().__init__()
		pass
		
	def reset(self):
		super().start()
		return super().mat
	
	def step(self, action):
	
		# Apply Action
		if action == 0:
			super().Action_Top()
		elif action == 1:
			super().Action_Bottom()
		elif action == 2:
			super().Action_Left()
		elif action == 3:
			super().Action_Right()
		
		# Decide done, r, info [not done yet]
		done = False
		r = 1
		info = None
		
		return super().mat, done, r, info
		
	
	def render(self):
		pass
		
		
	def print_(self):
		print(super())
		
		
	def __str__(self):
		pass

if __name__ == '__main__':
	a = env2048()
	#a.add_blocks(max_pow=3, add=15)
	print(a)

	
	
