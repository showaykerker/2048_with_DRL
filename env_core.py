import numpy as np

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
	
	
	def add_blocks(self, max_pow=2, add_=3): 
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

	
	def align(self, mat_, direction):
		'''
			Return a matrix after align
		'''
		
		mat = np.copy(mat_)
		if direction == 'Right':	
			for i in range(self.n):
				arr = [ v for v in list(np.copy(mat[i])) if v != 0 ] 
				for j in range(self.n-len(arr)): arr = [0] + arr
				mat[i,:] = np.array(arr)
				
		elif direction == 'Left':
			for i in range(self.n):
				arr = [ v for v in list(np.copy(mat[i])) if v != 0 ] 
				for j in range(self.n-len(arr)): arr.append(0)
				mat[i,:] = np.array(arr)
				
		elif direction == 'Top':
			raise NotImplementedError()
			
		elif direction == 'Bottom':
			raise NotImplementedError()
			
		else:
			raise ValueError()
			
		return mat

	
	def Action_Top_(self):
		'''
			Calculate Top Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the right
		mat = np.copy(self.mat)
		mat = self.align(mat, 'Right')
		
		pass
						
	def Action_Bottom_(self):
		'''
			Calculate Bottom Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the right
		mat = np.copy(self.mat)
		mat = self.align(mat, 'Right')
		
		pass
		
	def Action_Left_(self):
		'''
			Calculate Left Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the left
		mat = np.copy(self.mat)
		mat = self.align(mat, 'Left')
				
		# Add 
		for i in range(self.n):
			for j in range(self.n-1):
				if mat[i][j+1] == mat[i][j]: 
					mat[i][j+1] = 0
					mat[i][j] *= 2
		
		# Allign Again
		mat = self.align(mat, 'Left')
				
		return mat
		
	def Action_Right_(self):
		'''
			Calculate Right Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the right
		mat = np.copy(self.mat)
		mat = self.align(mat, 'Right')
		
		# Add
		for i in range(self.n):
			for j in range(self.n-1):
				idx = self.n - 1 - j
				if mat[i][idx-1] == mat[i][idx]:
					mat[i][idx-1] = 0
					mat[i][idx] *= 2
		
		# Align Again
		mat = self.align(mat, 'Right')
		
		return mat
	
	def Action_Right(self):
		self.mat = self.Action_Right_()
		self.add_blocks() # args may need to change
	
	
	def Action_Left(self):
		self.mat = self.Action_Left_()
		self.add_blocks() # args may need to change
		
		
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
				if self.mat[i][j] == 0: str += ' ' * 6
				else: str += '%6d' % self.mat[i][j]
				
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
	a.add_blocks(max_pow=3, add_=4)
	print(a)
	a.Action_Left()
	print(a)
	a.Action_Right()
	print(a)
	a.Action_Left()
	print(a)
	a.Action_Right()
	print(a)
	a.Action_Left()
	print(a)
	
	
