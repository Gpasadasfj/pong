import turtle  # Módulo para dibujar gráficos
import random  # Módulo para generar aleatoriedad
from abc import ABC, abstractmethod  # Módulo para definir clases abstractas


# Configurar la pantalla
class Pantalla:
    def __init__(self, jugador1, jugador2, pelota, marcador):
        self.crear_pantalla()  # Ejecutamos los métodos de inicio
        self.asignar_teclas(jugador1, jugador2)

    def crear_pantalla(self):
        self.screen = turtle.Screen()  # Inicializar la pantalla
        self.screen.listen()  # Escuchar eventos de teclado
        self.screen.setup(width=500, height=500)  # Configurar el tamaño de la pantalla
        self.screen.title("Pong")  # Configurar el título de la pantalla
        self.screen.bgcolor("black")  # Configurar el color de fondo de la pantalla

    def asignar_teclas(self, jugador1, jugador2):
        self.screen.onkey(jugador1.mover_arriba, "w")  # Asignar teclas
        self.screen.onkey(jugador1.mover_abajo, "s")
        self.screen.onkey(jugador2.mover_arriba, "Up")
        self.screen.onkey(jugador2.mover_abajo, "Down")


# Configurar el marcador
class Marcador:
    def __init__(self):
        self.puntuacion_jugador1 = 0
        self.puntuacion_jugador2 = 0
        self.marcador = turtle.Turtle()
        self.marcador.speed(0)
        self.marcador.color("white")
        self.marcador.penup()  # No dibujar al moverse
        self.marcador.hideturtle()  # No mostrar el cursor
        self.marcador.goto(0, 220)  # Posicionar el marcador
        self.actualizar_marcador()  # LLamada al método para actualizar el marcador

    # Función para actualizar el marcador
    def actualizar_marcador(self):
        self.marcador.clear()  # Limpiar el marcador anterior
        self.marcador.write(  # Escribir el nuevo marcador
            f"Jugador 1: {self.puntuacion_jugador1}  Jugador 2: {self.puntuacion_jugador2}",
            align="center",
            font=("Arial", 16, "bold"),
        )

    # Funciones para incrementar la puntuación
    def incrementar_puntuacion_jugador1(self):
        self.puntuacion_jugador1 += 1
        self.actualizar_marcador()

    def incrementar_puntuacion_jugador2(self):
        self.puntuacion_jugador2 += 1
        self.actualizar_marcador()


