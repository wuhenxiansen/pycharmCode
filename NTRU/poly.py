import random
import math
class can_not_div_Error(Exception):
	pass

def egcd(m, n):
    if n == 0:
        return (1, 0)
    a1 = b = 1
    a = 0
    b1 = 0
    c = m
    d = n
    q = c // d
    r = c % d
    while r:
        c = d
        d = r
        t = a1
        a1 = a
        a = t - q * a
        t = b1
        b1 = b
        b = t - q * b
        q = c // d
        r = c % d
    return (a + n) % n

class poly:
	def __init__(self,coe):
		self.coe = coe
		self.d = len(coe)
	def trim(self):
		L = len(self.coe)
		for i in range(L - 1,0,-1):
			if self.coe[i] == 0:
				self.coe.pop()
			else :
				break
		self.d = len(self.coe)
		return self
	def deg(self):
		for i in range(len(self.coe) - 1,-1,-1):
			if self.coe[i] != 0:
				return i
		return 0
	def expend(self,N):
		while len(self.coe) < N:
			self.coe.append(0)

	def StarMult(self,b,N,M):
		c = [0] * N
		self.expend(N)
		b.expend(N)
		for k in range(N - 1,-1,-1):
			c[k]  = 0
			j = k + 1
			for i in range(N - 1,-1,-1):
				if j == N :
					j = 0
				if self.coe[i] != 0 and b.coe[j] != 0:
					c[k] = c[k] + (self.coe[i] * b.coe[j])
					c[k] %= M
				j += 1
		self.trim()
		b.trim()
		return poly(c).trim()
	def polymult(self,b,M = -1):
		N = b.d + self.d
		c = [0] * (N + 1)
		self.expend(N + 1)
		b.expend(N + 1)
		for i in range(0,self.d + 1):
			for j in range(0,b.d + 1):
				c[i + j] += self.coe[i] * b.coe[j]
				if M != -1:
					c[i + j] %= M
		self.trim()
		b.trim()
		c = poly(c).trim()
		return c

	def polyadd(self,b,M = -1):
		N = max(b.d,self.d)
		c = [0] * (N + 1)
		self.expend(N + 1)
		b.expend(N + 1)
		for i in range(0,N + 1):
			c[i] = self.coe[i] + b.coe[i]
			if (M != -1):
				c[i] %= M
		self.trim()
		b.trim()
		return poly(c).trim()

	def polysub(self,b,M = -1):
		N = max(b.d,self.d)
		c = [0] * (N + 1)
		self.expend(N + 1)
		b.expend(N + 1)
		for i in range(0,N + 1):
			c[i] = self.coe[i] - b.coe[i]
			if (M != -1):
				c[i] %= M
		self.trim()
		b.trim()
		return poly(c).trim()
	def polydiv(self,b,p):
		if b.is_z():
			1/0
		N = b.deg()
		r = self
		q = [0]
		q = poly(q)
		deg_b = b.deg()
		b_N = b.coe[deg_b]
		gcd = math.gcd(b_N,p)
		if gcd != 1:
			raise can_not_div_Error()
		u = egcd(b_N,p)
		while  r.deg() >= N and not r.is_z():
			d = r.deg()
			v = [0] * (d - N) + [u * r.coe[d]]
			v = poly(v).trim()
			tmp = v.polymult(b,p)
			r = r.polysub(tmp,p).trim()
			q = q.polyadd(v).trim()
		q = q.trim()
		r = r.trim()
		return (q,r)

	def is_z(self):
		return self.deg() == 0 and self.coe[0] == 0

	def egcd(self,n,p):
		m  = self
		if n.is_z():
			return (poly([1]),poly([0]),m)
		one = poly([1])
		z_ = poly([0])
		a1  = b  = one
		a = z_
		b1 = z_
		c = m
		d = n
		tmp =  c.polydiv(d,p)
		q = tmp[0]
		r = tmp[1]
		while r.is_z() != True:
			c = d
			d = r
			t = a1
			a1 = a
			a = t.polysub(q.polymult(a,p),p)
			t = b1
			b1 = b
			b = t.polysub(q.polymult(b,p),p)
			tmp = c.polydiv(d,p)
			q = tmp[0]
			r = tmp[1]
		return (a,b,d)
	def multInt(self,k,p = -1):
		for i in range(0,len(self.coe)):
			self.coe[i] *= k;
			if p != -1:
				self.coe[i] %= p 
		return self

	def inv_p(self,N,p):
		P = [0] * (N + 1)
		P[0] = -1
		P[N] = 1
		P = poly(P)
		res = self.egcd(P,p)
		u = res[0]
		v = res[1]
		d = res[2]
		#print(d.coe)
		if res[2].deg() is 0:
			inv_d = egcd(d.coe[0],p)
			for i in range(0,len(u.coe)):
				u.coe[i] *= inv_d
				u.coe[i] %= p
			return u.trim()
		else:
			return False
	def inv_pr(self,N,p,e):
		P = [0] * (N + 1)
		P[0] = -1
		P[N] = 1
		P = poly(P)
		inv = self.inv_p(N,p)
		a = self
		if inv is False :
			return False
		n = p
		pr = pow(p,e)
		while n < pr:
			n = n * n
			ttmp = a.polymult(inv.polymult(inv,n),n)
			inv  =  inv.multInt(2).polysub(ttmp,n)
			inv = inv.polydiv(P,n)[1]

		for i in range(0,len(inv.coe)):
			inv.coe[i] %= pr

		inv = inv.trim()
		return inv
	def inv(self,N,p,k):
		return self.inv_pr(N,p,k)


#print(randpoly(10).coe)
#a = poly([9,7,1])
#b = poly([5,2,3])
#c = poly([-1,1,0,0,1])
#P = poly([-1,0,0,0,0,1])


#print(a.StarMult(b,len(a.coe),100).coe)
#d = c.inv_Fq(5,32)
#e = poly([1, 0, 1, 1, 0, 0])
#print(c.StarMult(e,5,2).coe)
#print(c.StarMult(d,5,32).coe)
#d =b.polydiv(a,7) 
#e = a.polymult(b,100).polydiv(P,100)
#e = a.egcd(b,7)
#print(e[0].coe,e[1].coe,e[2].coe)
#print(a.inv_p(3,7).coe)
#print(a.inv_p(3,7).StarMult(a,3,7).coe)
#f = c.inv(5,3,1)
#print(f.coe)
#if f is not False:
#	print(c.polymult(f,3).polydiv(P,3)[1].coe)
#else :
#	print(f)