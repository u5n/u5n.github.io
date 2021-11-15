# sum function use closed interval
lowbit = lambda x: x&-x

# index start from 1
class BIT1:
	__slots__='n','bit'
	def __init__(self, n):
		self.n = n
		self.bit = [0] * (n + 1)

	def add(self, idx, delta):
		while idx <= self.n:
			self.bit[idx] += delta
			idx += lowbit(idx)

	def sum(self, idx, idx2=None):
		""" 
		sum(A[1:idx+1]
		sum(A[idx:idx2+1] 
		"""
		if idx2!=None:
			return self.sum(idx2) - self.sum(idx - 1)
		
		ret = 0 
		while idx > 0:
			ret += self.bit[idx]
			idx -= lowbit(idx)
		return ret

# index start from 0
class BIT0:
	__slots__='n','bit'	
	def __init__(self, n):
		self.n = n
		self.bit = [0] * n

	def add(self, idx, delta):
		while idx < self.n:
			self.bit[idx] += delta
			idx += lowbit(idx+1)

	def sum(self, idx, idx2=None):
		if idx2!=None:
			return self.sum(idx2) - self.sum(idx - 1)
		else: 
			ret = 0 
			while idx >= 0:
				ret += self.bit[idx]
				idx -= lowbit(idx+1)
			return ret


# index start from 0, and 2 dimension
class BIT20:
	__slots__='m', 'n', 'bit'
	def __init__(self, shape):
		self.m,self.n = shape
		self.bit = {}
		
	def add(self, idx, delta):
		x = idx[0]
		while x < self.m:
			y = idx[1]
			while y < self.n:
				self.bit[x,y] = self.bit.get((x,y),0)+delta
				y += lowbit(y+1)
			x+=lowbit(x+1)
	def sum(self, idx, idx2=None):
		if idx2!=None:
			return self.sum(idx2) + self.sum((idx[0]-1,idx[1]-1)) - self.sum((idx2[0],idx[1]-1)) - self.sum((idx[0]-1,idx2[1]))
		ret=0
		x = idx[0]
		while x>=0:
			y = idx[1]
			while y>=0:
				ret += self.bit.get((x,y),0)
				y -= lowbit(y+1)
			x -= lowbit(x+1)
		return ret