# Clase abstracta para los jugadores
class Jugadores(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def mover_arriba(self):
        pass

    @abstractmethod
    def mover_abajo(self):
        pass


# Clase para el jugador 1
class Jugador1(Jugadores):
    def __init__(self):
        self.t = turtle.Turtle()  # Inicializamos la barra del jugador 1
        self.t.shape("square")  # Forma de la barra
        self.t.shapesize(stretch_wid=4, stretch_len=1)  # Tamaño de la barra
        self.t.color("blue")  # Color de la barra
        self.t.speed(0)  # Velocidad instantánea
        self.t.penup()  # No dibujar mientras se mueve
        self.t.goto(-240, 0)  # Posición inicial de la barra

    def mover_arriba(self):
        y = self.t.ycor()
        if y < 208:
            self.t.sety(y + 20)  # Mover 20 pasos hacia arriba

    def mover_abajo(self):
        y = self.t.ycor()
        if y > -200:
            self.t.sety(y - 20)  # Mover 20 pasos hacia abajo


# Clase para el jugador 2
class Jugador2(Jugadores):
    def __init__(self):
        self.t = turtle.Turtle()  # Inicializamos la barra del jugador 2
        self.t.shape("square")  # Forma de la barra
        self.t.shapesize(stretch_wid=4, stretch_len=1)  # Tamaño de la barra
        self.t.color("green")  # Color de la barra
        self.t.speed(0)  # Velocidad instantánea
        self.t.penup()  # No dibujar mientras se mueve
        self.t.goto(240, 0)  # Posicion incial de la barra

    def mover_arriba(self):
        y = self.t.ycor()
        if y < 208:
            self.t.sety(y + 20)  # Mover 20 pasos hacia arriba

    def mover_abajo(self):
        y = self.t.ycor()
        if y > -200:
            self.t.sety(y - 20)  # Mover 20 pasos hacia abajo


# Clase para configurar la pelota
class Pelota:
    def __init__(self, jugador1, jugador2, marcador):
        self.pelota = turtle.Turtle()
        self.pelota.shape("circle")
        self.pelota.color("red")
        self.pelota.speed(9)
        self.pelota.penup()

        self.dx = random.uniform(2, 4) * random.choice(
            [-1, 1]
        )  # Dirección aleatoria en el eje X

        self.dy = random.uniform(2, 4) * random.choice(
            [-1, 1]
        )  # Dirección aleatoria en el eje Y

        self.limite_x = 240  # Límites de la pantalla
        self.limite_y = 240
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.marcador = marcador
        self.mover_pelota()  # Iniciar el movimiento de la pelota

    # Método para mover la pelota
    def mover_pelota(self):
        if self.pelota.ycor() > self.limite_y:  # Si la pelota llega al límite superior
            self.pelota.sety(self.limite_y)  # La pelota rebota
            self.dy = -self.dy + random.uniform(
                -0.5, 0.5
            )  # Cambia la dirección en el eje Y

        if self.pelota.ycor() < -self.limite_y:  # Si la pelota llega al límite inferior
            self.pelota.sety(-self.limite_y)  # La pelota rebota
            self.dy = -self.dy + random.uniform(
                -0.5, 0.5
            )  # Cambia la dirección en el eje Y

        if self.pelota.xcor() > self.limite_x:  # Si la pelota llega al límite derecho
            self.pelota.setx(self.limite_x)  # La pelota rebota
            self.dx = -self.dx + random.uniform(
                -0.5, 0.5
            )  # Cambia la dirección en el eje X
            self.marcador.incrementar_puntuacion_jugador1()  # Incrementa la puntuación del jugador 1

        if (
            self.pelota.xcor() < -self.limite_y
        ):  # Si la pelota llega al límite izquierdo
            self.pelota.setx(-self.limite_x)  # La pelota rebota
            self.dx = -self.dx + random.uniform(
                -0.5, 0.5
            )  # Cambia la dirección en el eje X
            self.marcador.incrementar_puntuacion_jugador2()  # Incrementa la puntuación del jugador 2

        self.pelota.goto(
            self.pelota.xcor() + self.dx, self.pelota.ycor() + self.dy
        )  # Mover la pelota

        self.colisiones()  # Comprobar colisiones

        turtle.ontimer(
            self.mover_pelota, 1
        )  # Llamar al método mover_pelota cada 1 milisegundo

    def colisiones(self):
        # Colisión con el jugador 1
        if (
            self.pelota.xcor() < -220  # Si la pelota está cerca del jugador 1
            and self.jugador1.t.ycor() - 50
            < self.pelota.ycor()
            < self.jugador1.t.ycor() + 50
        ):
            self.pelota.setx(-220)  # La pelota rebota
            self.dx = -self.dx  # Cambia la dirección en el eje X

        # Colisión con el jugador 2
        if (
            self.pelota.xcor() > 220  # Si la pelota está cerca del jugador 2
            and self.jugador2.t.ycor() - 50
            < self.pelota.ycor()
            < self.jugador2.t.ycor() + 50
        ):
            self.pelota.setx(220)  # La pelota rebota
            self.dx = -self.dx  # Cambia la dirección en el eje X

        self.pelota.goto(
            self.pelota.xcor() + self.dx, self.pelota.ycor() + self.dy
        )  # Mover la pelota


jugador1 = Jugador1()
jugador2 = Jugador2()
marcador = Marcador()
pelota = Pelota(jugador1, jugador2, marcador)


screen = Pantalla(jugador1, jugador2, pelota, marcador)
turtle.mainloop()
