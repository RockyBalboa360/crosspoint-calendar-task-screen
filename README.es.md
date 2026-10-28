[English](README.md) · [Deutsch](README.de.md) · [Français](README.fr.md) · **Español**

# Pantalla de reposo con calendario para la Xteink X4 Pro

**Fork no oficial de [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader) 1.6.5.**
Tu Xteink X4 Pro muestra tu día como pantalla de reposo: el tiempo de dos lugares, los eventos de hoy de Google
Calendar y las tareas de hoy de Todoist.

<p align="center">
  <img src="docs/example-calendar-screen.png" alt="Ejemplo: tiempo de Berlín y Fráncfort, eventos y tareas (datos de muestra)" width="320"><br>
  <em>Imagen de ejemplo con datos de muestra, tal como aparece en la pantalla (480x800, escala de grises)</em>
</p>

> Proyecto no oficial. Sin relación con el proyecto CrossPoint Reader ni con Xteink.
> Probado en una sola X4 Pro, úsalo bajo tu propia responsabilidad, sin ninguna garantía.

**Dos partes que van juntas:**
- 🧩 **Firmware** (este repositorio): [crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/tree/feature/calendar-sleep-screen), **última versión: [Releases](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases/latest)**
- 🔌 **Alternativa sin firmware propio:** [plugin SD para el CrossPoint 2.0 oficial](https://github.com/RockyBalboa360/CrossPoint-SDPlugin-weather-calendar-task-screen)
- ☁️ **Servidor de imagen** (Cloudflare Worker): [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen)

## Cómo funciona
1. Un pequeño **servidor** (Cloudflare Worker) obtiene el tiempo, los eventos y las tareas y los dibuja en una imagen:
   [worker-for-crosspoint-calendar-task-screen](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen).
2. Este **firmware** añade una nueva pantalla de reposo **«Calendar»** y el ajuste **«Calendar Server URL»**.
3. Cuando el dispositivo se duerme, se conecta a tu WiFi guardada, descarga la imagen de esa URL y la muestra como
   pantalla de reposo. Si falla, se queda la última imagen descargada.

## Instalación
1. Descarga `firmware.bin` de la [última versión](https://github.com/RockyBalboa360/crosspoint-calendar-task-screen/releases/latest)
   y cópialo en la raíz de la tarjeta SD.
2. En el dispositivo: *Settings → System → SD Card Firmware Update*, elige el archivo y confirma.
   El firmware anterior se conserva en la segunda ranura de programa.
3. *Settings → System → WiFi Networks*: guarda tu WiFi.
4. *Settings → Display → Calendar Server URL*: introduce la dirección de tu worker
   (por ejemplo `https://tu-worker.tu-nombre.workers.dev`).
5. *Settings → Display → Sleep Screen → Calendar*.

La configuración del worker (cuenta de servicio de Google, token de Todoist, lugares) se describe en su
[README](https://github.com/RockyBalboa360/worker-for-crosspoint-calendar-task-screen#readme).
Los menús del dispositivo están en inglés o alemán; aquí se indican los nombres de los menús en inglés.

## ¿Primero eventos o tareas?
Los eventos y las tareas comparten el espacio bajo el tiempo. En *Settings → Display* decides quién lo recibe primero:

| *Calendar priority* | Efecto |
|---|---|
| *All events* | todos los eventos de hoy, las tareas reciben el resto |
| *Fixed events* | exactamente N eventos, las tareas reciben el resto (por defecto, N = 3) |
| *Fixed tasks* | exactamente N tareas, los eventos reciben el resto |
| *All tasks* | todas las tareas, los eventos reciben el resto |

*Fixed count* define N (de 1 a 8). Si no cabe todo, la sección termina con «+N weitere» («+N más», en alemán, porque el
worker está en alemán). Una sección vacía ocupa solo una línea.

<p align="center">
  <img src="docs/layout-priorities.png" alt="Los cuatro diseños: todos los eventos, eventos fijos, tareas fijas, todas las tareas" width="100%"><br>
  <em>Los cuatro diseños (de izquierda a derecha): todos los eventos, 2 eventos, 3 tareas, todas las tareas</em>
</p>

El firmware añade la elección a la URL del servidor como `?priority=…&count=…`. Para ello hace falta el worker
actualizado; un worker antiguo la ignora y mantiene su diseño fijo.

## Conviene saber
- La imagen se descarga **cuando el dispositivo se duerme**, manualmente o tras el tiempo de inactividad. Después se
  queda hasta que despiertes el dispositivo y lo dejes dormir de nuevo. No hay despertar programado.
- Con menos de **10 % de batería** el dispositivo no descarga nada. En su lugar muestra una imagen de «Batería baja»
  con el nivel de carga. Tras cargar, el calendario se actualiza la próxima vez que el dispositivo se duerma.
- Elige la **imagen de batería baja** en *Settings → Display → Low battery screen*: una galería con el icono de batería
  sencillo y **16 dibujos** (una batería clásica, 3 diseños futuristas de circuitos, 9 dibujos de cómic y 3 diseños
  steampunk). Desliza o usa las teclas laterales para navegar; los botones táctiles «Choose» y «Cancel» de la parte
  inferior aceptan la imagen mostrada o salen de la galería.
- La imagen debe ser un BMP de 480x800 píxeles. El worker entrega exactamente eso.
- La dirección de tu worker es pública. Quien la conozca puede ver tus eventos y tareas. No la compartas.
- Actualizar con «Check for updates» vuelve a sustituir este firmware por el oficial.

<p align="center">
  <img src="docs/lowbattery-screens.png" alt="Las 16 imágenes de batería baja" width="640"><br>
  <em>Las 16 imágenes de batería baja a elegir (bajo cada imagen el dispositivo muestra «Batería baja» y el nivel de carga)</em>
</p>

## Qué cambia respecto a CrossPoint 1.6.5
Son nuevos `src/network/CalendarFetcher.{h,cpp}` y pequeños cambios en `SleepActivity`, `SettingsActivity`, los
ajustes y las traducciones (inglés y alemán). Todo lo demás permanece igual. La lista exacta, las instrucciones de
compilación y todas las licencias están en [FORK_NOTICE.md](FORK_NOTICE.md). El manual original es
[USER_GUIDE.md](USER_GUIDE.md).

## Compilarlo tú mismo
```
git clone --recurse-submodules https://github.com/RockyBalboa360/crosspoint-calendar-task-screen
cd crosspoint-calendar-task-screen
git checkout feature/calendar-sleep-screen
pio run -e x4pro-gh_release
```
El archivo final queda en `.pio/build/x4pro-gh_release/firmware.bin`.

## Aspectos legales y fuentes
- Basado en **CrossPoint Reader** (MIT, Copyright (c) 2025 CrossPoint Reader organization). El archivo
  [LICENSE](LICENSE) no se ha modificado. Mis cambios también están bajo licencia MIT.
- El firmware incluye bibliotecas con sus propias licencias, entre ellas **wolfSSL (GPL-2.0 o posterior)** y
  arduinoWebSockets (LGPL-2.1). Los textos de las licencias están en [third_party_licenses/](third_party_licenses/),
  las fuentes y versiones en [FORK_NOTICE.md](FORK_NOTICE.md).
- «Xteink» y «CrossPoint» son nombres de sus respectivos titulares y aquí solo se usan de forma descriptiva.
- Los cambios se realizaron con la ayuda de Claude Code (Anthropic) y fueron revisados y publicados por el propietario
  del repositorio.

Proyecto original: <https://github.com/crosspoint-reader/crosspoint-reader>
