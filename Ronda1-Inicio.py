import pygame
import sys
import os
import random


pygame.init()

RUTA_ARCHIVO_FONDO = "fondo.jpg" 
RUTA_ARCHIVO_UAIBOT =  "UAIBOT.png"
RUTA_ARCHIVO_AUTO= "auto.png"
RUTA_IMG_PAQUETE = "imgPaquete.png"
RUTA_INTRO = "imgIntro.jpg"
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_ROJO = (200, 0, 0)
COLOR_AZUL = (0, 0, 200)
COLOR_VERDE = (0, 200, 0)
COLOR_INSTRUCCION_FONDO = (50, 50, 50)
PANTALLA_ANCHO = 1280
PANTALLA_ALTO = 720
PISO_POS_Y = 450
clock = pygame.time.Clock()
FPS = 60


  
# Tiempo
TIEMPO_MAX = 60 #segundos
tiempo_restante = TIEMPO_MAX
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

# Dificultad
dificultad = 1  # 1: fácil, 2: media, 3: difícil
auto_vel_x = 8
autos = []


pantalla = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
pygame.display.set_caption("OFIRCA 2025 - Ronda 1 Inicio")
imgPerdiste = pygame.image.load("imgPerdiste.png")


#VARIABLES FUERZA DE SALTO, VELOCIDAD DE FONDO Y GRAVEDAD
velocidad_y = 0
gravedad = 1
salto_fuerza = 25
fondo_x = 0 
fondo_velocidad = 2  
en_suelo = True 
victoria = False
game_over = False


# Kilómetros
KM_TOTAL = 1.0
km_restantes = KM_TOTAL
km_por_segundo = 0.03


#IMAGENES
if os.path.exists(RUTA_INTRO):
    img_intro = pygame.image.load(RUTA_INTRO)
    img_intro = pygame.transform.scale(img_intro, (PANTALLA_ANCHO, PANTALLA_ALTO))

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
font_timer = pygame.font.SysFont(None, 50)

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
saltarIntro = False
intro_mostrada = False



# Crear auto
def crear_auto():
    y = PISO_POS_Y - 80
    x = PANTALLA_ANCHO + random.randint(0, 500)
    return pygame.Rect(x, y, 80, 80)

autos = [crear_auto()]

#FUNCION PARA REINICIAR EL JUEGO

def reiniciar_juego():
    global robot_y, velocidad_y, en_suelo, game_over, victoria, tiempo_restante, km_restantes, autos
    robot_y = PISO_POS_Y - robot_tamaño
    velocidad_y = 0
    en_suelo = True
    game_over = False
    victoria = False
    tiempo_restante = TIEMPO_MAX
    km_restantes = KM_TOTAL
    autos = [crear_auto()]

reiniciar_juego()



# === INTRO ===
while not saltarIntro:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                saltarIntro = True
    
    pantalla.blit(img_intro, (0, 0))
    pygame.display.flip()
    clock.tick(FPS)


# ======== BUCLE PRINCIPAL ========
while juegoEnEjecucion:
    clock.tick(FPS)
    
    keys = pygame.key.get_pressed()


        # ======== EVENTOS ========
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juegoEnEjecucion = False

            if event.type == timer_event and not game_over and not victoria:
                tiempo_restante -= 1
                km_restantes = max(0, km_restantes - km_por_segundo)
                if tiempo_restante <= 0:
                    game_over = True
                if km_restantes <= 0:
                    victoria = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciar_juego()
                elif event.key == pygame.K_1:
                    dificultad = 1
                    auto_vel_x = 8
                elif event.key == pygame.K_2:
                    dificultad = 2
                    auto_vel_x = 12
                elif event.key == pygame.K_3:
                    dificultad = 3
                    auto_vel_x = 15
                    

    if not game_over:
            # Actualizar fondo
            fondo_x -= fondo_velocidad
            if fondo_x <= -PANTALLA_ANCHO:
                fondo_x = 0

            pantalla.blit(img_fondo, (fondo_x, 0))
            pantalla.blit(img_fondo, (fondo_x + PANTALLA_ANCHO, 0))
            
            for auto in autos:
                pantalla.blit(imgAUTO, auto)
            # Barra de tiempo
            pygame.draw.rect(pantalla, COLOR_ROJO, (20, 20, 300, 30))  
            barra_ancho = max(0, int((tiempo_restante / TIEMPO_MAX) * 300))
            pygame.draw.rect(pantalla, COLOR_VERDE, (20, 20, barra_ancho, 30))
            # Texto tiempo
            tiempo_texto = font_timer.render(f"Tiempo: {tiempo_restante}", True, COLOR_BLANCO)
            pantalla.blit(tiempo_texto, (340, 15))
            # Kilómetros restantes
            km_texto = font_timer.render(f"Km restantes: {km_restantes:.2f}", True, COLOR_BLANCO)
            pantalla.blit(km_texto, (20, 60))
        


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
                
            
    if not game_over and not victoria:
            # Mover autos
            for auto in autos:
                auto.x -= auto_vel_x
                if auto.x < -auto.width:
                    auto.x = PANTALLA_ANCHO + random.randint(0, 500)
            
            # Dificultad: más autos
            if dificultad >= 2 and len(autos) < 2:
                autos.append(crear_auto())
            if dificultad == 3 and len(autos) < 3:
                autos.append(crear_auto())


            # Colisión
            robot_rect = pygame.Rect(robot_x, robot_y, robot_tamaño, robot_tamaño)
            for auto in autos:
                if robot_rect.colliderect(auto):
                    game_over = True
            
            
        # ======== DIBUJO ========
    if not game_over and not victoria:
            # Robot
            pantalla.blit(imgUAIBOT, (robot_x, robot_y))
            # Autos
            for auto in autos:
                pantalla.blit(imgAUTO, auto)
            # Barra de tiempo
            pygame.draw.rect(pantalla, COLOR_ROJO, (20, 20, 300, 30))  
            barra_ancho = max(0, int((tiempo_restante / TIEMPO_MAX) * 300))
            pygame.draw.rect(pantalla, COLOR_VERDE, (20, 20, barra_ancho, 30))
            # Texto tiempo
            tiempo_texto = font_timer.render(f"Tiempo: {tiempo_restante}", True, COLOR_BLANCO)
            pantalla.blit(tiempo_texto, (340, 15))
            # Kilómetros restantes
            km_texto = font_timer.render(f"Km restantes: {km_restantes:.2f}", True, COLOR_BLANCO)
            pantalla.blit(km_texto, (20, 60))
    elif game_over:
            if imgPerdiste:
                pantalla.blit(imgPerdiste, (0, 0))
            pantalla.blit(txtGameOver, txtGameOver.get_rect(center=(PANTALLA_ANCHO // 2, 460 )))
    elif victoria:
            pantalla.blit(imgPaquete, (0,0))
            #frenar fondo
            fondo_velocidad = 0

    pygame.display.flip()
pygame.quit()
sys.exit()
