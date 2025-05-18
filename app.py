import random
import sys, os
import pygame
import copy
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import views.colores as colores
from views.arbolView import VisualizadorArbol
from views.planoView import Plano
from views.planoView import Punto
from views import cargarArchivo
from views.UI import Boton as Boton
from views.UI import Seccion as Seccion
from views.UI import crear_diseño as crear_diseño
from models.metodos import permutar
from models.metodos import encontrar_mejor_arbol_plano
from models.metodos import puntos_a_pixel
from models.metodos import distance
from models.metodos import encontrar_limites
from models.metodos import detectar_seccion
from models.metodos import crear_cuadro_texto
from models.metodos import dibujar_textos
from views.planoView import SelectorColores

colores_borde = [
        colores.ROJO,
        colores.VERDE,
        colores.AZUL,
        colores.AMARILLO,
        colores.CIAN,
        colores.MAGENTA,
        (0,0,0,0)
    ]

colores_area_personalizados = copy.copy(colores.colores_area_personalizados)
colores_borde_personalizados = copy.copy(colores.colores_area_personalizados)


# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTURA = 1200, 600
pantalla = pygame.display.set_mode((ANCHO, ALTURA))
#Nombre de la pestaña
pygame.display.set_caption("Visualización de Árboles")

def principal():
    #Permite controlar el ritmo de la apicacion
    reloj = pygame.time.Clock()
    secciones, botones = crear_diseño()
     # Crear y configurar el arbol de árboles
    arbol = VisualizadorArbol()
    mejor_arbol = VisualizadorArbol()

    plano = Plano()
    mejor_plano = Plano()
    plano_personalizado = Plano()

    # Iniciaizar valores en None para que puedan leerse la primera vez
    
    informacion = "¡Bienvenido al sistema de visualizacion de planos! \n - Para cargar tus puntos: click en el botón 'Cargar JSON'\n - Para ver todos los árboles generados: 'Mostrar plano del carrusel'\n - Para ver el plano con menor cantidad de divisiones: 'Mostrar plano óptimo' \n - Para personalizar algún plano: elige el carrusel o el plano óptimo, luego, \n presiona personalizar, este se guardará en 'Mostrar árbol personalizado'."
    eleccion_config = "Informacion apli"

    dragging = False
    puntos_plano = []
    permutaciones = []
    puntero = 0
    mejor_permutacion = []
    mejor_arbol_seccion = None
    carrusel_seccion = None
    puntero_seccion = None
    info_mejor = None
    info_actual = None
    config_actual = None
    active = False
    active_texto = False
    text = ''
    text_poner=''
    eleccion_plano = 0 
    area= None
    color_seleccionado = None
    color_borde_seleccionado= None
    area_texto = None
    cuadros_texto= []

    for seccion in secciones:
        if seccion.titulo == "Mejor árbol":
                mejor_arbol_seccion = seccion
        if seccion.titulo == "Carrusel de árboles":
                carrusel_seccion = seccion
        if seccion.titulo == "Puntero":
                puntero_seccion = seccion
        if seccion.titulo == "Info árbol actual":
                info_actual = seccion
        if seccion.titulo == "Info mejor árbol":
                info_mejor = seccion
        if seccion.titulo == "Configuracion actual":
                config_actual = seccion     
        
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            # Evento de cerrar la ventana
            if evento.type == pygame.QUIT:
                ejecutando = False
            # Evento de algun boton del mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Clic izquierdo
                    # If the user clicked on the puntero_arbol rect.
                    if puntero_seccion.rectangulo.collidepoint(evento.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False

                    if active_texto:
                        print(f"Texto ingresado: {text_poner}")
                        
                        if detectar_seccion(plano_personalizado, evento.pos):
                            area_texto = detectar_seccion(plano_personalizado, evento.pos)
                            print(area_texto.id)
                            
                            # Crear cuadro de texto en la posición del evento
                            cuadro_texto = crear_cuadro_texto(text_poner)                            
                            # Posicionar el cuadro de texto en la posición del evento
                            x, y = evento.pos
                            
                            # Ajustar posición para que el cuadro no salga de los límites de la pantalla
                            x = min(x, pantalla.get_width() - cuadro_texto.get_width())
                            y = min(y, pantalla.get_height() - cuadro_texto.get_height())
                            
                            cuadros_texto.append((cuadro_texto, x, y))
                                                    
                            text_poner = ''  # Limpiar el texto
                        else: 
                            active_texto = False
                                        
                    for boton in botones:
                        # Evento.pos es la posición del mouse en el momento del evento
                        if boton.es_presionado(evento.pos):
                            if boton.id == "cargar_json":
                                eleccion_plano = 0  # 0: Mostrar plano mejor, 1: Mostrar plano carrusel, 2: Mostrar plano personalizado
                                puntos = cargarArchivo.cargar_archivo()
                                permutar(puntos, permutaciones, []) 
                                
                                mejor_permutacion, indice = encontrar_mejor_arbol_plano(permutaciones)
                                # Cargar puntos para el arbol y para el plano del carrusel
                                plano.cargar_datos_ejemplo(permutaciones[puntero])
                                arbol.cargar_datos_ejemplo(permutaciones[puntero])
                                # Cargar puntos para el arbol y para el plano mejores
                                mejor_arbol.cargar_datos_ejemplo(mejor_permutacion)
                                mejor_plano.cargar_datos_ejemplo(mejor_permutacion)
                            
                            if boton.id == "anadir":
                                eleccion_config = "escribir"
                                active_texto = not active_texto
                            else:
                                active_texto = False

                            if boton.id == "Personalizar":
                                if eleccion_plano==0:
                                    plano_personalizado.cargar_datos_ejemplo(mejor_permutacion)
                                    print("Cargué el plano")

                                elif eleccion_plano==1:
                                    plano_personalizado.cargar_datos_ejemplo(permutaciones[puntero])
                                    print("Cargué el plano")

                                
                            if boton.id == "-Mostrar Plano Optimo":
                                eleccion_plano = 0

                            if boton.id == "-Mostrar Plano Carrusel":
                                eleccion_plano = 1

                            if boton.id == "-Mostrar Plano Personalizado":
                                eleccion_plano = 2  

                            if boton.id == "flecha_izquierda":
                                if puntero > 0:
                                    puntero -= 1
                                else:
                                   puntero = len(permutaciones)-1
                                print(f"Lista: {permutaciones[puntero]}, puntero: {puntero}")
                                arbol.cargar_datos_ejemplo(permutaciones[puntero])
                                plano.cargar_datos_ejemplo(permutaciones[puntero])

                            
                            if boton.id == "flecha_derecha":
                                if puntero >= len(permutaciones)-1:
                                    puntero = 0
                                else:
                                    puntero += 1
                          
                                arbol.cargar_datos_ejemplo(permutaciones[puntero])
                                plano.cargar_datos_ejemplo(permutaciones[puntero])

                            if boton.id == "instrucciones":
                                eleccion_config = "Informacion apli"
                            
                            if boton.id == "-Color fondo seccion":
                                eleccion_config = "-Color fondo seccion"
                            
                            if boton.id == "-Cambiar borde seccion":
                                eleccion_config = "-Cambiar borde seccion"

                    if eleccion_plano == 2:
                        #Posicion del cursor
                        mouse_pos = pygame.mouse.get_pos()
                        # Verificar si se hizo clic en algún punto
                        for i, punto in enumerate(puntos_plano):
                            if distance(punto, mouse_pos) <= 8:
                                #Guarda el indice de los puntos del plano
                                selected_point = i
                                minimo_eje1, maximo_eje1, eje, minimo_eje2, maximo_eje2 = encontrar_limites(plano_personalizado.puntos, plano_personalizado.puntos[selected_point], plano_personalizado.espaciado)
                                dragging = True
                                #Si se mueve un punto se borran los cuadros de texto que haya añadido
                                cuadros_texto = []
                                break
            #Si se suelta un punto no dibujar mas
            elif evento.type == pygame.MOUSEBUTTONUP and eleccion_plano == 2:
                if evento.button == 1:  # Botón izquierdo
                    dragging = False
            
            elif evento.type == pygame.MOUSEMOTION and eleccion_plano == 2:
                if dragging and selected_point is not None:
                    # Actualizar la posición del punto seleccionado
                    if eje == 0:
                        #Manejar limites para que no se salga del rectangulo
                        if evento.pos[eje] < maximo_eje1 and evento.pos[eje] > minimo_eje1 and evento.pos[eje+1] < maximo_eje2 and evento.pos[eje+1] > minimo_eje2:
                            #Cambiar las coordenadas del punto en pixeles
                            puntos_plano[selected_point] = evento.pos
                            #Guardar ese punto en pixeles
                            punto_nuevo = puntos_plano[selected_point]
                            #Hacer la conversion de pixeles a punto normal
                            x=(punto_nuevo[0] - plano_personalizado.rectangulo.x) // plano_personalizado.espaciado
                            y= (punto_nuevo[1] - plano_personalizado.rectangulo.y)  // plano_personalizado.espaciado
                            alineacion= plano_personalizado.puntos[selected_point].alineacion
                            
                            #Re asignar la coordenada del punto en plano_personalizado.puntos
                            plano_personalizado.puntos[selected_point] = Punto(x, y,alineacion)
                    if eje == 1:
                        if evento.pos[eje] < maximo_eje2 and evento.pos[eje] > minimo_eje2 and evento.pos[eje-1] < maximo_eje1 and evento.pos[eje-1] > minimo_eje1:
                            puntos_plano[selected_point] = evento.pos
                            punto_nuevo = puntos_plano[selected_point]
                            
                            x=(punto_nuevo[0] - plano_personalizado.rectangulo.x) // plano_personalizado.espaciado
                            y= (punto_nuevo[1] - plano_personalizado.rectangulo.y)  // plano_personalizado.espaciado
                            alineacion= plano_personalizado.puntos[selected_point].alineacion
                            
                            plano_personalizado.puntos[selected_point] = Punto(x, y,alineacion)
                        

                
            # Manejo de entrada de teclado (fuera del evento del mouse)
            elif evento.type == pygame.KEYDOWN:
                if active:
                    #Detecta si se presiono la tecla enter
                    if evento.key == pygame.K_RETURN:
                        print(f"Texto ingresado: {text}")
                        try:
                            nuevo_puntero = int(text)
                            if 0 < nuevo_puntero <= len(permutaciones):
                                puntero = nuevo_puntero
                                arbol.cargar_datos_ejemplo(permutaciones[puntero-1])
                           
                        except (ValueError, NameError):
                            print("Valor no válido o permutaciones no definidas aún")
                        text = ''
                    #Tecla de retroceso, borrar texto en text
                    elif evento.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        # Solo permitir números
                        if evento.unicode.isdigit():
                            text += evento.unicode 

                if active_texto:
                    #Tecla de retroceso, borrar texto en text
                    if evento.key == pygame.K_BACKSPACE:
                        text_poner = text_poner[:-1]
                    
                    else:
                        if len(text_poner) < 20:
                            text_poner += evento.unicode
                        else:
                            text_poner = text_poner[:-1]

                         
                                              
        
        # Dibujar fondo
        pantalla.fill(colores.AZUL_MAS_OSCURO)
        
        # Dibujar secciones
        for seccion in secciones:
            seccion.dibujar(pantalla)
        
        # Dibujar el árbol en la sección "Carrusel"
        if carrusel_seccion:
            arbol.dibujar_arbol(pantalla, carrusel_seccion)
        
        # Dibujar el mejor árbol en la sección "Mejor árbol"
        if mejor_arbol_seccion:
            mejor_arbol.dibujar_arbol(pantalla, mejor_arbol_seccion)
        
        # Renderizar el texto en la sección del puntero
        if puntero_seccion:
            # Dibujar caja de texto con color diferente cuando está activa
            color_fondo = colores.MORADO if active else colores.BLANCO
            pygame.draw.rect(pantalla, color_fondo, puntero_seccion.rectangulo)
            pygame.draw.rect(pantalla, colores.NEGRO, puntero_seccion.rectangulo, 2)
            
            # Renderizar texto
            texto_surface = pygame.font.SysFont(None, 24).render(text, True, colores.NEGRO)
            # Centrar el texto en la sección
            text_rect = texto_surface.get_rect(center=puntero_seccion.rectangulo.center)
            #blit() toma el contenido de texto_surface y lo "pinta" sobre pantalla en la posición especificada por text_rect.
            pantalla.blit(texto_surface, text_rect)
        
        # Dibujar botones
        for boton in botones:
            boton.dibujar(pantalla)
            cuadro_perso= pygame.Rect(925,255,240,40)
            titulo_perso= pygame.font.Font(None, 20).render("Configuraciones de plano personalizado", True, colores.BLANCO)
            pantalla.blit(titulo_perso, (cuadro_perso.x-10,cuadro_perso.y-2))

        
        # Escribir la información de los árboles
        if info_actual:
            if permutaciones:
                cantidad = len(permutaciones)
                permutacion = permutaciones[puntero]
                espaciado = (info_actual.rectangulo.height - 45) // (len(permutacion)+2)
                lineas = [str(p) for p in permutacion]  # 
                texto = f"Árbol {puntero+1} de {cantidad}\nÓrden de los puntos:\n" + "\n".join(lineas)
                lineas = texto.split('\n')  # Dividir texto en líneas
                y_offset = info_actual.rectangulo.y + 45
                for linea in lineas:
                    cuadro_texto = pygame.font.Font(None, 16).render(linea, True, colores.BLANCO)
                    pantalla.blit(cuadro_texto, (info_actual.rectangulo.x + 10, y_offset))
                    y_offset +=espaciado  # Ajustar la separación entre líneas
        
        if info_mejor:
            if permutaciones:
                cantidad = len(permutaciones)
                permutacion = mejor_permutacion
                espaciado = (info_mejor.rectangulo.height - 45) // (len(permutacion)+2)
                lineas = [str(p) for p in permutacion]  # 
                texto = f"Árbol {indice+1} de {cantidad}\nÓrden de los puntos:\n" + "\n".join(lineas)
                lineas = texto.split('\n')  # Dividir texto en líneas
                y_offset = info_mejor.rectangulo.y + 45
                for linea in lineas:
                    cuadro_texto = pygame.font.Font(None, 16).render(linea, True, colores.BLANCO)
                    pantalla.blit(cuadro_texto, (info_actual.rectangulo.x + 10, y_offset))
                    y_offset +=espaciado  # Ajustar la separación entre líneas
        
        # Escribir información del programa
        if config_actual:
            if eleccion_config == "Informacion apli":
                lineas_info = informacion.split('\n')
                fuente = pygame.font.Font(None, 16)

                # Ajustar la posición inicial con un margen izquierdo
                margen_x = config_actual.rectangulo.x + 5
                y_inicial = config_actual.rectangulo.y + 10

                #Rectangulo blanco para borrar lo que habia
                pygame.draw.rect(pantalla, colores.BLANCO, config_actual.rectangulo)


                # Calcular espaciado dinámico para las líneas
                espaciado_info = max(20, (config_actual.rectangulo.height - 15) // len(lineas_info)) -3

                # Dibujar todas las líneas dentro del rectángulo
                inter = y_inicial
                for linea in lineas_info:
                    cuadro_texto = fuente.render(linea, True, colores.NEGRO)
                    pantalla.blit(cuadro_texto, (margen_x, inter))
                    inter += espaciado_info

                    # Detener si excede la altura del rectángulo
                    if inter > config_actual.rectangulo.y + config_actual.rectangulo.height:
                        break
                    
            if eleccion_config == "-Color fondo seccion":
                selector = SelectorColores(config_actual, colores.colores_area)
                selector.dibujar_seccion_color(pantalla)
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  
                        #Encontrar el color
                        if selector.manejar_clic_color(evento.pos):
                            color_seleccionado= selector.obtener_color_seleccionado()

                        #Detectar el area
                        if selector.detectar_clic_seccion(plano_personalizado, evento.pos):
                            area = selector.detectar_clic_seccion(plano_personalizado, evento.pos)
                            
                        if area and color_seleccionado:
                            colores_area_personalizados[area.id-1] = color_seleccionado
                            area = None
                            color_seleccionado= None
                            
            if eleccion_config == "-Cambiar borde seccion":
                selector = SelectorColores(config_actual, colores_borde)
                selector.dibujar_seccion_color(pantalla)
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:  
                        #Encontrar el color
                        if selector.manejar_clic_color(evento.pos):
                            color_borde_seleccionado= selector.obtener_color_seleccionado()

                        #Detectar el area
                        if selector.detectar_clic_seccion(plano_personalizado, evento.pos):
                            area = selector.detectar_clic_seccion(plano_personalizado, evento.pos)
                            
                        if area and color_borde_seleccionado:
                            colores_borde_personalizados[area.id-1] = color_borde_seleccionado
                            area = None
                            color_borde_seleccionado= None
            
            if eleccion_config == "escribir":
               
                # Dibujar caja de texto con color diferente cuando está activa
                color_fondo = colores.MORADO if active_texto else colores.BLANCO
                pygame.draw.rect(pantalla, color_fondo, config_actual.rectangulo)
                pygame.draw.rect(pantalla, colores.NEGRO, config_actual.rectangulo, 2)
                
                # Renderizar texto
                texto_surface = pygame.font.SysFont(None, 24).render(text_poner, True, colores.NEGRO)
                # Centrar el texto en la sección
                text_rect = texto_surface.get_rect(center=config_actual.rectangulo.center)
                #blit() toma el contenido de texto_surface y lo "pinta" sobre pantalla en la posición especificada por text_rect.
                pantalla.blit(texto_surface, text_rect)

        # Elegir que arbol mostrar
        if eleccion_plano == 0:
            mejor_plano.dibujar_plano()
            mejor_plano.dibujar_puntos(mejor_plano.rectangulo, mejor_plano.espaciado)
            mejor_plano.colorear_area()
        elif eleccion_plano == 1:
            #Para cargar donde quedo ubicado
            plano.cargar_datos_ejemplo(permutaciones[puntero])
            plano.dibujar_plano()
            plano.dibujar_puntos(plano.rectangulo, plano.espaciado)
            plano.colorear_area()
        elif eleccion_plano == 2:
            #En cada iteracion va dibujando el plano de acorde a sus cambios
            plano_personalizado.dibujar_plano()
            puntos_plano = puntos_a_pixel(plano_personalizado.puntos, plano_personalizado.espaciado)
            #Los colorea segun el color que se añada a colores_area_personalizados y colores_borde_personalizados
            plano_personalizado.colorear_area_personalizada( colores_area_personalizados, colores_borde_personalizados)
            #Dibuja los puntos para que no se superpongan
            plano_personalizado.dibujar_puntos(plano_personalizado.rectangulo, plano_personalizado.espaciado)
            #Dibuja la casilla de texto que se inserte en x posicion 
            dibujar_textos(cuadros_texto, pantalla)


        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()


#Ejecutar el bloque principal
if __name__ == "__main__":
    principal()