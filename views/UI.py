import pygame
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import estructuras1.views.colores as colores

class Boton:
    def __init__(self, x, y, ancho, altura, texto, color, color_texto= colores.NEGRO, tamaño_fuente=18, id=None):
        self.rectangulo = pygame.Rect(x, y, ancho, altura)
        self.color = color
        self.texto = texto
        self.color_texto = color_texto
        #Recibe tipo de letra y tamaño
        self.fuente = pygame.font.SysFont(None, tamaño_fuente)
        self.id = id  # Identificador único opcional
        
    def dibujar(self, superficie):
        #Dibuja el rectangulo
        pygame.draw.rect(superficie, self.color, self.rectangulo)
        pygame.draw.rect(superficie, colores.NEGRO, self.rectangulo, 2)  # Borde
        
        superficie_texto = self.fuente.render(self.texto, True, self.color_texto)
        rectangulo_texto = superficie_texto.get_rect(center=self.rectangulo.center)
        superficie.blit(superficie_texto, rectangulo_texto)
        
    def es_presionado(self, posicion):
        #Verifica que las coordenadas de la posicion se encuentren dentro del rectangulo
        return self.rectangulo.collidepoint(posicion)

class Seccion:
    def __init__(self, x, y, ancho, altura, titulo="", color_titulo=colores.NEGRO, id=None):
        #Define la seccion del rectangulo pero no lo dibuja
        self.rectangulo = pygame.Rect(x, y, ancho, altura)
        self.color_fondo = colores.AZUL_OSCURO
        self.color_borde = colores.CELESTE
        self.titulo = titulo
        self.color_titulo = color_titulo
        self.fuente = pygame.font.SysFont(None, 24)
        self.id = id
        
    def dibujar(self, superficie):
        pygame.draw.rect(superficie, self.color_fondo, self.rectangulo)
        pygame.draw.rect(superficie, self.color_borde, self.rectangulo, 2)  # Borde
        
        if self.titulo:
            superficie_texto = self.fuente.render(self.titulo, True, self.color_titulo)
            rectangulo_texto = superficie_texto.get_rect(center=(self.rectangulo.centerx, self.rectangulo.y + 20))
            superficie.blit(superficie_texto, rectangulo_texto)


def crear_diseño():
    # Definir dimensiones de las secciones
    secciones = []
    botones = []
    
    # Info árbol actual
    info_arbol_actual = Seccion(10, 10, 150, 250, "Info árbol actual", colores.BLANCO)
    secciones.append(info_arbol_actual)
    
    # Carrusel de árboles
    carrusel = Seccion(170, 10, 280, 250, "Carrusel de árboles", colores.BLANCO)
    secciones.append(carrusel)
    
    # Mejor plano
    mejor_plano = Seccion(462, 10, 425, 450, "Visualizacion del plano", colores.BLANCO)
    secciones.append(mejor_plano)

    # Control de navegación
    control_navegacion = Seccion(60, 270, 330, 80, "Cambiar árbol actual", colores.NEGRO)
    control_navegacion.color_fondo = colores.BLANCO
    secciones.append(control_navegacion)
    
    # Flecha izquierda
    flecha_izquierda = Boton(70, 305, 50, 30, "←", colores.BLANCO, id="flecha_izquierda")
    botones.append(flecha_izquierda)
    
    # Flecha derecha
    flecha_derecha = Boton(330, 305, 50, 30, "→", colores.BLANCO, id="flecha_derecha")
    botones.append(flecha_derecha)

    # Colocar número de puntero
    puntero_arbol = Seccion(150, 305, 150, 40, "Puntero", colores.BLANCO)
    puntero_arbol.color_fondo = colores.BLANCO
    secciones.append(puntero_arbol)
    
    # Info mejor árbol
    info_mejor_arbol = Seccion(10, 360, 150, 230, "Info mejor árbol", colores.BLANCO)
    secciones.append(info_mejor_arbol)
   
    # Mejor árbol
    mejor_arbol = Seccion(170, 360, 280, 230, "Mejor árbol", colores.BLANCO)
    secciones.append(mejor_arbol)

    # Configuración actual
    config_actual = Seccion(462, 470, 425, 120, "Configuracion actual", colores.NEGRO)
    config_actual.color_fondo = colores.BLANCO
    secciones.append(config_actual)
    
    # Cargar JSON
    cargar_json = Boton(925, 495, 110, 40, "Cargar JSON", colores.BLANCO, id="cargar_json")
    botones.append(cargar_json)

    # Personallizar
    personalizar = Boton(1027, 495, 110, 40, "Personalizar", colores.BLANCO, id="Personalizar")
    botones.append(personalizar)
    
    # Panel de opciones
    panel_opciones = Seccion(900, 10, 280, 579, "", colores.BLANCO)
    secciones.append(panel_opciones)
    
    # Botones de opciones
    botones_opciones = [
        Boton(925,20, 240, 40, "-Mostrar Plano Optimo", colores.GRIS_CLARO, id="-Mostrar Plano Optimo"),
        Boton(925,70, 240, 40, "-Mostrar Plano Carrusel", colores.GRIS_CLARO, id="-Mostrar Plano Carrusel"),
        Boton(925,280, 240, 40, "-Mostrar Plano Personalizado", colores.GRIS_CLARO, id="-Mostrar Plano Personalizado"),
        Boton(925,120, 240, 40, "-Instrucciones", colores.NARANJA, id="instrucciones"),
        Boton(925,330, 240, 40, "-Añadir elementos", colores.CELESTE, id="anadir"),
        Boton(925,380, 240, 40, "-Color fondo seccion", colores.MORADO, id= "-Color fondo seccion"),
        Boton(925,430, 240, 40, "-Cambiar borde seccion", colores.MORADO, id= "-Cambiar borde seccion"),
    ]

    #Añadir los elementos de botones_opciones a botones
    botones.extend(botones_opciones)
    

    return secciones, botones
