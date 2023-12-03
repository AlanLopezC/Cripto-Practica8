
from Punto import Punto
from CurvaEliptica import CurvaEliptica
from random import randint


class Entidad:

    def __init__(self, nombre: str, mensaje: str, curva: CurvaEliptica, puntoGenerador: Punto):
        self.nombre = nombre
        self.mensaje = mensaje
        self.curva = curva
        self.puntoGenerador = puntoGenerador
        self.ordenG = curva.orden(puntoGenerador)
        self.llavePrivada = self._llavePriv()
        self.puntoPrivado = self._puntoAleatorio()
        self.llavesPublicas = self._llavesPublicas()
        self.llavesPublicasOtra = self._llavesPublicasOtra()
        self.tabla = self._tabla()

    def _llavePriv(self):
        """
        Genera la llave privada de la entidad.
        Numero aleatorio entre 1 y el orden del punto generador.
        """
        return randint(1, self.ordenG)

    def _puntoAleatorio(self):
        """
        Genera un punto aleatorio en la curva elíptica.
        """
        puntos = self.curva.puntos()
        return puntos[randint(0, len(puntos)-1)]

    def __str__(self):
        return f'Entidad: {self.nombre}\n' \
            f'Mensaje: {self.mensaje}\n' \
            f'Llave privada: {self.llavePrivada}\n' \
            f'Punto privado: {self.puntoPrivado}\n' \
            f'Llaves públicas: {self.llavesPublicas}\n' \
            f'Llaves públicas otra entidad: {self.llavesPublicasOtra}\n' \
            f'Tabla: {self.tabla}\n'

    def cifrar(self, llavesPublicas):
        """
        Cifra self.mensaje a parejas de puntos que son de la curva elíptica.
        """
        cifrado = []
        for letra in self.mensaje:
            cifrado.append(self._cifrar(letra, llavesPublicas))
        return cifrado

    def _cifrar(self, letra, llavesPublicas):
        """
        Cifra una letra a una pareja de puntos que son de la curva elíptica.
        """
        k = randint(1, self.ordenG)
        return (k * self.puntoGenerador, k * llavesPublicas[letra])

    def desciifrar(self, cifrado):
        """
        Descifra un conjunto de parejas de puntos (e1, e2) de una curva elíptica a un texto.
        """
        return ''.join([self._descifrar(e1, e2) for e1, e2 in cifrado])

    def _descifrar(self, e1: Punto, e2: Punto):
        """
        Descifra una pareja de puntos (e1, e2) de una curva elíptica a una letra.
        """
        return chr(e2 - self.llavePrivada * e1.x)

    def _llavesPublicas(self):
        """
        Genera las llaves públicas de la entidad.
        """
        return {letra: self.llavePrivada * self.puntoGenerador + ord(letra) * self.puntoPrivado for letra in self.mensaje}

    def recibeLlavesPublicas(self, llavesPublicas):
        """
        Recibe las llaves públicas de otra entidad y las mezcla con su llave privada para poder cifrar mensajes con la otra entidad.
        """
        self.llavesPublicasOtra = {
            letra: self.llavePrivada * llavesPublicas[letra] for letra in self.mensaje}

    def llavesFinales(self):
        """
        Genera todas las llaves públicas de esta entidad P_k1, P_k2 y P_ke donde P_ke es la combinación de la llave privada de esta entidad con la llave pública de la otra entidad P_k2.
        """
        return {letra: self.llavesPublicas[letra] + self.llavesPublicasOtra[letra] for letra in self.mensaje}
