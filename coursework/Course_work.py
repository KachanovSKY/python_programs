from PIL import Image, ImageDraw 
from random import randint
from re import findall
import math

def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def gcdExtended(a, b):
    if a == 0 :
        return b,0,1
    gcd,x1,y1 = gcdExtended(b%a, a)
    x = y1 - (b//a) * x1
    y = x1
    return gcd,x,y

def reverse(n, p):
    gcd, x, y = gcdExtended(n, p)
    if gcd == 1:
        return (x % p + p) % p
    else:
        return -1

def stega_encrypt(mes, img, k, saveName):
	draw = ImageDraw.Draw(img)
	width = img.size[0]
	height = img.size[1]
	pix = img.load()
	f = open(k,'w')
	s = [int(i) for i in list(bin(mes[0]))[2:]]
	r = [int(i) for i in list(bin(mes[1]))[2:]]
	y = [int(i) for i in list(bin(mes[2]))[2:]]


	if len(s) >= len(r) and len(s) >= len(y):
		for i in range(len(s) - len(r)):
			r.insert(0, 0)
		for i in range(len(s) - len(y)):
			y.insert(0, 0)
	elif len(r) >= len(s) and len(r) >= len(y):
		for i in range(len(r) - len(s)):
			s.insert(0, 0)
		for i in range(len(r) - len(y)):
			y.insert(0, 0)
	elif len(y) >= len(s) and len(y) >= len(r):
		for i in range(len(y) - len(s)):
			s.insert(0, 0)
		for i in range(len(y) - len(r)):
			r.insert(0, 0)

	for i in range(len(s)):
		key = (randint(1, width-10), randint(1, height-10))
		red, green, blue = pix[key]
		red = ((red >> 1) << 1) | y[i]
		green = ((green >> 1) << 1) | s[i]
		blue = ((blue >> 1) << 1) | r[i]
		draw.point(key, (red, green, blue))
		f.write(str(key)+'\n')
	
	print('keys were written to the keys.txt file')
	img.save("C:\\Users\\Vladislav\\Videos\\Desktop\\new" + saveName, "PNG")
	f.close()

def stega_decrypt(path, k):
	s = 0
	r = 0
	y = 0
	a = []
	keys = []
	img = Image.open(path)
	pix = img.load()
	f = open(k,'r')
	string = str([line.strip() for line in f])

	for i in range(len(findall(r'\((\d+)\,',string))):
		keys.append((int(findall(r'\((\d+)\,',string)[i]), int(findall(r'\,\s(\d+)\)', string)[i])))
	for key in keys:
		a.append(pix[tuple(key)])
	for i in a:
		s = (s << 1) | (i[1] % 2)
		r = (r << 1) | (i[2] % 2)
		y = (y << 1) | (i[0] % 2)
	return s, r, y

def check(n, p):
	for i in range(1, n + 1):
		if n % i == 0 and p % i == 0:
			return False
	return True

def main(path):
	g = []
	for i in range(pow(2, 32) - 100, pow(2, 32)):
		if is_prime(2*i + 1):
			g.append(i)
	
	print("Возможные g:", g)
	g = g[randint(0, len(g))]
	print("Выбраное g:", g)
	p = g * 2 + 1
	print("Полученое p:", p)
	x = randint(1, p - 1)
	print("Закрытый ключ x:", x)
	y = pow(g, x, p)
	print("Открытый ключ y:", y)
	k = 0
	
	for i in range(randint(2, p-2), p):
		if math.gcd(i, p) == 1 and reverse(i, p-1) != -1:
			k = i
			break

	print("Случайное k:", k)
	r = pow(g, k, p)
	print("Первый ключ подписи r:", r)
	revk = reverse(k, p-1)
	img = Image.open(path)
	#input("Путь к картинке: ")
	width = img.size[0]
	height = img.size[1]
	s = (revk * (((height * width) - x * r) % (p - 1))) % (p - 1)
	print("Второй ключ подписи s:", s)
	keys = "C:\\Users\\Vladislav\\Videos\\Desktop\\keys.txt"
	#input("Путь к ключам пикселей: ")
	stega_encrypt([r, s, y], img, keys, path[path.rfind("\\") + 1:])
	nr, ns, ny = stega_decrypt(path[:path.rfind("\\")+ 1] + "new" + path[path.rfind("\\") + 1:], keys)
	print("Раскодированые ключи:\n s:", ns, "\n r:", nr, "\n y:", ny)

	if (pow(ny, nr, p) * pow(nr, ns, p)) % p == pow(g, (height * width), p):
		print ("Подпись подтверждена\n")
	else:
		print ("Подпись не подтверждена\n")

if __name__ == '__main__':
	path = ["C:\\Users\\Vladislav\\Videos\\Desktop\\kodim16.png", 
	 "C:\\Users\\Vladislav\\Videos\\Desktop\\BnW.png", 
	 "C:\\Users\\Vladislav\\Videos\\Desktop\\yellow.png"]
	for i in path:
		main(path[0])