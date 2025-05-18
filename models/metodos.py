import copy
import pygame
from estructuras1.views.planoView import Plano
import math
def distance(p1, p2):
    """Calcula la distancia entre dos puntos"""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def permutar(lista, matriz, s_actual):
    if len(s_actual) == len(lista):
        matriz.append(copy.deepcopy(s_actual))
    else:
        for punto in lista:
            if punto not in s_actual:
                s_actual.append(punto)
                permutar(lista, matriz, s_actual)
                s_actual.pop()

def encontrar_mejor_arbol_plano(permutaciones):
    print("Cargando, espere por favor...")
    mejor_permutacion=[]
    menor_areas=float('inf')
    indice=0
   
    plano_rect = pygame.Rect(500, 70, 360, 360)
    
    for perm in permutaciones:
        
        #Limpiar el arbol
        plano=Plano()
        plano.cargar_datos_ejemplo(perm)
         # Generar los puntos
        anchura = plano.arbol.recorrido_anchura()

        # Asignar los puntos al plano
        plano.puntos = plano.generar_puntos(anchura)

        if not plano.puntos:
            return
        # Encontrar límites de los puntos para ajustar la escala
        x_max = max(p.x for p in plano.puntos)
        y_max = max(p.y for p in plano.puntos)
        maximo = max(x_max, y_max) +1
        espaciado= plano_rect.width // maximo

        plano.rectas, plano.areas = plano.generar_rectas_areas(plano.puntos, plano_rect, espaciado)
        if len(plano.areas) < menor_areas:
            indice = permutaciones.index(perm)
            mejor_permutacion=perm
            menor_areas=len(plano.areas)
    return mejor_permutacion, indice

def encontrar_limites(puntos, punto_seleccionado, espaciado):
    plano_rect = pygame.Rect(500, 70, 360, 360)
    
    x_menor = plano_rect.x 
    #Se suma el espaciado para que llegue hasta el borde
    x_mayor = plano_rect.x + plano_rect.width
    y_menor = plano_rect.y 
    y_mayor = plano_rect.y + plano_rect.height 
    
    if punto_seleccionado.alineacion == 0:
        return x_menor, x_mayor, 0, y_menor, y_mayor
    else:
        return x_menor, x_mayor, 1 , y_menor, y_mayor          

def puntos_a_pixel(puntos,espaciado):
    plano_rect = pygame.Rect(500, 70, 360, 360)
    puntos_pixel=[]
    for punto in puntos:
        puntos_pixel.append((plano_rect.x + punto.x * espaciado, plano_rect.y + punto.y * espaciado))
    return puntos_pixel

def distance(p1, p2):
    """Calcula la distancia entre dos puntos"""
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        
def detectar_seccion( plano, pos):
        """Detecta qué sección fue clicada y la establece como activa"""
        for seccion in plano.areas:
            if seccion.rectangulo.collidepoint(pos):
                return seccion
        return None

def crear_cuadro_texto(texto, fuente=None, color_texto=None, color_fondo=None, padding=5):
    # Usar fuente predeterminada si no se especifica
    if fuente is None:
        fuente = pygame.font.Font(None, 24)
    
    # Colores predeterminados
    if color_texto is None:
        color_texto = (255, 255, 255)  # Blanco
    if color_fondo is None:
        color_fondo = (50, 50, 50)  # Gris oscuro

    # Renderizar el texto
    superficie_texto = fuente.render(texto, True, color_texto)
    
    # Crear superficie para el cuadro de texto con un poco de padding
    ancho = superficie_texto.get_width() + 2 * padding
    alto = superficie_texto.get_height() + 2 * padding
    superficie_cuadro = pygame.Surface((ancho, alto))
    
    # Dibujar el fondo del cuadro
    superficie_cuadro.fill(color_fondo)
    
    # Dibujar un borde
    pygame.draw.rect(superficie_cuadro, (100, 100, 100), superficie_cuadro.get_rect(), 2)
    
    # Colocar el texto en el centro del cuadro
    rect_texto = superficie_texto.get_rect(center=(ancho//2, alto//2))
    superficie_cuadro.blit(superficie_texto, rect_texto)
    
    return superficie_cuadro

def dibujar_textos(cuadros, pantalla):
    for cuadro in cuadros:
     # Dibujar el cuadro de texto
       pantalla.blit(cuadro[0], (cuadro[1], cuadro[2]))