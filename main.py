import pygame
from random import randint

# CONSTANTES

ANCHO = 250
ALTO = 450

HITBOX = ALTO / 5


# CLASES


class Tecla:
    def __init__(self, y=-500):
        self.ancho = ANCHO / 4
        self.alto = ALTO / 5

        self.rel = randint(0, 3)
        self.x = self.rel * self.ancho + 1
        self.y = y

    def dibujar(self):
        pygame.draw.rect(ventana, (0, 0, 0), (self.x, self.y, self.ancho, self.alto))


class Boton:
    def __init__(self, x, y, ancho, alto, color, tipo):
        self.x = x
        self.y = y

        self.ancho = ancho
        self.alto = alto
        self.color = color
        self.tipo = tipo
        self.dentro = self.dentro()

    def dentro(self):
        x = round((self.ancho - self.tipo.get_size()[0]) / 2) + self.x
        y = round((self.alto - self.tipo.get_size()[1]) / 2) + self.y
        return x, y

    def clicked(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.ancho:
            if self.y <= y <= self.y + self.alto:
                return True

    def dibujar(self):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.alto))
        ventana.blit(self.tipo, self.dentro)


# FUNCIONES


def mover(teclas, vel):
    for t in teclas:
        t.y += vel


def render(teclas):
    ventana.fill((255, 255, 255))

    # lineas
    lin1 = ANCHO / 4
    lin2 = ANCHO / 2
    lin3 = ANCHO * 0.75

    pygame.draw.line(ventana, (0, 0, 0), (lin1, 0), (lin1, ALTO))
    pygame.draw.line(ventana, (0, 0, 0), (lin2, 0), (lin2, ALTO))
    pygame.draw.line(ventana, (0, 0, 0), (lin3, 0), (lin3, ALTO))

    # teclas
    for t in teclas:
        t.dibujar()

    # Puntuación
    puntos = fuente.render(str(contador), 1, (255, 0, 0))
    ventana.blit(puntos, (ANCHO // 2, 10))


def reset():
    pygame.time.delay(2000)
    teclas = [Tecla()]
    return teclas, 0


# MAIN SCRIPT


def main():
    global ventana, contador, fuente

    # INICIALIZACIÓN
    pygame.init()

    # Ventana
    pygame.display.set_caption('Piano plagio')
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    clock = pygame.time.Clock()

    # MENU ======================================================================================

    # Variables
    opcion = ['Fácil', 'Normal', 'Difícil', 'Clásico']
    elegido = 3
    fuente = pygame.font.SysFont(None, 40)

    alto_cartel = 150

    izq_b = fuente.render('<', 1, (255, 255, 255))
    izq = Boton(10, alto_cartel - 10, 40, 40, (0, 255, 0), izq_b)
    der_b = fuente.render('>', 1, (255, 255, 255))
    der = Boton(ANCHO - 50, alto_cartel - 10, 40, 40, (0, 255, 0), der_b)
    start_b = fuente.render('COMENZAR', 1, (255, 255, 255))
    start = Boton(30, ALTO // 2, ANCHO - 60, 50, (0, 255, 0), start_b)

    titulo = fuente.render('PIANO PLAGIO :V', 1, (0, 0, 0))

    _vel = 5

    menu = True
    run = False

    while menu:

        # Detectar cierre de aplicación
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                comandos = [izq.clicked(pos), der.clicked(pos), start.clicked(pos)]

                if comandos != [0, 0, 0]:
                    if comandos[0]:
                        if elegido > 0:
                            elegido -= 1
                        else:
                            elegido = 3
                    elif comandos[1]:
                        if elegido < 3:
                            elegido += 1
                        else:
                            elegido = 0
                    elif comandos[2]:
                        menu = False
                        run = True
                        _vel = [5, 8, 12, 0]
                        _vel = _vel[elegido]

        # RENDER
        ventana.fill((255, 255, 255))
        ventana.blit(titulo, (ANCHO // 2 - titulo.get_size()[0] // 2, 30))

        # Seleccion de modo
        cartelito = fuente.render(opcion[elegido], 1, (0, 0, 0))
        ventana.blit(cartelito, (ANCHO // 2 - cartelito.get_size()[0] // 2, alto_cartel))

        izq.dibujar()
        der.dibujar()
        start.dibujar()

        pygame.display.update()

    # Variables
    teclas = [Tecla()]
    contador = 0
    fuente = pygame.font.SysFont(None, 45)
    vel = _vel
    reloj = 0

    # MAINLOOP =======================================================

    while run:

        # Detectar cierre de aplicación
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Acción con tecla
            if event.type == pygame.KEYDOWN:
                botones = pygame.key.get_pressed()
                botones = [botones[pygame.K_v], botones[pygame.K_b], botones[pygame.K_n], botones[pygame.K_m]]

                if teclas != [0, 0, 0, 0]:
                    if botones[teclas[0].rel]:
                        del teclas[0]
                        contador += 1
                    else:
                        teclas, contador = reset()
                        reloj = 0

            # Acción con mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if pygame.mouse.get_pos()[0] // (ANCHO / 4) == teclas[0].rel:
                    del teclas[0]
                    contador += 1
                else:
                    teclas, contador = reset()
                    reloj = 0

        # Actualizar teclas
        if not len(teclas):
            teclas.append(Tecla(-175))
        elif teclas[-1].y > 0:
            teclas.append(Tecla(randint(1, 2) * -ALTO // 5 + 10))

        if teclas[0].y + HITBOX > ALTO:
            teclas, contador = reset()
            reloj = 0

        # Velocidad
        if not _vel:
            #print(reloj)
            reloj += 1
            vel = reloj // 1000 + 4

        # UPDATE
        mover(teclas, vel)
        render(teclas)
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
