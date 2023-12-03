

from Punto import Punto


class CurvaEliptica:

    def __init__(self, a, b, p):
        """
        y**2 = x**3 + ax + b (mod p)
        """
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        return f'y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})'

    def tiene(self, p: Punto):
        """
        Verifica si el punto p pertenece a la curva
        """
        return (p.y**2) % self.p == (p.x**3 + self.a*p.x + self.b) % self.p

    def puntos(self):
        """
        Devuelve la lista de puntos de la curva
        """
        puntos = []
        for x in range(self.p):
            for y in range(self.p):
                p = Punto(x, y)
                if self.tiene(p):
                    puntos.append(p)
        return puntos

    def orden(self, p: Punto):
        """
        Dado el punto p que pertenece al a curva elíptica, 
        nos regresa el mínimo entero k tal que kP = punto al infinito.
        !!!!!!!!!!!!!!!!!!!!!!!!1
        """
        k = 1
        while True:
            if p * k == Punto.INF:
                return k
            k += 1

    def cofactor(self, p: Punto):
        """
        Dado un punto p en la curva, nos regresa el total de puntos entre orden(p). 
        Obs: si el resultado es 1, la curva es buena.
        """
        return len(self.puntos()) // self.orden(p)

    def suma(self, p: Punto, q: Punto):
        """
        Suma de puntos en la curva elíptica
        """
        if p == Punto.INF:
            return q
        if q == Punto.INF:
            return p
        if p.x == q.x and p.y == -q.y:
            return Punto.INF
        if p.x == q.x and p.y == q.y:
            m = (3*p.x**2 + self.a) * self.inverso(2*p.y)
        else:
            m = (q.y - p.y) * self.inverso(q.x - p.x)
        x = m**2 - p.x - q.x
        y = m*(p.x - x) - p.y
        return Punto(x, y)

    def mult(self, p: Punto, k: int):
        """
        Multiplicación de un punto p por un escalar k
        """
        if k == 0:
            return Punto.INF
        if k == 1:
            return p
        if k % 2 == 0:
            return self.mult(self.suma(p, p), k // 2)
        return self.suma(p, self.mult(p, k-1))

    def inverso(self, x):
        """
        Inverso multiplicativo de x
        """
        for i in range(self.p):
            if (x * i) % self.p == 1:
                return i
        return None

    def inv(self, p: Punto):
        """
        Inverso aditivo de p
        """
        return Punto(p.x, -p.y)
