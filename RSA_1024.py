from BigInt1024 import *
from  constant import ZERO , ONE , TWO , small_prime
import random
import sys
def GenKey(nb):
	p = PrimeGen(nb)
	q = PrimeGen(nb)
	res = (p,q)
	n = MulMod(p,q,BigInt(2**1024-1))

	q= q - ONE
	p= p-ONE
	
	phi = MulMod(p,q,n)	
	#find e
	e = BigInt(3)
	TWO = BigInt(2)
	while GCD(e,phi) > ONE :
		e+= TWO
	# tmp = random.randrange(1,int(str(phi))/2-1)
	# e = BigInt(tmp*2 + 1)
	# while GCD(e,phi) > ONE :
	# 	tmp = random.randrange(1,int(str(phi))/2-1)
	# 	e = BigInt(tmp*2 + 1)
	tmp = pow(int(str(e)),-1,int(str(phi)))
	d = BigInt(tmp)
	d = d % phi
	return ((e,n),(d,n),res)
def Encrypt(pubKey , plaintext):
	e,n = pubKey
	cipher = []
	for c in plaintext:
		crs = int(str(PowMod(BigInt(ord(c)),e,n)))
		char = ''
		while crs > 0 :
			char += chr(crs % 2**7 + 65)
			crs //= 2**7
		cipher.append(char)
	return cipher
def Decrypt(prvKey, ciphers):
	d,n = prvKey
	cip = []
	for cipher in ciphers:
		chars = 0 
		t = 1
		for char in cipher:
			chars += (ord(char) - 65) * t
			t*= 128
		cip.append(BigInt(chars))
	ret = ''

	for c in cip:
		ret += chr(int(str(PowMod(c,d,n))))

	return ret
def FastDecrypt(prvKey,p,q, ciphers):
	TWO = BigInt(2)
	ONE = BigInt(1)
	'''
	prvKey la khoa bao mat
	p,q la 2 so tu nhien tao ra n va thuoc kieu BIGINT
	cipher la 
	p < q
	'''
	d, n = prvKey

	# lay message
	cip = []
	for cipher in ciphers:
		chars = 0 
		t = 1
		for char in cipher:
			chars += (ord(char) - 65) * t
			t*= 128
		cip.append(BigInt(chars))

	

	# Dp = d mod phi(p-1)  rut gon d
	Dp = d % (p-ONE)
	# Dq = d mod phi(q-1)  rut gon d
	Dq = d % (q-ONE)
	ret = ''
	# ret = ''
	for c in cip :
		# Rut gon lai c
		Cp = c % p
		Cq = c % q

		# Tinh char theo p
		c1 = PowMod(Cp,Dp,p)
		# Tinh char theo q
		c2 = PowMod(Cq,Dq,q)

		#Ap dung m = c1 mod p 
		#		 m = c2 mod q
		#      =================
		#       c2 +q*x = c1 mod p          vi q > p

		#rut gon p theo q  va tinh q^-1 trong p
		q1 = PowMod((q%p),p-TWO,p)		# q^p-2 ap dung dinh ly EUler
		# char = c1 - c2       x = (c2-c1)*q1 mod p
		char = c1 -c2
		x = MulMod(char,q1,p)
		# thế x nguoc vào m = c2 + q*x
		ret += chr(int(str(c2 + MulMod(x,q,n))))


		#Cach khac ap dung dong du trung hoa:
	return ret
def PrimeTest(p):

	t = p - ONE
	a = random.choice(small_prime)
	b = BigInt(a)

	s = 0
	i = 0
	while t.Getbit(i) == 0 :
		i +=1
		s +=1
	if s == 0:
		return False
	t = t >> s
	neg1 = int(str(t))
	b_expo_t = PowMod(b,t,p)
	m = ONE
	for i in range(1,s):
		m = MulMod(b_expo_t,m,p)
		tmp = int(str(m))
		if tmp !=1 and tmp != neg1:
			return False
	return True	
def PrimeGen(n):
	t = random.randint(3,2**(n//2 - 1) - 1)
	p = BigInt(2*t + 1)
	while not PrimeTest(p) :
		p = p + TWO
	return p
if __name__ == '__main__':
	'''
	py RSA_1024.py todo parameters
	todo : 	-gen  sinh key -> parameters : so luong bit (max = 1024)
			-enc  ma hoa   -> parameters : e , n 
			-dec  giai ma  -> parameters : d , n
			-fdec giai ma nhanh -> parameters : e , n ,p , q 
	'''
	if len(sys.argv) < 3 : 
		print("To run: RSA_1024.py input arguments.")
		print("WARNING: Must be provide enough arguments")
		exit

	if sys.argv[1] == 'gen': 
		if int(sys.argv[2]) > 1024 or int(sys.argv[2]) <1:
			print("WARNING: Must be provide correct arguments (positive integer little equal 1024)")
		res = GenKey(int(sys.argv[2]))
		print("Public Key: ("  , res[0][0],',', res[0][1], " )\nPrivate Key: ( ", res[1][0] , ',' , res[1][1], ')')
	elif sys.argv[1] == 'enc':
		try:
			e = BigInt(int(sys.argv[2]))
			n = BigInt(int(sys.argv[3]))
		except:
			print("WARNING: Must be provide correct arguments")
			exit
		inp = input("Enter plaintext to Encrypt:")
		print(Encrypt((e,n),inp))
	elif sys.argv[1] == 'dec':
		try:
			d = BigInt(int(sys.argv[2]))
			n = BigInt(int(sys.argv[3]))
		except:
			print("WARNING: Must be provide correct arguments")
			exit
		inp = input("Enter cipher to Decrypt:")
		print(Decrypt((d,n),inp))
	elif sys.argv[1] == 'fdec':
		try:
			d = BigInt(int(sys.argv[2]))
			n = BigInt(int(sys.argv[3]))
			p = BigInt(int(sys.argv[4]))
			q = BigInt(int(sys.argv[5]))

		except:
			print("WARNING: Must be provide correct arguments")
			exit
		inp = input("Enter cipher to Decrypt:")
		print(FastDecrypt((d,n),p,q,inp))
	else:
		print("To run: RSA_1024.py input arguments.")
		print("WARNING: Must be provide correct arguments")

