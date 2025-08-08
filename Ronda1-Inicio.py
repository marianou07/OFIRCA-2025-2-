import pygame
import sys
import os



pygame.init()

RUTA_ARCHIVO_FONDO = "fondo.jpeg" 
RUTA_ARCHIVO_UAIBOT =  "UAIBOT.png"
RUTA_ARCHIVO_AUTO= "auto.png"
RUTA_IMG_PAQUETE = "imgPaquete.png"
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (200, 0, 0)
COLOR_AZUL = (0, 0, 200)
COLOR_VERDE = (0, 200, 0)
COLOR_INSTRUCCION_FONDO = (50, 50, 50)
PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720
PISO_POS_Y = 450
temporizador = pygame.time.Clock()
FPS = 60
ultimo_tiempo_segundo = 0
ultimoKm = -1
InicioTemp=pygame.time.get_ticks()
    
pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("OFIRCA 2025 - Ronda 1 Inicio")
imgPerdiste = pygame.image.load("imgPerdiste.png")


#VARIABLES FUERZA DE SALTO, VELOCIDAD DE FONDO Y GRAVEDAD
velocidad_y = 0
gravedad = 1
salto_fuerza = 25
fondo_x = 0 
fondo_velocidad = 2  


#IMAGENES
if os.path.exists(RUTA_ARCHIVO_FONDO):
    img_fondo = pygame.image.load(RUTA_ARCHIVO_FONDO)
    img_fondo = pygame.transform.scale(img_fondo, (PANTALLA_ANCHO, PANTALLA_ALTO))

if os.path.exists(RUTA_ARCHIVO_UAIBOT):
    imgUAIBOT = pygame.image.load(RUTA_ARCHIVO_UAIBOT)
    imgUAIBOT = pygame.transform.scale(imgUAIBOT, (150, 150))  

if os.path.exists(RUTA_IMG_PAQUETE):
    imgPaquete = pygame.image.load(RUTA_IMG_PAQUETE)
    imgPaquete = pygame.transform.scale(imgPaquete, (PANTALLA_ANCHO, PANTALLA_ALTO))
    
if os.path.exists(RUTA_ARCHIVO_AUTO):
    imgAUTO = pygame.image.load(RUTA_ARCHIVO_AUTO)
    imgAUTO = pygame.transform.scale(imgAUTO, (200, 80)) 

# Carga y escalado de la imagen de "perdiste"
if os.path.exists("imgPerdiste.png"):
    imgPerdiste = pygame.image.load("imgPerdiste.png")
    imgPerdiste = pygame.transform.scale(imgPerdiste, (PANTALLA_ANCHO, PANTALLA_ALTO))
else:
    imgPerdiste = None  # Para prevenir errores si no existe

#TEXTOS
font_TxtInstrucciones = pygame.font.SysFont(None, 36)
txtInstrucciones = font_TxtInstrucciones.render("Usa la barra espaciadora para saltar", True, COLOR_BLANCO)
txtInstrucciones_desplazamiento = 10
txtInstrucciones_rect = txtInstrucciones.get_rect()
txtInstrucciones_rect.topleft = (10, 10)
fondo_rect = pygame.Rect(txtInstrucciones_rect.left - txtInstrucciones_desplazamiento,
                      txtInstrucciones_rect.top - txtInstrucciones_desplazamiento,
                      txtInstrucciones_rect.width + 2 * txtInstrucciones_desplazamiento,
                      txtInstrucciones_rect.height + 2 * txtInstrucciones_desplazamiento)

font_TxtGameOver = pygame.font.SysFont(None, 100)
txtGameOver = font_TxtGameOver.render("JUEGO TERMINADO", True, COLOR_ROJO)
txtGameOver_rect = txtGameOver.get_rect(center=(PANTALLA_ANCHO // 2, (PANTALLA_ALTO // 2)-200))


#VARIABLES TAMAÑOS
robot_tamaño = 150
robot_x = 100
robot_y = PISO_POS_Y - robot_tamaño

auto_ancho = 80
auto_alto = 80
auto_x = PANTALLA_ANCHO
auto_y = PISO_POS_Y - auto_alto
auto_vel_x = 10

#VARIABLES DE JUEGO ACTIVO/ROBOT EN EL PISO
juegoEnEjecucion = True
game_over = False
en_suelo = True

#VARIABLE DE KILOMETRAJE
km = 0


#FUNCION PARA REINICIAR EL JUEGO

def reiniciar_juego():
    global robot_x, robot_y, velocidad_y, en_suelo, auto_x, game_over, fondo_x, km
    robot_x = 100
    robot_y = PISO_POS_Y - robot_tamaño
    velocidad_y = 0
    en_suelo = True
    auto_x = PANTALLA_ANCHO
    fondo_x = 0
    km = 0 
    game_over = False



while juegoEnEjecucion:
    temporizador.tick(FPS)

    # EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juegoEnEjecucion = False
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reiniciar_juego()

    keys = pygame.key.get_pressed()

    if not game_over:
        # Actualizar fondo
        fondo_x -= fondo_velocidad
        if fondo_x <= -PANTALLA_ANCHO:
            fondo_x = 0

        pantalla.blit(img_fondo, (fondo_x, 0))
        pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, 0))

        # Actualizar kilometraje
        tiempoActual = (pygame.time.get_ticks() - InicioTemp) // 1000
        if tiempoActual > ultimo_tiempo_segundo:
            km += 0.03
            ultimo_tiempo_segundo = tiempoActual
            km = round(km, 2)

        # Movimiento del auto
        auto_x -= auto_vel_x
        if auto_x < -auto_ancho:
            auto_x = PANTALLA_ANCHO

        # Salto
        if keys[pygame.K_SPACE] and en_suelo:
            velocidad_y = -salto_fuerza
            en_suelo = False

        # Gravedad
        velocidad_y += gravedad
        robot_y += velocidad_y

        if robot_y >= PISO_POS_Y - robot_tamaño:
            robot_y = PISO_POS_Y - robot_tamaño
            velocidad_y = 0
            en_suelo = True

        # Colisiones
        robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
        auto_rect = pygame.Rect(auto_x, auto_y, auto_ancho, auto_alto)

        if robot_rect.colliderect(auto_rect):
            game_over = True
        
        
        if int(km) > ultimoKm:
            ultimoKm = int(km)
            pantalla.blit(imgPaquete,(0,0))
            
    # DIBUJAR ELEMENTOS
    pantalla.blit(imgUAIBOT, (robot_x, robot_y))
    pantalla.blit(imgAUTO, (auto_x, auto_y))

    pygame.draw.rect(pantalla, COLOR_INSTRUCCION_FONDO, fondo_rect)
    pantalla.blit(txtInstrucciones, txtInstrucciones_rect)
    txtKm = font_TxtInstrucciones.render(f"KM: {km:.2f}", True, COLOR_BLANCO)
    pantalla.blit(txtKm, (PANTALLA_ANCHO - 200, 10))

    if game_over:
        if imgPerdiste:
            pantalla.blit(imgPerdiste, (0, 0))
        pantalla.blit(txtGameOver, txtGameOver_rect)

    pygame.display.flip()




pygame.quit()
sys.exit()
