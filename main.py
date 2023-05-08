import pygame
import csv
import constantes
from jugador import Jugador
from arma import Arma
from item import Item
from mundo import Mundo

pygame.init()

pantalla = pygame.display.set_mode(constantes.sizePantalla)

# Titulo de la pantalla
pygame.display.set_caption("Template")

# Creando el Clock
clock = pygame.time.Clock()

# Definir Variables del Juego
level = 1

# Movimento del jugador
movimientoIzquierda = False
movimientoDerecha = False
movimientoArriba = False
movimientoAbajo = False

# Fuentes del Proyecto
fuente = pygame.font.Font("recursos/fuentes/AtariClassic.ttf", 20)

# Escalar imagenes correctamente
def escalarImagen(imagen, escala):
    w = imagen.get_width()
    h = imagen.get_height()
    return pygame.transform.scale(imagen, (w * escala, h * escala))

# Cargar Imagenes de los corazones (vida del personaje)
corazonVacio = escalarImagen(pygame.image.load("recursos/imagenes/articulos/heart_empty.png").convert_alpha(), constantes.ESCALA_ARTICULOS)
corazonMitad = escalarImagen(pygame.image.load("recursos/imagenes/articulos/heart_half.png").convert_alpha(), constantes.ESCALA_ARTICULOS)
corazonCompleto = escalarImagen(pygame.image.load("recursos/imagenes/articulos/heart_full.png").convert_alpha(), constantes.ESCALA_ARTICULOS)

# Cargar monedas
imagenesMonedas = []
for x in range(4):
    img = escalarImagen(pygame.image.load(f"recursos/imagenes/articulos/coin_f{x}.png").convert_alpha(), constantes.ESCALA_ARTICULOS)
    imagenesMonedas.append(img)

# Cargar pocion
pocionRoja = escalarImagen(pygame.image.load("recursos/imagenes/articulos/potion_red.png").convert_alpha(), constantes.ESCALA_POSION)


# Cargar Armas
imagenArco = escalarImagen(pygame.image.load("recursos/imagenes/armas/bow.png").convert_alpha(), constantes.ESCALA_ARMA)
imagenFlecha = escalarImagen(pygame.image.load("recursos/imagenes/armas/arrow.png").convert_alpha(), constantes.ESCALA_ARMA)

# Cargar las casillas
listaCasilla = []
for x in range(constantes.CASILLAS_TYPE):
    casillaImage = pygame.image.load(f"recursos/imagenes/casillas/{x}.png").convert_alpha()
    casillaImage = pygame.transform.scale(casillaImage, (constantes.CASILLAS_SIZE, constantes.CASILLAS_SIZE))
    listaCasilla.append(casillaImage)

# Cargar otros personajes
mobAnimaciones = []
tiposMod = ["jugador", "imp", "esqueleto", "duende", "muddy", "zombie", "demonio"]

tipoAnimaciones = ["idle", "run"]
for mod in tiposMod:
    # Cargar Imagenes del Jugador
    animaciones_lista = []
    for animaciones in tipoAnimaciones:
        # Lista temporal para resetear lista
        listaTemp = []
        for i in range(4):
            img = pygame.image.load(f"recursos/imagenes/mob/{mod}/{animaciones}/{i}.png").convert_alpha()
            img = escalarImagen(img, constantes.ESCALA)
            listaTemp.append(img)
        animaciones_lista.append(listaTemp)
    mobAnimaciones.append(animaciones_lista)

# Funcion para Dibujar texto
def dibujarTexto(texto, font, coloTexto, x, y):
    img = fuente.render(texto, True, coloTexto)
    pantalla.blit(img, (x, y))

# Dibujar la informacion en la pantalla
def dibujarInformacion():
    # Dibujar el panel de informacion
    pygame.draw.rect(pantalla, constantes.PANEL, (0, 0, constantes.anchoPantalla, 50))
    pygame.draw.line(pantalla, constantes.BLANCO, (0, 50), (constantes.anchoPantalla, 50))
    # Dibujar vidas
    corazonesVacios = False
    for i in range(5):
        if jugador.vida >= ((i + 1) * 20):
            pantalla.blit(corazonCompleto, (10 + i * 50, 0))
        elif (jugador.vida % 20 > 0) and corazonesVacios == False:
            pantalla.blit(corazonMitad, (10 + i * 50, 0))
            corazonesVacios = True
        else:
            pantalla.blit(corazonVacio, (10 + i * 50, 0))
    # Mostrar Puntos
    dibujarTexto(f"x{jugador.puntos}", fuente, constantes.BLANCO, constantes.anchoPantalla - 100, 15)

