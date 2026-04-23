# 🧩 Solución de Laberintos con Algoritmo A*

Implementación del algoritmo de búsqueda A* (A-estrella) para encontrar la ruta óptima en laberintos 2D.
Para la materia de Inteligencia Artificial 8vo Semestre

## Descripción

Este proyecto resuelve laberintos generados proceduralmente utilizando el algoritmo **A***, una técnica de búsqueda informada que encuentra el camino más corto entre dos puntos mediante una función heurística (en este caso, distancia Manhattan).

El sistema incluye:
- Generación aleatoria de laberintos con obstáculos
- Búsqueda del camino óptimo desde el inicio hasta la meta
- Visualización ASCII del laberinto y la ruta encontrada
- Componente de Perceptrón (opcional) para aprendizaje de características

## 📊 Algoritmo A*

El algoritmo A* evalúa cada nodo mediante la función:
```
f(n) = g(n) + h(n)
```
- **g(n)**: Costo real desde el inicio hasta el nodo actual
- **h(n)**: Heurística estimada (distancia Manhattan) al objetivo

### Ventajas de A*:
- Garantiza encontrar el camino más corto (si la heurística es admisible)
- Más eficiente que Dijkstra (usa heurística para guiar la búsqueda)
- Óptimo y completo

## 🗺️ Estructura del Laberinto

| Símbolo | Significado |
|---------|-------------|
| `I`     | Inicio (posición 0,0) |
| `F`     | Meta (esquina inferior derecha) |
| `*`     | Camino encontrado |
| `█`     | Obstáculo (pared) |
| `·`     | Espacio libre |

### Características:
- Dimensiones configurables (por defecto 10x10)
- 25% de celdas son obstáculos
- Inicio siempre en (0,0)
- Meta siempre en (filas-1, columnas-1)
- Movimientos permitidos: arriba, abajo, izquierda, derecha

## 🔧 Instalación y Ejecución

### Requisitos:
```bash
Python 3.7+ (solo bibliotecas estándar)
```

### Ejecutar:
```bash
python main.py
```

### Salida esperada:
```
Búsqueda A*
==============================

Laberinto 10 x 10 I -> Inicio  F -> Meta █ -> Obstáculo

  I · · · · · · · · ·
  · · █ · · · · · · ·
  · · █ · █ █ · · · ·
  · · · · █ · · · · ·
  · · · · · · · █ · ·
  · · · · · · · · · ·
  · █ · · · · · · · ·
  · · · █ · · · · · ·
  · · · · · · · █ · ·
  · · · · · · · · · F

====================
A* pura: 
====================
Longitud del camino es: 19 nodos

  I * * * · · · · · ·
  · · █ * · · · · · ·
  · · █ * █ █ · · · ·
  · · · * █ * * * · ·
  · · · * * * · █ * ·
  · · · · · · · · * ·
  · █ · · · · · · * ·
  · · · █ · · · · * ·
  · · · · · · · █ * ·
  · · · · · · · · · F
```

## 📖 Uso Personalizado

### Crear laberinto diferente:
```python
from laberinto import Laberinto
from pathfinding import a_estrella

# Laberinto 15x15 con semilla específica
laberinto = Laberinto(filas=15, cols=15, semilla=42)

# Encontrar camino
inicio = (0, 0)
meta = (14, 14)
camino = a_estrella(laberinto, inicio, meta)

# Visualizar
laberinto.imprimir(camino, inicio, meta)
```

### Modificar densidad de obstáculos:
Edita el método `_generar()` en la clase `Laberinto`:
```python
if random.random() < 0.25:  # Cambia 0.25 por otro valor (ej. 0.4 para 40% obstáculos)
    grid[r][c] = 1
```

### Cambiar heurística:
```python
# Distancia Euclidiana
def heuristica_euclidiana(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

# Distancia Chebyshev
def heuristica_chebyshev(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))
```

## 🧠 Versión con Perceptrón (Opcional)

El proyecto incluye una extensión que entrena un perceptrón para predecir celdas prometedoras, mejorando la heurística:

```python
# Entrenar perceptrón con rutas exitosas
X, y = generar_datos_entrenamiento(laberinto, n_rutas=30)
perceptron = Perceptron(n_features=4, lr=0.1)
perceptron.train(X, y, generaciones=50)

# Usar A* con heurística aprendida
camino_hibrido = a_estrella(laberinto, inicio, meta, 
                            perceptron=perceptron, 
                            peso_aprendido=0.3)
```


## 🔬 Casos de Prueba

### Laberinto sin solución:
Si no hay camino posible (inicio bloqueado por obstáculos), el algoritmo retorna `[]`:
```
Sin Solución :()
```

### Laberinto completamente libre:
El camino óptimo será una línea recta (solo derecha y abajo).


## 📚 Referencias

- [A* Search Algorithm - Wikipedia](https://en.wikipedia.org/wiki/A*_search_algorithm)
- [Introduction to A* - Stanford CS](http://theory.stanford.edu/~amitp/GameProgramming/)
- [Distance Metrics](https://en.wikipedia.org/wiki/Taxicab_geometry)

## 📄 Licencia

MIT License - Libre para uso educativo y de investigación.

---

**Desarrollado como demostración del algoritmo A* para resolución de laberintos**
```