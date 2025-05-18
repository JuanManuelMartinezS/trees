import pygame
import sys
import os
# Importar la clase ArbolBinarioProyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from estructuras1.models.arbol import ArbolBinarioProyecto  # Uso de la clase ArbolBinarioProyecto
import estructuras1.views.colores as colores

class VisualizadorArbol:
    def __init__(self, tamaño_fuente=18):
        self.ancho, self.alto = 1200, 600
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        # Estado actual
        self.arbol = ArbolBinarioProyecto()
        self.puntos = []
        self.radio_nodo = 17
        self.fuente = pygame.font.SysFont(None, tamaño_fuente)
        self.fuente_nodo = pygame.font.SysFont(None, 17)
        self.fuente_pequena = pygame.font.SysFont(None, 16)

    def cargar_datos_ejemplo(self, puntos):
        self.arbol = ArbolBinarioProyecto()
        self.puntos = puntos
        for punto in self.puntos:
            self.arbol.insertar(punto)
    
    def dibujar_plano(self):
        # Dibujar el fondo del plano
        plano_rect = pygame.Rect(500, 70, 360, 360)
        pygame.draw.rect(self.screen, colores.AZUL_OSCURO, plano_rect)
        pygame.draw.rect(self.screen, colores.CELESTE, plano_rect, 2)


        if not self.puntos:
            return
        # Encontrar límites de los puntos para ajustar la escala
        x_max = max(p[0] for p in self.puntos)
        y_max = max(p[1] for p in self.puntos)
        maximo = max(x_max, y_max) +1

        espaciado= plano_rect.width // maximo

        # For que empieza en la parte izquierda del cuadrado (saltando una columna) hasta la parte derecha, saltando entre cada una el espaciado definido
        for x in range(plano_rect.x + espaciado, plano_rect.right, espaciado):
            #Crea una linea desde la parte de arriba (rect.y) hasta la de abajo (rect.bottom)

            #Pantalla, color, punto inicio, punto final, grosor
            pygame.draw.line(self.screen, (30, 40, 50), (x, plano_rect.y), (x, plano_rect.bottom), 1)

        # For que empieza en la parte de arriba del cuadrado (saltando una fila) hasta la parte de abajo, saltando entre cada una el espaciado definido
        for y in range(plano_rect.y + espaciado, plano_rect.bottom, espaciado):
            #Crea una linea desde la parte izquierda (rect.x) hasta la de la derecha (rect.rigth)
            pygame.draw.line(self.screen, (30, 40, 50), (plano_rect.x, y), (plano_rect.right, y), 1)


        # Dibujar marcas y etiquetas de medidas (fuente más pequeña)
        fuente_unidades = pygame.font.Font(None, 12)  # Fuente más pequeña

        for i in range(maximo+1):
            x_pos = plano_rect.x + i * (espaciado)
            pygame.draw.line(self.screen, colores.BLANCO, (x_pos, plano_rect.y - 5), (x_pos, plano_rect.y + 5), 2)
            unidad = i
            texto_medida = fuente_unidades.render(f"{unidad}u", True, colores.BLANCO)
            self.screen.blit(texto_medida, (x_pos - 6, plano_rect.y - 20))  # Ajuste de posición

        for i in range(maximo+1):
            y_pos = plano_rect.y + i * (espaciado)
            pygame.draw.line(self.screen, colores.BLANCO, (plano_rect.x - 5, y_pos), (plano_rect.x + 5, y_pos), 2)
            unidad = i
            texto_medida = fuente_unidades.render(f"{unidad}u", True, colores.BLANCO)
            self.screen.blit(texto_medida, (plano_rect.x - 20, y_pos - 6))  # Ajuste de posición


        for punto in self.puntos:
            # Convertir coordenadas a posición en pantalla (relativas al plano)
            px = int(punto[0]*espaciado + plano_rect.x)
            py = int(punto[1]*espaciado + plano_rect.y)
            # Dibujar el punto
            pygame.draw.circle(self.screen, colores.VERDE_AGUA, (px, py), 4)

    def dibujar_nodo(self, superficie, nodo, x, y, ancho_disponible, desplazamiento_y, nivel, color_nodo=colores.VERDE_AGUA, color_texto=colores.NEGRO):
        # Dibujar el nodo (círculo)
        pygame.draw.circle(superficie, color_nodo, (x, y), self.radio_nodo)
        pygame.draw.circle(superficie, colores.NEGRO, (x, y), self.radio_nodo, 2)  # Borde del nodo
        
        # Dibujar el valor del nodo
        if hasattr(nodo, 'valor'):
            # Para nodos con un solo valor
            texto = f"({nodo.valor[0]},{nodo.valor[1]})"
        else:
            texto = "?"
            
        superficie_texto = self.fuente_nodo.render(texto, True, color_texto)
        rectangulo_texto = superficie_texto.get_rect(center=(x, y))
        superficie.blit(superficie_texto, rectangulo_texto)
        
        # Calcular espaciado para el siguiente nivel
        nuevo_ancho = ancho_disponible / 2
        
        # Dibujar líneas y subárboles recursivamente
        if nodo.izquierda:
            x_izq = x - nuevo_ancho
            y_izq = y + desplazamiento_y
            #Superficie, color, punto inicio, punto final, grosor 
            pygame.draw.line(superficie, colores.BLANCO, (x, y + self.radio_nodo), (x_izq, y_izq - self.radio_nodo), 2)
            self.dibujar_nodo(superficie, nodo.izquierda, x_izq, y_izq, nuevo_ancho, desplazamiento_y, nivel + 1)
            
        if nodo.derecha:
            x_der = x + nuevo_ancho
            y_der = y + desplazamiento_y
            pygame.draw.line(superficie, colores.BLANCO, (x, y + self.radio_nodo), (x_der, y_der - self.radio_nodo), 2)
            self.dibujar_nodo(superficie, nodo.derecha, x_der, y_der, nuevo_ancho, desplazamiento_y, nivel + 1)
    
    def dibujar_arbol(self, superficie, seccion, arbol=None):
        """Dibuja el árbol en la sección especificada"""
        if arbol is None:
            arbol = self.arbol
            
        if arbol.raiz is None:
            # Mostrar mensaje de árbol vacío
            fuente = pygame.font.SysFont(None, 24)
            texto = fuente.render("Árbol vacío", True, colores.BLANCO)
            rect_texto = texto.get_rect(center=(seccion.rectangulo.centerx, seccion.rectangulo.centery))
            superficie.blit(texto, rect_texto)
            return
            
        # Calcular dimensiones disponibles (descontando el espacio para el título)
        ancho_disponible = seccion.rectangulo.width - 40  # Margen de 20px en cada lado
        y_inicial = seccion.rectangulo.y + 50  # Espacio para el título
        desplazamiento_y = (seccion.rectangulo.height - 20) / arbol.obtener_altura()  # Espacio vertical para cada nivel
        
        # Dibujar el árbol desde la raíz
        self.dibujar_nodo(
            superficie, 
            arbol.raiz, 
            seccion.rectangulo.centerx,  # Centrado horizontalmente
            y_inicial,  # Posición vertical inicial
            ancho_disponible / 2,  # Ancho disponible inicial para cada subárbol
            desplazamiento_y,  # Espaciado vertical
            0  # Nivel inicial
        )
        