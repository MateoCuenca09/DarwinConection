# Darwin Conection

Esta librería Python es parte esencial de un emocionante proyecto que simplifica la gestión y el análisis del flujo de clientes en el menú de Darwin.
El proyecto automatiza la descarga de una base de datos, calcula métricas cruciales y almacena los resultados en un archivo histórico.xlsx.
Lo mejor de todo es que este proceso se ejecuta de forma automática todos los días.

## Tabla de Contenidos

- [Darwin Conection](#darwin-conection)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Acerca del Proyecto](#acerca-del-proyecto)
  - [Instalación](#instalación)
  - [Manual de Usuario](#manual-de-usuario)
    - [Categoria de Datos](#categoria-de-datos)

## Acerca del Proyecto

Este proyecto esta programado en Python 3 y utiliza esencialmente la libreria Pandas (v.1.5.3), corre en Windows 10 y la version instalada en el server debe contar con acceso a las carpetas donde se quiera guardar el archivo Historico.xlsx y el TableroDarwin.pbix

## Instalación

Para instalar este proyecto, primero conseguimos el proyecto descargandolo de la web de GitHub, luego instalamos las dependencias/librerias necesarias o bien,

```bash
# Descargar el proyecto
git clone https://github.com/MateoCuenca09/DarwinConection.git
cd MateoCuenca09
npm install
# Instalar las dependencias
pip install pandas, datatime, unidecode, schedule, time, requests
```

Por las dudas que falle, aqui dejo las versiones de las librerias que yo utilice:

- requests 2.28.2
- unidecode 1.3.6
- pandas 1.5.3
- schedule 1.2.0

## Manual de Usuario

- *Carga de Datos*: El programa descarga los datos automáticamente todos los días a las 20hs, mediante la API brindada por la empresa de Darwin.

- *Visualización de Datos POWER BI*: El programa genera un excel en la carpeta “O:\Gestion y Experiencia del Cliente\5. SERVICIO DE ATENCIÓN AL CLIENTE\11. TRANSFORMACIÓN DIGITAL\ReportesDarwin\PBI” con el nombre de Historico.xlsx que es la tabla de datos que toma el archivo TableroDarwin.pbix. Esta tabla es acumulativa por dos meses, cuando un dato supera este tiempo es guardado en un archivo aparte junto con los archivos cercanos a el en un plazo de dos meses, con el nombre de los meses correspondientes.
  
- *POWER BI*: Cada vez que se quiera ver datos nuevos, se debe actualizar el tablero pulsando el boton 'actualizar' que se encuentra el la barra horizontal superior. El archivo queda publicado online la primera vez, luego si es solicitado o querido se puede actualizar el online dando click al botón de publicar que se encuentra en la barra superior en el extremo derecho. Que se encuentre online permite que lo vean distintas personas sin problemas.

### Categoria de Datos

Para entender las clasificaciones de los clientes en el menu, primero se debe entender el siguiente flujo del menu de Darwin:
![Texto alternativo](Flujo_menu.png)
Luego tambien tenemos que tener en cuenta que los numeros que se veran naturalmente son un recuento por conversacion, no por cliente.

- Pestaña Principal:
  - *Menu Principal:* Es un recuento de la primera opcion del menu elegida por el cliente, una vez ingresado a este.
  - *Menu Secundario:* Es un recuento de la segunda opcion del menu elegida por el cliente, una vez ingresado una opcion correcta en el menu principal.
  - **Modalidades de Finalizacion del Bot:** Aqui vemos como finalizaron la conversacion con las siguientes opciones.
    - Derivados Bot:
    - Resueltos x Sistema:
    - Abandonan:
    - Derivados Error:

- Pestaña Totales:
  - Inicios de Conversacion:
  - Ingresos al Menu Principal:
  - Ingresos Fallidos:
  - Cantidad de Usuarios:
  - Usuarios Recurrentes:

- Pestaña FeedBack:
  - Encuesta Reclamo:
  - Encuesta Satisfaccion:
  - Usuarios:

- Pestaña Otras Consultas:
  - Cantidad de Otras Consultas:
  - Clasificacion de Otras Consultas:
  - Mensajes:
  