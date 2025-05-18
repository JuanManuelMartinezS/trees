import pygame
import sys
import os
import numpy as np
import math
# Importar la clase ArbolBinarioProyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from estructuras1.models.arbol import ArbolBinarioProyecto  # type: ignore # Uso de la clase ArbolBinarioProyecto
import estructuras1.views.colores as colores
from estructuras1.views.UI import Seccion
import estructuras1.views.colores as colores

class Punto:
    def __init__(self, x, y, alineacion, id=None):
        self.x = x
        self.y = y
        self.alineacion = alineacion  # 0: X, 1: Y
        self.id = id

class Recta:
    def __init__(self, inicio, fin, punto):
        self.inicio = inicio
        self.fin = fin
        self.punto = Punto(punto.x, punto.y, punto.alineacion, punto.id)
        
       
class Plano:
    def __init__(self):
        self.ancho, self.alto = 1200, 600
        self.screen = pygame.display.set_mode((self.ancho, self.alto))
        self.rectangulo = pygame.Rect(500, 70, 360, 360)
        # Estado actual
        self.arbol = ArbolBinarioProyecto()
        self.puntos = []
        self.rectas = []
        self.rectasy=[]
        self.rectasx=[]
        self.areas = []
        self.espaciado = None

    def cargar_datos_ejemplo(self, puntos):
        self.arbol = ArbolBinarioProyecto()
        self.puntos = puntos
        for punto in self.puntos:
            self.arbol.insertar(punto)
        # Generar los puntos
        anchura = self.arbol.recorrido_anchura()
        self.puntos = self.generar_puntos(anchura)

    def generar_puntos(self, anchura):
        # Generar los puntos en el plano
        puntos = []
        id=0
        for fila in anchura:
            altura = anchura.index(fila) + 1
            for punto in fila:
                if altura % 2 == 0:
                    punto = Punto(punto[0], punto[1],1, id)
                else:   
                    punto = Punto(punto[0], punto[1],0, id)
                id+=1
                puntos.append(punto)
        return puntos

    def calcular_ecuacion_recta(self, p1, p2):
        """Calcula la ecuación de la recta en la forma Ax + By + C = 0."""
        x1, y1 = p1
        x2, y2 = p2
        A = y2 - y1
        B = x1 - x2
        C = x2 * y1 - x1 * y2
        return A, B, C

    def interseccion_rectas(self, p1, p2, p3, p4):
        """Calcula la intersección entre dos segmentos de recta dados por sus puntos de inicio y fin."""
        # Calcular las ecuaciones de las rectas
        A1, B1, C1 = self.calcular_ecuacion_recta(p1, p2)
        A2, B2, C2 = self.calcular_ecuacion_recta(p3, p4)

        # Crear la matriz de coeficientes y el vector de términos independientes
        coeficientes = np.array([[A1, B1], [A2, B2]])
        terminos_independientes = np.array([-C1, -C2])

        try:
            # Resolver el sistema de ecuaciones
            x, y = np.linalg.solve(coeficientes, terminos_independientes)
            
            # Verificar si el punto está dentro de ambos segmentos
            def esta_en_segmento(px, py, p1, p2):
                x_min, x_max = min(p1[0], p2[0]), max(p1[0], p2[0])
                y_min, y_max = min(p1[1], p2[1]), max(p1[1], p2[1])
                
                # Añadir una pequeña tolerancia para errores de punto flotante
                epsilon = 1e-9
                return (x_min - epsilon <= px <= x_max + epsilon and 
                        y_min - epsilon <= py <= y_max + epsilon)
            
            if esta_en_segmento(x, y, p1, p2) and esta_en_segmento(x, y, p3, p4):
                return x, y
            else:
                return None
        except np.linalg.LinAlgError:
            # Si las rectas son paralelas o coincidentes
            return None


