import pygame
MORADO = (160, 132, 220)
MORADO_CLARO = (229, 204, 255)
AZUL = (102, 102, 255)
VERDE = (102, 204, 153)
ROSA = (204, 153, 204)
CREMA = (255, 255, 204)
ROJO = (255, 102, 102)
NARANJA = (255, 178, 102)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS_CLARO = (240, 240, 240)
AZUL_OSCURO = (15, 25, 35)
AZUL_MAS_OSCURO = (14, 15, 31)
CELESTE = (0, 191, 255)
VERDE_AGUA = (0, 200, 170)

#Colores para escoger

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CIAN = (0, 255, 255)
MAGENTA = (255, 0, 255)



colores_area = [
            (0, 0, 255, 100),     # Azul con 39% de transparencia
            (0, 255, 0, 100),     # Verde con 39% de transparencia  
            (255, 165, 0, 100),   # Naranja con 39% de transparencia
            (128, 0, 128, 100),   # Morado con 39% de transparencia
            (255, 255, 0, 100),   # Amarillo con 39% de transparencia
            (255, 0, 0, 100),     # Rojo con 39% de transparencia
            (0, 255, 255, 100),   # Cian con 39% de transparencia
            (204, 153, 204, 100), # Rosa
            (255, 255, 204, 100), # Crema
            (229, 204, 255, 100), # Morado claro
            (0,0,0,0) #transparente total
        ]

colores_area_personalizados=[]
for i in range(20):
    colores_area_personalizados.append((0,0,0,0))
