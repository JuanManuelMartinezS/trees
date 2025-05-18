class Nodo:
    def __init__(self, x, y):
        self.valor = (x,y) # Cada nodo tiene como valor una tupla con los puntos en "X" y "Y"
        self.izquierda = None
        self.derecha = None
        self.padre = None # Referencia al padre para saber orden de inserción
        self.altura = 1

class ArbolBinarioProyecto:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor[0],valor[1])
        else:
            self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if nodo.altura %2 !=0:
            if valor[0] < nodo.valor[0]:
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor[0],valor[1])
                    nodo.izquierda.padre = nodo
                    nodo.izquierda.altura = nodo.altura + 1
                else:
                    
                    self._insertar(nodo.izquierda, valor)
            elif valor[0] >= nodo.valor[0]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor[0],valor[1])
                    nodo.derecha.padre = nodo
                    nodo.derecha.altura = nodo.altura + 1
                else:
                    self._insertar(nodo.derecha, valor)
        else:
            if valor[1] < nodo.valor[1]:
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor[0],valor[1])
                    nodo.izquierda.padre = nodo
                    nodo.izquierda.altura = nodo.altura + 1
                else:
                    self._insertar(nodo.izquierda, valor)
            elif valor[1] >= nodo.valor[1]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor[0],valor[1])
                    nodo.derecha.padre = nodo
                    nodo.derecha.altura = nodo.altura + 1
                else:
                    self._insertar(nodo.derecha, valor)

    def recorrido_anchura(self):
        nodos = [[]]
        self._recorrido_anchura(self.raiz, nodos, 0)
        return nodos
    
    def _recorrido_anchura(self, nodo, nodos, h):
        if nodo is None:
            return
        else:
            nodos.append([])
            nodos[h].append(nodo.valor)
            self._recorrido_anchura(nodo.izquierda, nodos, h+1)
            if not nodos[-1]:
                nodos.pop()
            self._recorrido_anchura(nodo.derecha, nodos, h+1)
            if not nodos[-1]:
                nodos.pop()
                
    def obtener_altura(self):
        alturas = [0]  # Uso una lista de un solo elemento para que sea mutable, ya que los enteros son inmutables
        self._alturas(self.raiz, alturas, 0)
        return alturas[0]  # Devolver el valor almacenado en la lista

    def _alturas(self, nodo, alturas, altura):
        if nodo is not None:
            altura+= 1
            if altura> alturas[0]:
                alturas[0] = altura # Se modifica la lista, afectando la variable original
            self._alturas(nodo.izquierda, alturas, altura)
            self._alturas(nodo.derecha, alturas, altura)

# Ejemplo de uso
if __name__ == "__main__":
    arbol = ArbolBinarioProyecto()
    tupla=[(5,8), (1, 13), (10, 15), (11, 15), (20, 12), (14, 8)]
    for i in tupla:
        arbol.insertar(i)
    nodos = arbol.recorrido_anchura()

    print(nodos)
