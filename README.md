# Mesa con mecanismo de tijera: fuerzas y simulación

Programa en Python que calcula las fuerzas de una mesa elevadora de tijera (Modelo 1) con una caja encima y **simula en un GIF** qué pasa cuando la tijera sube hasta un ángulo θ. Si la mesa se inclina demasiado, la caja se desliza o se voltea y se cae.

![Simulación con θ = 85°: la caja se desliza y se cae](ejemplos/simulacion_theta85.gif)

## Índice

1. [Qué hace](#qué-hace)
2. [Estructura del repo](#estructura-del-repo)
3. [Requisitos e instalación](#requisitos-e-instalación)
4. [Cómo correrlo](#cómo-correrlo)
5. [Datos de entrada](#datos-de-entrada)
6. [Casos de ejemplo](#casos-de-ejemplo)
7. [Cómo probar tus propios casos](#cómo-probar-tus-propios-casos)
8. [Qué calcula (modelo)](#qué-calcula-modelo)
9. [Archivos que genera](#archivos-que-genera)
10. [Problemas comunes](#problemas-comunes)

## Qué hace

- Pide los datos de entrada (o los toma de los argumentos) y calcula todas las fuerzas por equilibrio estático.
- Imprime en consola las fuerzas y a partir de qué θ la caja se desliza o se voltea.
- Genera un GIF donde la tijera sube desde la mesa horizontal hasta el θ que pusiste, con α, el estado de la caja y las fuerzas en vivo.
- Si la caja se desliza o se voltea, se sale de la mesa y cae. Mientras se mueve, el panel avisa que ya no hay equilibrio estático.
- Guarda una tabla de barrido (`barrido_tijera.csv`) y una gráfica de la fuerza en los eslabones (`graficas_tijera.png`).

## Estructura del repo

```
tijera-fuerzas-/
├── tijera_fuerzas.py       # el programa
├── requirements.txt        # dependencias (matplotlib, pillow)
├── README.md
├── simulacion_tijera.gif   # GIF del último run (se sobrescribe)
├── graficas_tijera.png     # gráfica F1 vs θ (se sobrescribe)
├── barrido_tijera.csv      # tabla de barrido (se sobrescribe)
└── ejemplos/               # GIFs y salidas de consola de casos de ejemplo
```

## Requisitos e instalación

Necesitas **Python 3.9 o superior** y dos librerías: `matplotlib` (dibuja y anima) y `pillow` (guarda el GIF).

### 1. Revisa si tienes Python

Abre una terminal (en Mac: Terminal; en Windows: PowerShell o CMD) y corre:

```bash
python3 --version      # Mac / Linux
python --version       # Windows
```

Si no te sale una versión 3.9 o mayor, instálalo desde <https://www.python.org/downloads/>. En Windows marca la casilla **"Add Python to PATH"** durante la instalación.

### 2. Descarga el repo

```bash
git clone https://github.com/m2galindo/tijera-fuerzas-.git
cd tijera-fuerzas-
```

Si no usas git, en GitHub dale a **Code → Download ZIP**, descomprime y entra a la carpeta desde la terminal con `cd`.

### 3. Instala las dependencias

Se recomienda un entorno virtual para no mezclar librerías con las de tu sistema:

```bash
# crear el entorno (una sola vez)
python3 -m venv .venv

# activarlo (cada vez que abras una terminal nueva)
source .venv/bin/activate          # Mac / Linux
.venv\Scripts\activate             # Windows

# instalar
pip install -r requirements.txt
```

Sin entorno virtual también funciona:

```bash
pip install matplotlib pillow
```

### 4. Verifica la instalación

```bash
python3 -c "import matplotlib, PIL; print('OK')"
```

Debe imprimir `OK`. Si marca `ModuleNotFoundError`, repite el paso 3 con el entorno activado.

## Cómo correrlo

Siempre desde la carpeta del repo. En Windows usa `python` en lugar de `python3`.

### Modo interactivo

```bash
python3 tijera_fuerzas.py
```

Te pregunta uno por uno m, θ, L, a, b, c, h, y_A, y_H y μk. Con **Enter** usa el valor por defecto que aparece entre corchetes. Acepta coma o punto decimal.

### Modo directo (con argumentos)

No pregunta nada. Los datos que no pongas usan su valor por defecto.

```bash
python3 tijera_fuerzas.py --m 40 --theta 85
python3 tijera_fuerzas.py --m 20 --theta 60 --mu_k 0.5
```

### Qué pasa al correr

1. Imprime los datos de entrada y las fuerzas con la mesa horizontal y con tu ángulo.
2. Imprime a partir de qué θ la caja se desliza o se voltea y el veredicto.
3. Guarda el CSV y la gráfica.
4. Genera `simulacion_tijera.gif` (tarda unos segundos).

> **Importante:** cada corrida **sobrescribe** `simulacion_tijera.gif`, `graficas_tijera.png` y `barrido_tijera.csv`. Si quieres conservar uno, cámbiale el nombre o muévelo antes de volver a correr:
> ```bash
> mv simulacion_tijera.gif ejemplos/mi_caso.gif
> ```

> Si corres sin pantalla (servidor, SSH) usa `MPLBACKEND=Agg python3 tijera_fuerzas.py --theta 85`.

## Datos de entrada

| Argumento | Descripción | Por defecto |
|---|---|---|
| `--m` | Masa de la caja (máx. 40 kg) | 40 kg |
| `--theta` | Ángulo de los brazos de la tijera con la horizontal, θ (0° a 90°) | 50° |
| `--L` | Largo de cada eslabón corto de la tijera | 0.12 m |
| `--a` | Distancia del apoyo G al borde de la caja | 0.20 m |
| `--b` | Base de la caja (≤ 0.40 m) | 0.35 m |
| `--c` | Distancia del borde de la caja al poste H | 0.20 m |
| `--h` | Altura de la caja (≤ 0.30 m) | 0.25 m |
| `--y_A` | Altura del perno A (base de la tijera) | 0.25 m |
| `--y_H` | Altura del perno H (poste fijo) | 0.45 m |
| `--mu_k` | Coeficiente de fricción cinética caja-mesa | 0.35 |

La longitud total de la mesa se calcula sola: `d = a + b + c`. Unidades: longitudes en m, fuerzas en N, ángulos en grados.

## Casos de ejemplo

Con los datos por defecto, la mesa queda horizontal con θ = 24.62°. La caja **se desliza** con α > 19.29° (θ > 68.88°) y **se voltearía** con α > 54.46°, ángulo al que la tijera no llega.

### Caso 1: θ = 50°, la caja se queda en su lugar

```bash
python3 tijera_fuerzas.py --theta 50
```

![θ = 50°](ejemplos/simulacion_theta50.gif)

Salida completa: [`ejemplos/salida_theta50.txt`](ejemplos/salida_theta50.txt).

### Caso 2: θ = 85°, la caja se desliza y se cae

```bash
python3 tijera_fuerzas.py --theta 85
```

![θ = 85°](ejemplos/simulacion_theta85.gif)

| α | N | f | G_y | H_y | F1 | T |
|---|---|---|---|---|---|---|
| 21.77° | 364.4 N | 145.5 N | 170.1 N | 222.3 N | 85.4 N | 29.8 N |

Como α = 21.77° > 19.29°, la caja se desliza hasta salirse de la mesa. Salida completa: [`ejemplos/salida_theta85.txt`](ejemplos/salida_theta85.txt).

### Caso 3: caja alta y angosta, se voltea

```bash
python3 tijera_fuerzas.py --theta 85 --b 0.1 --h 0.3
```

![Caja que se voltea](ejemplos/simulacion_volteo.gif)

Aquí `b/h = 0.33 < μk = 0.35`, así que la caja se voltea sobre su esquina antes de deslizarse. Salida completa: [`ejemplos/salida_volteo.txt`](ejemplos/salida_volteo.txt).

### Caso 4: más fricción, la caja ya no se desliza

```bash
python3 tijera_fuerzas.py --theta 85 --mu_k 0.6
```

![μk = 0.6](ejemplos/simulacion_mu06.gif)

Con μk = 0.6 el límite de deslizamiento sube a α > 30.96°. El mismo θ = 85° que en el caso 2 ahora da α = 21.77° y la caja se queda en su lugar.

### Caso 5: menos masa y ángulo medio

```bash
python3 tijera_fuerzas.py --m 20 --theta 60
```

Resultado en consola: α = 16.71°, N = 187.9 N, f = 56.4 N, F1 = 51.0 N. Como α < 19.29° la caja se queda en su lugar.

### Caso 6: ángulo imposible

```bash
python3 tijera_fuerzas.py --theta 120
```

```
ERROR: con θ = 120.0° la tijera no puede armar la mesa con estas medidas.
Prueba otro ángulo (0° < θ < 90°) o revisa L, y_A, y_H y d.
```

El programa avisa y termina sin generar archivos.

## Cómo probar tus propios casos

1. Elige qué quieres cambiar: masa, ángulo, medidas de la caja o fricción.
2. Corre el programa con los argumentos correspondientes, por ejemplo:
   ```bash
   python3 tijera_fuerzas.py --m 30 --theta 70 --b 0.25 --h 0.30 --mu_k 0.4
   ```
3. Lee en consola la última línea que empieza con `>>`: te dice si la caja se queda, se desliza o se voltea.
4. Abre `simulacion_tijera.gif` para ver el movimiento (arrástralo a un navegador o ábrelo con tu visor de imágenes).
5. Guarda el GIF con otro nombre si quieres conservarlo.

Reglas para elegir datos:
- Para ver **deslizamiento**: sube θ por encima de la θ crítica que imprime el programa, o baja μk.
- Para ver **volteo**: usa una caja alta y angosta con `b/h < μk` (por ejemplo `--b 0.1 --h 0.3`).
- Para que la caja **se quede**: baja θ o sube μk.
- Si el programa dice que θ no es posible, prueba otro ángulo o revisa L, y_A, y_H y d (el ángulo máximo depende de la geometría).

## Qué calcula (modelo)

Con la masa m y el ángulo θ obtiene, por equilibrio estático:

| Variable | Qué es |
|---|---|
| α | Inclinación de la mesa: `sin α = (y_A + 4·L·sin θ − y_H) / d` |
| N, f | Fuerza normal y fuerza de fricción sobre la caja |
| G_y, H_y | Reacciones en los apoyos de la mesa (ΣM_H = 0 y ΣF_y = 0) |
| F1 | Compresión en los eslabones de la tijera: `G_y / (2 sin θ)` |
| T (= C_x) | Tensión en el tornillo B–D: `2·G_y / tan θ` |
| A_y | Reacción vertical en el perno A |

Criterios para la caja:
- **Se desliza** si `tan α > μk`.
- **Se voltea** si `tan α > b/h`.
- Si `b/h < μk`, se voltea antes de deslizarse.

La fuerza que aplica el usuario en la manivela produce T y fija θ. Su valor depende de la rosca y no se calcula aquí. T se imprime en consola y se guarda en el CSV, pero ya no se grafica.

## Archivos que genera

| Archivo | Contenido |
|---|---|
| `simulacion_tijera.gif` | Animación: la tijera sube y la caja se queda, se desliza, se voltea o cae. Panel con datos de entrada, θ, α, estado y fuerzas |
| `graficas_tijera.png` | Fuerza en los eslabones F1 contra θ para m = 10, 20, 30 y 40 kg |
| `barrido_tijera.csv` | Todas las fuerzas para m = 10, 20, 30, 40 kg y θ = 5° a 85° cada 5° |

![Fuerza en los eslabones F1 contra θ](graficas_tijera.png)

## Problemas comunes

| Problema | Solución |
|---|---|
| `python3: command not found` (Windows) | Usa `python` en lugar de `python3` |
| `ModuleNotFoundError: No module named 'matplotlib'` | Activa el entorno virtual y corre `pip install -r requirements.txt` |
| `pip: command not found` | Usa `python3 -m pip install -r requirements.txt` |
| `error: externally-managed-environment` | Usa un entorno virtual (paso 3 de la instalación) |
| `ERROR: ... la tijera no puede armar la mesa` | Elige otro θ entre 0° y 90° o revisa L, y_A, y_H y d |
| El GIF no cambió | Se sobrescribe en cada corrida; revisa que corriste en la carpeta correcta |
| Decimales con coma en argumentos | En argumentos usa punto (`--mu_k 0.4`); en modo interactivo se acepta coma |