#posicion el plano en x
    def generar_rectas_areas(self, puntos, plano_rect, espaciado):
        # Crear lista vacia de rectas actuales con alineacion X
        rectas_x = []
        # Crear lista vacia de rectas actuales con alineacion Y
        rectas_y = []

        rectas_completas = []

        areas = []
        areas.append(Seccion(plano_rect.x, plano_rect.y, plano_rect.width, plano_rect.height, id=1))
      

        # Recorrer los puntos
        for punto in puntos:

            # Si la alineacion del punto es X
            if punto.alineacion == 0:
                # int(punto.x*espaciado + plano_rect.x)
                
                # Recta prototipo, ubica la recta con el punto y el espaciado en el plano
                recta = Recta((int(plano_rect.x + punto.x * espaciado), int(plano_rect.topleft[1])), (int(plano_rect.x + punto.x * espaciado), int(plano_rect.bottomleft[1])), punto)

                # Si la lista de rectas Y esta vacia
                if not rectas_y:
                    # Agregar la recta a la lista de rectas X
                    areas = self.actualizar_areas(areas, recta, rectas_x, rectas_y)
                    rectas_x.append(recta)
                    rectas_completas.append(recta)

                else:
                    # Si la lista de rectas Y no esta vacia
                    
                    # Borde superior de la cuadricula en Y
                    menor = plano_rect.topleft[1]
                    # Borde inferior de la cuadricula en Y
                    mayor = plano_rect.bottomleft[1]

                    for rectay in rectas_y:
                        interseccion = self.interseccion_rectas(recta.inicio, recta.fin, rectay.inicio, rectay.fin)
                        if punto.y == rectay.punto.y:
                            pass
                        else:
                            if interseccion:
                                if rectay.punto.y < punto.y:
                                    if interseccion[1] > menor:
                                        menor = interseccion[1]
                                else:
                                    if interseccion[1] < mayor:
                                        mayor = interseccion[1]

                    recta.inicio = (recta.inicio[0], menor)
                    recta.fin = (recta.fin[0], mayor)
                    areas = self.actualizar_areas(areas, recta, rectas_x, rectas_y)
                    rectas_x.append(recta)
                    rectas_completas.append(recta)
                    
                

            # Si la alineacion del punto es Y
            elif punto.alineacion == 1:
              
                # Recta prototipo
                recta = Recta((int(plano_rect.topleft[0]), int(plano_rect.y + punto.y * espaciado)), (int(plano_rect.topright[0]), int(plano_rect.y + punto.y * espaciado)), punto)

                # Si la lista de rectas X esta vacia
                if not rectas_x:
                    # Agregar la recta a la lista de rectas Y
                    areas = self.actualizar_areas(areas, recta, rectas_x, rectas_y)
                    rectas_y.append(recta)
                    rectas_completas.append(recta)

                else:
                    # Si la lista de rectas Y no esta vacia
            
                    # Borde izquierda de la cuadricula en X
                    menor = plano_rect.topleft[0]
                    # Borde derecha de la cuadricula en X
                    mayor = plano_rect.topright[0]

                    for rectax in rectas_x:
                        interseccion = self.interseccion_rectas(recta.inicio, recta.fin, rectax.inicio, rectax.fin)
                        if punto.x == rectax.punto.x:
                            pass
                        else:
                            if interseccion:
                                if rectax.punto.x < punto.x:
                                    if interseccion[0] > menor:
                                        menor = interseccion[0]
                                else:
                                    if interseccion[0] < mayor:
                                        mayor = interseccion[0]

                    recta.inicio = (menor, recta.inicio[1])
                    recta.fin = (mayor, recta.fin[1])
                    areas = self.actualizar_areas(areas, recta, rectas_x, rectas_y)
                    rectas_y.append(recta)
                    rectas_completas.append(recta)
            

        # Devolver listado de rectas generadas
        
        return rectas_completas, areas

    def actualizar_areas(self, areas, recta, rectasx, rectasy):
        continuar = True
        rectax=None
        rectay=None
        #Si ya existe una recta con el mismo punto en su respectiva alineacion no cree mas areas
        if recta.punto.alineacion == 0 and rectasx:
            for rectax in rectasx:
                if recta.punto.x == rectax.punto.x:
                    continuar = False
        if recta.punto.alineacion == 1 and rectasy:
            for rectay in rectasy:
                if recta.punto.y == rectay.punto.y:
                    continuar = False
                    
        if continuar:
            areas_a_procesar = areas.copy()  # Copia la lista para poder modificar la original
            iniciox = None
            inicioy = None
            finx = None
            finy = None
            
            # Para que las rectas no se superpongan
            if recta.punto.alineacion == 0:
                iniciox = recta.inicio[0]
                inicioy = recta.inicio[1]+1
                finx = recta.fin[0]
                finy = recta.fin[1]-1
            elif recta.punto.alineacion == 1:
                iniciox = recta.inicio[0]+1
                inicioy = recta.inicio[1]
                finx = recta.fin[0]-1
                finy = recta.fin[1]
        
            
            for area in areas_a_procesar:

                # Verificar si el punto está dentro del área usando coordenadas transformadas
                if area.rectangulo.collidepoint(iniciox, inicioy):
                    # Si la alineación del punto es X (vertical)
                    if recta.punto.alineacion == 0:
                        # Crear nueva área a la derecha de la línea
                        nueva_x = recta.inicio[0]
                        nueva_ancho = area.rectangulo.right - nueva_x
                        area_nueva = Seccion(nueva_x, area.rectangulo.y, nueva_ancho, area.rectangulo.height, id=len(areas)+1)
                        
                        # Modificar el área original (ahora es la izquierda)
                        nueva_ancho_original = recta.inicio[0] - area.rectangulo.x
                        area.rectangulo.width = nueva_ancho_original
                        area.rectangulo = pygame.Rect(area.rectangulo.x, area.rectangulo.y, area.rectangulo.width, area.rectangulo.height)

                        areas.append(area_nueva)
                        

                        
                    # Si la alineación del punto es Y (horizontal)
                    elif recta.punto.alineacion == 1:
                        # Crear nueva área debajo de la línea
                        nueva_y = recta.inicio[1]
                        nueva_altura = area.rectangulo.bottom - nueva_y
                        area_nueva = Seccion(area.rectangulo.x, nueva_y, area.rectangulo.width, nueva_altura, id=len(areas)+1)
                        
                        # Modificar el área original (ahora es la de arriba)
                        nueva_altura_original = recta.inicio[1] - area.rectangulo.y
                        area.rectangulo.height = nueva_altura_original
                        area.rectangulo = pygame.Rect(area.rectangulo.x, area.rectangulo.y, area.rectangulo.width, area.rectangulo.height)
                        
                        areas.append(area_nueva)
                        

                elif area.rectangulo.collidepoint(finx, finy):
                    # Si la alineación del punto es X (vertical)
                    if recta.punto.alineacion == 0:
                        # Crear nueva área a la derecha de la línea
                        nueva_x = recta.inicio[0]
                        nueva_ancho = area.rectangulo.right - nueva_x
                        area_nueva = Seccion(nueva_x, area.rectangulo.y, nueva_ancho, area.rectangulo.height, id=len(areas)+1)
                        
                        # Modificar el área original (ahora es la izquierda)
                        nueva_ancho_original = area.rectangulo.width - nueva_ancho
                        area.rectangulo.width = nueva_ancho_original
                        area.rectangulo = pygame.Rect(area.rectangulo.x, area.rectangulo.y, area.rectangulo.width, area.rectangulo.height)
                        
                        
                        areas.append(area_nueva)
                        
                    # Si la alineación del punto es Y (horizontal)
                    elif recta.punto.alineacion == 1:
                        # Crear nueva área debajo de la línea
                        nueva_y = recta.inicio[1]
                        nueva_altura = area.rectangulo.bottom - nueva_y
                        area_nueva = Seccion(area.rectangulo.x, nueva_y, area.rectangulo.width, nueva_altura, id=len(areas)+1)
                        
                        # Modificar el área original (ahora es la de arriba)
                        nueva_altura_original = area.rectangulo.height - nueva_altura
                        area.rectangulo.height = nueva_altura_original
                        area.rectangulo = pygame.Rect(area.rectangulo.x, area.rectangulo.y, area.rectangulo.width, area.rectangulo.height)
                         
                        areas.append(area_nueva)    
        return areas
        
        
    def dibujar_plano(self, puntos=None):
        # Dibujar el fondo del plano
        plano_rect = pygame.Rect(500, 70, 360, 360)
        pygame.draw.rect(self.screen, colores.AZUL_OSCURO, plano_rect)
        pygame.draw.rect(self.screen, colores.CELESTE, plano_rect, 2)

        if not self.puntos:
            # Asignar los puntos al plano
            return

        # Encontrar límites de los puntos para ajustar la escala
        x_max = max(p.x for p in self.puntos)
        y_max = max(p.y for p in self.puntos)
        maximo = max(x_max, y_max) + 1

        espaciado= plano_rect.width // maximo
        self.espaciado=espaciado

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

        self.rectas, self.areas = self.generar_rectas_areas(self.puntos, plano_rect, espaciado)
        self.dibujar_rectas()

    
    def colorear_area(self):
        # Crear una superficie con canal alfa del mismo tamaño que la pantalla
        superficie_transparente = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        colores_area = colores.colores_area
        
        # Iterar por todas las áreas y colorearlas
        for i, area in enumerate(self.areas):
            
            color = colores_area[i % len(colores_area)]
            pygame.draw.rect(superficie_transparente, color, area.rectangulo)
            # Opcional: Mostrar el ID del área
            fuente = pygame.font.Font(None, 20)
            texto = fuente.render(str(area.id), True, (255, 255, 255))
            superficie_transparente.blit(texto, (area.rectangulo.centerx - 5, area.rectangulo.centery - 5))
           
        self.screen.blit(superficie_transparente, (0, 0))

    def colorear_area_personalizada(self, colores_area_personalizados, colores_borde_personalizados):
        # Crear una superficie con canal alfa del mismo tamaño que la pantalla
        superficie_transparente = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)

        colores_area = colores_area_personalizados
        colores_borde = colores_borde_personalizados

        # Iterar por todas las áreas y colorearlas
        for i, area in enumerate(self.areas):
            color = colores_area[i % len(colores_area)]
            color_borde = colores_borde[i % len(colores_borde)]

            pygame.draw.rect(superficie_transparente, color, area.rectangulo)
            pygame.draw.rect(superficie_transparente, color_borde, area.rectangulo, 2)
            # Opcional: Mostrar el ID del área
            fuente = pygame.font.Font(None, 20)
            texto = fuente.render(str(area.id), True, (255, 255, 255))
            superficie_transparente.blit(texto, (area.rectangulo.centerx - 5, area.rectangulo.centery - 5))
           
        self.screen.blit(superficie_transparente, (0, 0))

    def colorear_seccion(self, color, area):
        pantalla= pygame.Surface((self.rectangulo.width, self.rectangulo.height))
        pygame.draw.rect(pantalla, color , area.rectangulo)
        # Opcional: Mostrar el ID del área
        fuente = pygame.font.Font(None, 20)
        texto = fuente.render(str(area.id), True, (255, 255, 255))
        pantalla.blit(texto, (area.rectangulo.centerx - 5, area.rectangulo.centery - 5))

    def dibujar_puntos(self, plano_rect, espaciado):
        for punto in self.puntos:
            # Convertir coordenadas a posición en pantalla (relativas al plano)
            px = int(punto.x*espaciado + plano_rect.x)
            py = int(punto.y*espaciado + plano_rect.y)
            # Dibujar el punto
            pygame.draw.circle(self.screen, colores.VERDE_AGUA, (px, py), 4)

    def dibujar_rectas(self):
        for recta in self.rectas:
            # Convertir coordenadas a posición en pantalla
            inicio = (int(recta.inicio[0]), int(recta.inicio[1]))
            fin = (int(recta.fin[0]), int(recta.fin[1]))
            # Dibujar la recta
            pygame.draw.line(self.screen, colores.ROJO, inicio, fin, 2)

    
            
