import random
import math

class Proover():
    def __init__(self, key, n, p, g):
        self.secret_key = key
        #self.n = n
        self.p = p
        self.g = g
        #self.open_key = self.secret_key ** 2 % n
        self.open_key = pow(g, self.secret_key, p)


    def send_x(self):
        self.z = int(random.random() * 1000 / 4)
        #return (self.z ** 2 % self.n)
        return pow(self.g, self.z, self.p)

    def get_bit(self, bit):
        if bit == 0:
            self.y = self.z
        if bit == 1:
            self.y = self.z + self.secret_key % (self.p - 1)
    
    def send_y(self):
        return self.y

class Verificator():
    def __init__(self, n, p, g):
        #self.n = n
        self.p = p
        self.g = g

    def get_public_key(self, key):
        self.public_key = key
    
    def get_x(self, x):
        self.x = x

    def send_bit(self):
        tmp = random.random()
        if tmp > 0.5:
            self.bit = 1
            return 1
        else:
            self.bit = 0
            return 0

    def check_y(self, y):
        if self.bit == 1 and self.x * self.public_key % self.p == pow(self.g, y, self.p):
            print("Approved")
        elif self.bit == 0 and self.x == pow(self.g, y, self.p):
            print("Approved")
        else:
            print("Failed")
        # if y ** 2 % self.n == (self.x * self.public_key) ** self.bit % self.n:
        #     print("Approved")
        # else:
        #     print("Failed")

def main():
    #n = int(input("Enter n=pq:")) # 4111
    p = int(input("Enter p:")) #4111
    q = int(input("Enter q:")) #12
    secret = int(input("Enter sekret key:")) #	любое
    Peggy = Proover(secret, 0, p, q)
    Victor = Verificator(0, p, q)
    print("Open key:", Peggy.open_key)
    Victor.get_public_key(Peggy.open_key)

    for i in range(10):
        Victor.get_x(Peggy.send_x())
        print("z:", Peggy.z)
        Peggy.get_bit(Victor.send_bit())
        print("bit:", Victor.bit)
        print("y:", Peggy.y)
        Victor.check_y(Peggy.send_y())

if __name__ == "__main__":
    main()
