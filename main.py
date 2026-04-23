
import math 
import random
import heapq
from collections import defaultdict

class Perceptron:
    def ___init__(self, n_features:int, lr:float=0.1):
        # perceptron = x1*w1 + x2*w2 + bias
        
        # resultado = (perceptron) + lr
        self.lr = lr
        self.weights = [random.uniform(-0.5, 0.5) for _ in range(n_features)]
        self.bias = random.uniform(-0.5, 0.5)
        self.history = []
    def _activacion(self, z:float) -> int:
        return 1 if z >= 0 else 0
    
    def predict(self,x:list):
        z = sum( w * xi for w, xi in zip(self.weights,x)) + self.bias
        return self._activacion(z)
    
    def score(self, x:list):
        return sum( w * xi for w, xi in zip(self.weights,x)) + self.bias
    
    def train(self, X,y, generaciones = 50):
        for generacion in range(generaciones):
            errores = 0
            for xi,yi in zip(X,y):
                pred = self.predict(xi)
                error = yi - pred
                if error != 0:
                    errores +=1
                    self.weights = [
                         w + self.lr * error * xi for w, x in zip(self.weights, xi)
                        ]
                    self.bias += self.lr * error
                    self.history.append(errores)
                if errores == 0:
                    print(f"Convergio en generación: {generacion+1}")
                    break
            else:
                print(f"Entrenado en {generaciones} generaciones"
                      f"Errores Finales: {self.history[-1]}")
    def accuracy(self, X,y):
        correcto = sum(1 for xi,yi in zip(X,y) if self.predict(xi) == yi)
        return correcto/len(y) if y else 0.0
    
class Laberinto:
    def __init__(self, filas, cols, semilla=50):
        self.filas = filas
        self.cols = cols
        random.seed(semilla)
        self.grid = self._generar()
    def _generar(self):
        grid = [[0]*self.cols for _ in range(self.filas)]
        for r in range(self.filas):
            for c in range(self.cols):
                if random.random() < 0.25:
                    grid[r][c] = 1
        grid[0][0] = 0
        grid[self.filas-1][self.cols-1] = 0
        return grid
    
    def es_valido(self,r,c):
        return (
            0 <= r<self.filas and
            0 <= c<self.cols and
            self.grid[r][c] == 0
                )
    def vecinos(self, r,c):
        dirs = [(-1 , 0), (1 , 0), (0 , -1), (0 , 1)]
        return [(r + dr , c + dc ) for dr, dc in dirs if self.es_valido(r + dr, c + dc )]
    
    def densidad_local(self, r , c, radio = 2):
        total = obstaculos = 0

        for dr in range(-radio, radio+1):
            for dc in range(-radio, radio+1):
                nr, nc = r + dr, c + dc
                if 0 <= nr<self.filas and 0<=nc < self.cols:
                    total += 1
                    obstaculos += self.grid[nr][nc]
        return obstaculos / total if total else 0.0
    
    def imprimir(self, camino:list = None, inicio = (0,0), meta = None ):
        meta = meta or (self.filas-1, self.cols-1)
        camino_set = set(camino) if camino else set()

        simbolos = { 0:"·", 1:"█" }

        print()
        for r in range(self.filas):
            fila = ""
            for c in range(self.cols):
                pos = (r,c)
                if pos == inicio :
                    fila += " I"
                elif pos == meta:
                    fila += " F"
                elif pos in camino_set:
                    fila += " *"
                else:
                    fila += f" {simbolos[self.grid[r][c]]}"
            print(fila)
        print()

 # Heuristica #

def heuristica_manhattan( a , b ):
    return abs(a[0] - b[0] + abs(a[1] - b[1]))

def extraer_features(r: int, c: int, meta:tuple, laberinto: Laberinto):
    fr = r / (laberinto.filas -1)
    fc = c / (laberinto.cols -1)
    dist = heuristica_manhattan((r,c), meta)
    dis_norm = dist / ( laberinto.filas + laberinto.cols )
    dens = laberinto.densidad_local( r , c )
    return [fr, fc, dis_norm, dens]

def a_estrella(
        laberinto:Laberinto,
        inicio,
        meta, 
        perceptron = None,
        peso_aprendido=0.4,        
):
    """
    A* con Heuristica Hibrida:
    h(n) = (1-w) * manhattan( n , meta ) + w * penalizacion_perceptron
    """ 
    def h(nodo):
        h_base = heuristica_manhattan(nodo, meta)
        if perceptron is None:
            return h_base
        feats = extraer_features(nodo[0], nodo[1], meta, laberinto)
        penalizacion = perceptron.score(feats)
        h_aprendida = h_base + peso_aprendido * penalizacion

        return max (h_aprendida , 0)
    open_heap=[]
    heapq.heappush(open_heap,(h(inicio), 0, inicio))

    g_cost = defaultdict(lambda:math.inf)
    g_cost [inicio] = 0

    padre = {inicio:None}
    visitados = set()

    while open_heap:
        f , g, nodo = heapq.heappop(open_heap)
        if nodo in visitados:
            continue
        visitados.add(nodo)

        if nodo == meta:
            # Reconstruir nuestro camino
            camino = []
            while nodo is not None:
                camino.append(nodo)
                nodo = padre[nodo]
            return camino[::-1]
        for vecino in laberinto.vecinos(*nodo):
            nuevo_g = g + 1
            if nuevo_g < g_cost[vecino]:
                g_cost[vecino] = nuevo_g
                padre [vecino] = nodo
                h_nuevo = nuevo_g + h(vecino)   
                heapq.heappush(open_heap, (h_nuevo, nuevo_g, vecino))
    return [] # sin solucion

def generar_datos_entrenamiento(
        laberinto: Laberinto,
        n_rutas = 30
):
    X , y = [],[]
    meta = (laberinto.filas -1, laberinto.cols-1)
    for _ in range(n_rutas):
        r0 = random.randint(0 , laberinto.filas -1)
        c0 = random.randint(0 , laberinto.cols-1)
        if laberinto.grid[ r0 ][ c0 ] == 1:
            continue
        inicio = (r0,c0)
        camino = a_estrella(laberinto, inicio, meta)
        if not camino:
            continue
        camino_set = set(camino)
        for nodo in camino:
            X.append(extraer_features(nodo[0],nodo[1], meta, laberinto))
            y.append(1)
        libres = [
            (r , c )
            for r in range (laberinto.filas)
            for c in range (laberinto.cols)

            if laberinto.grid[r][c] == 0 and (r , c) not in camino_set
        ]
        muestra_neg = random.sample(libres, min(len(camino),len(libres)))
        for nodo in muestra_neg:
            X.append(extraer_features(nodo[0],nodo[1], meta, laberinto))
            y.append(0)
        return X,y
    
def main():
    print("Busqueda A*")
    print("="*30)
    FILAS , COLS = 30 , 30
    laberinto = Laberinto(FILAS,COLS, random.randint(3,100))
    inicio = (0,0)
    meta = (FILAS-1, COLS-1)

    print(f"\n\n Laberinto {FILAS} x {COLS} I -> Inicio  F -> Meta █ -> Obstaculo")
    laberinto.imprimir(inicio=inicio, meta=meta)

    print("="*20)
    print("A* pura: ")
    print("="*20)

    camino_puro = a_estrella(laberinto, inicio, meta, perceptron=None)
    if camino_puro :
        print(f"Longitud del camino es: {len(camino_puro)} nodos")
        laberinto.imprimir(camino_puro, inicio, meta)
    else:
        print(" Sin Solución :()")

if __name__ == "__main__":
    main() 