# Clase para el selector de colores
class SelectorColores:
    def __init__(self, seccion, lista_colores):
        self.seccion = seccion
        self.lista_colores = lista_colores
        self.color_seleccionado = None
        self.cuadros_colores = []
        self.inicializar_cuadros()
        
    def inicializar_cuadros(self):
        # Calcular dimensiones de los cuadros de colores
        margen = 10
        tamaño_cuadro = min(30, (self.seccion.rectangulo.width - margen * (len(self.lista_colores) + 1)) // len(self.lista_colores))
        
        # Crear los cuadros de colores
        x_inicio = self.seccion.rectangulo.x + margen
        y_pos = self.seccion.rectangulo.y + 40  # Posición después del título
        
        for i, color in enumerate(self.lista_colores):
            x_pos = x_inicio + (tamaño_cuadro + margen) * i
            rect = pygame.Rect(x_pos, y_pos, tamaño_cuadro, tamaño_cuadro)
            self.cuadros_colores.append((rect, color))
    
    def dibujar_seccion_color(self, pantalla):
        # Primero dibujar la sección
        self.seccion.dibujar(pantalla)
        
        # Luego dibujar los cuadros de colores
        for rect, color in self.cuadros_colores:
            pygame.draw.rect(pantalla, color, rect)
            
            # Dibujar un borde alrededor del color seleccionado
            if self.color_seleccionado == color:
                pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
    
    def manejar_clic_color(self, pos_mouse):
        for rect, color in self.cuadros_colores:
            if rect.collidepoint(pos_mouse):
                self.color_seleccionado = color
                return True
        return False
    def manejar_clic_area(self, pos_mouse, plano):
        for area in plano.areas:
            if area.rectangulo.collidepoint(pos_mouse):
                return True
        return False
    
    def obtener_color_seleccionado(self):
        return self.color_seleccionado
    
    def detectar_clic_seccion(self, plano, pos):
        """Detecta qué sección fue clicada y la establece como activa"""
        for seccion in plano.areas:
            if seccion.rectangulo.collidepoint(pos):
                self.seccion_activa = seccion
                return seccion
        # Si el clic no está en ninguna sección
        self.seccion_activa = None
        return None