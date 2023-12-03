class Punto:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x},{self.y})'

    def equals(self, otro):
        return self.x == otro.x and self.y == otro.y

    def setXY(self, x, y):
        self.x = x
        self.y = y