# Crear Lista Vacia De Casillas
worldData = []

for row in range(constantes.FILAS):
    r = [-1] * constantes.COLUMNAS
    worldData.append(r)
#print(worldDatad)

mundo = Mundo()
mundo.porcesarData(worldData, listaCasilla)


def dibujarRejilla():
    for x in range(30):
        pygame.draw.line(pantalla, constantes.BLANCO, (x * constantes.CASILLAS_SIZE, 0), (x * constantes.CASILLAS_SIZE, constantes.altoPantalla))
        pygame.draw.line(pantalla, constantes.BLANCO, (0, x * constantes.CASILLAS_SIZE), (constantes.anchoPantalla, x * constantes.CASILLAS_SIZE))


# Damage Text Class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = fuente.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.contador = 0

    def update(self):
        # Mover las letras
        self.rect.y -= 1
        self.contador += 1
        if self.contador > 30:
            self.kill()


# Crear jugador
jugador = Jugador(100, 100, 75, mobAnimaciones, 0)

# Crear Enemigo
enemigo = Jugador(200, 300, 100, mobAnimaciones, 1)

# Crear Arma
arco = Arma(imagenArco, imagenFlecha)

# Crear Lista de enemigo
enemigoLista = []
enemigoLista.append(enemigo)

# Grupos de sprites
damageTextGrupo = pygame.sprite.Group()
grupoFlecha = pygame.sprite.Group()
grupoItem = pygame.sprite.Group()

scoreMonedas = Item(constantes.anchoPantalla - 115, 23, 0, imagenesMonedas)
grupoItem.add(scoreMonedas)

pocion = Item(200, 200, 1, [pocionRoja])
grupoItem.add(pocion)
monedas = Item(400, 400, 0, imagenesMonedas)
grupoItem.add(monedas)

# # Test Damage class
# damageText = DamageText(300, 400, "15", constantes.ROJO)
# damageTextGrupo.add(damageText)


# Game Loop
run = True
while run:

    # Frames
    clock.tick(constantes.FPS)

    pantalla.fill(constantes.FONDO)

    #test
    dibujarRejilla()

    # Calcular Movimento
    dx = 0
    dy = 0
    if movimientoDerecha == True:
        dx += constantes.VELOCIDAD
    if movimientoIzquierda == True:
        dx -= constantes.VELOCIDAD
    if movimientoArriba == True:
        dy -= constantes.VELOCIDAD
    if movimientoAbajo == True:
        dy += constantes.VELOCIDAD

    # Actualizar al Jugador
    jugador.actualizar()
    flecha = arco.actualizar(jugador)
    if flecha:
        grupoFlecha.add(flecha)
    for flecha in grupoFlecha:
        damage, damagePos = flecha.actualizar(enemigoLista)
        if damage:
            damageText = DamageText(damagePos.centerx, damagePos.y, str(damage), constantes.ROJO)
            damageTextGrupo.add(damageText)
    damageTextGrupo.update()
    grupoItem.update(jugador)
    print(grupoFlecha)

    # Mover el Jugador
    jugador.move(dx, dy)

    # Actualizar enemigos
    for enemigo in enemigoLista:
        enemigo.actualizar()

    print("(" + str(dx) + ", " + str(dy) + ")")
    mundo.draw(pantalla)
    # Dibujar Enemigos
    for enemigo in enemigoLista:
        enemigo.dibujar(pantalla)
    damageTextGrupo.draw(pantalla)
    grupoItem.draw(pantalla)
    dibujarInformacion()
    scoreMonedas.dibujar(pantalla)

    # Dibujar Jugador
    jugador.dibujar(pantalla)
    arco.dibujar(pantalla)
    for flecha in grupoFlecha:
        flecha.dibujar(pantalla)

    print(enemigo.vida)


    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # print("a - izquierda")
                movimientoIzquierda = True
            if event.key == pygame.K_d:
                # print("d - derecha")
                movimientoDerecha = True
            if event.key == pygame.K_w:
                # print("w - arriba")
                movimientoArriba = True
            if event.key == pygame.K_s:
                # print("s - abajo")
                movimientoAbajo = True
        # Release Teclas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                # print("a - izquierda")
                movimientoIzquierda = False
            if event.key == pygame.K_d:
                # print("d - derecha")
                movimientoDerecha = False
            if event.key == pygame.K_w:
                # print("w - arriba")
                movimientoArriba = False
            if event.key == pygame.K_s:
                # print("s - abajo")
                movimientoAbajo = False

    pygame.display.flip()