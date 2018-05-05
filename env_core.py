import numpy as np

def wait_key():
	''' Wait for a key press on the console and return it. '''
	import os
	import sys
	result = None
	if os.name == 'nt':
		import msvcrt
		result = msvcrt.getch()
	else:
		import termios
		fd = sys.stdin.fileno()

		oldterm = termios.tcgetattr(fd)
		newattr = termios.tcgetattr(fd)
		newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
		termios.tcsetattr(fd, termios.TCSANOW, newattr)

		try:
			result = sys.stdin.read(1)
		except IOError:
			pass
		finally:
			termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	
	#print(result=='w')
	#print(result==b'w')

	return result

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
		self.score = 0
	
	
	def clean(self):
		'''
			Set self.mat to zeros
		'''
		self.mat = np.zeros((self.n, self.n))
		self.score = 0
		
	def calc_score(self):
		self.score = self.mat.sum()
		return self.score
	
	def add_blocks(self, max_pow=2, add_=2): 
		'''
			Add add_ numbers range(2, 2**(max_pow+1)) to self.mat
			If add_ is bigger than numbers of empty slot, then add=len(empty_slot)
		'''
		empty = np.array(np.where(self.mat==0)).transpose()
		if len(empty) < add_: add_ = len(empty)
		if add_ == 0: return
		actual_add = np.random.choice([i for i in range(1, add_+1)])
		#print(actual_add)
		idx = np.random.choice(range(len(empty)), size=actual_add, replace=False)
		for i in idx:
			r, c = empty[i]
			# More likely to choice smaller digit
			arr = [2**i for i in range(1, 1+max_pow)]
			p=[0.5+0.5**(max_pow)]+[0.5**(i+1) for i in range(1,max_pow)]
			fill_with = np.random.choice(arr, 1, p=p)[0]
			self.mat[r][c] = fill_with		
	
	
	def start(self, max_pow=2, add_=3):
		'''
			Start Game
		'''
		self.clean()
		self.add_blocks(max_pow=max_pow, add_=add_)
		self.score = self.calc_score()

	
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

		else:
			raise ValueError()
			
		return mat

	
	def Action_Up_(self):
		'''
			Calculate Up Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the left
		mat = np.copy(self.mat).transpose()
		mat = self.align(mat, 'Left')
				
		# Add 
		for i in range(self.n):
			for j in range(self.n-1):
				if mat[i][j+1] == mat[i][j]: 
					mat[i][j+1] = 0
					mat[i][j] *= 2
		
		# Allign Again
		mat = self.align(mat, 'Left').transpose()
		
		return mat
	
	
	def Action_Down_(self):
		'''
			Calculate Down Arrow Movement
			Return
				mat_ : a numpy matrix that present the mattrix after the movement
		'''
		# Align all numbers to the right
		mat = np.copy(self.mat).transpose()
		mat = self.align(mat, 'Right')
		
		# Add
		for i in range(self.n):
			for j in range(self.n-1):
				idx = self.n - 1 - j
				if mat[i][idx-1] == mat[i][idx]:
					mat[i][idx-1] = 0
					mat[i][idx] *= 2
		
		# Align Again
		mat = self.align(mat, 'Right').transpose()
		
		return mat

		
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

	
	def Action_Up(self):
		self.mat = self.Action_Up_()
		self.add_blocks() # args may need to change
		return self.check_dead()
		
		
	def Action_Down(self):
		self.mat = self.Action_Down_()
		self.add_blocks() # args may need to change
		return self.check_dead()
		
		
	def Action_Left(self):
		self.mat = self.Action_Left_()
		self.add_blocks() # args may need to change
		return self.check_dead()
		
		
	def Action_Right(self):
		self.mat = self.Action_Right_()
		self.add_blocks() # args may need to change
		return self.check_dead()
		
		
	def check_empty(self):
		'''
			Return 
				n: integer, numbers of empty slot
		'''
		return np.count_nonzero(self.mat==0)
	

	def check_dead(self):
		if (self.Action_Up_() == self.mat).all() and \
			(self.Action_Down_() == self.mat).all() and \
			(self.Action_Left_() == self.mat).all() and \
			(self.Action_Right_() == self.mat).all():
			return True
		else: return False
	
	
	def simple_game(self):
		import os
		import platform
		
		if platform.system() == 'Windows': clean = 'cls'
		elif platform.system() == 'Linux': clean = 'clear'
		
		os.system(clean)

		print("=== Simple 2048 Game on Terminal ===")
		print("Press w,a,s,d for moving blocks.")
		input("Press Enter To Start Game.")
	
		os.system(clean)
		self.start()
		print(self)
		print('\n'+' '*20, 'score =',self.score)
		
		while not self.check_dead():
			cmd = wait_key()
			os.system(clean)
			if   cmd == b'w' or cmd == 'w': ret = self.Action_Up()
			elif cmd == b's' or cmd == 's': ret = self.Action_Down()
			elif cmd == b'a' or cmd == 'a': ret = self.Action_Left()
			elif cmd == b'd' or cmd == 'd': ret = self.Action_Right()
			elif cmd == b'q' or cmd == 'q': ret = True
			else: 
				print(self)
				print('\n'+' '*20, 'score =',int(self.calc_score()))
				continue
			print(self)
			print('\n'+' '*20, 'score =',int(self.calc_score()))
			if ret:
				print('\n')
				print('\n ===== score: %8d ===== ' % self.calc_score())
				print('\n =====    Game Over    ===== \n\n')
				break

		restart = input('Play Again? (Y/n) ')
		restart = False if restart == 'n' else True
		return restart
	
	
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
			ret = super().Action_Up()
		elif action == 1:
			ret = super().Action_Down()
		elif action == 2:
			ret = super().Action_Left()
		elif action == 3:
			ret = super().Action_Right()
		
		# Decide done, r, info [not done yet]
		done = ret
		r = 1 if not ret else 0
		info = None
		
		return super().mat, done, r, info
		
	
	def render(self):
		pass
		
		
	def print_(self):
		print(super())
		
		
	def __str__(self):
		pass

if __name__ == '__main__':
	a = env2048(n=5)
	while a.simple_game():
		pass
	print('Bye.')
		

	
	
