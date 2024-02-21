# Darwin Conection

Todos sabemos que WhatsApp habilito la creacion de Bots de respuesta automatica a todos! Este programa utiliza una conexion API con la empresa que nos brinda el Bot (Evoltis, evoltis.com) y utilizando Pandas y PowerBi, procesamos metricas cruciales y mostramos el flujo de los clientes en el menu del Bot...

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
![Texto alternativo](src/Flujo_menu.png)
Luego tambien tenemos que tener en cuenta que los numeros que se veran naturalmente son un recuento por conversacion, no por cliente.

- ***Pestaña Principal:***
  - **Menu Principal:** Es un recuento de la primera opcion del menu elegida por el cliente, una vez ingresado a este.
  - **Menu Secundario:** Es un recuento de la segunda opcion del menu elegida por el cliente, una vez ingresado una opcion correcta en el menu principal.
  - **Modalidades de Finalizacion del Bot:** Aqui vemos como finalizaron la conversacion con las siguientes opciones:
    - *Derivados Bot:* Son los que siguieron un flujo natural del menu y fueron derivados.
    - *Resueltos x Sistema:* Son los que siguieron un flujo natural del menu y fueron resueltos por sistema.
    - *Abandonan:* Son los que no terminaron un flujo ya que dejaron de responderle al bot.
    - *Derivados Error:* Son los que enviaron tres opciones erroneas seguidas y por lo tanto fueron derivados.

- ***Pestaña Totales:***
  - **Inicios de Conversacion:** Es un recuento de la cantidad de conversaciones iniciadas en el bot.
  - **Ingresos al Menu Principal:** Es un recuento de la cantidad de conversaciones que llegan al Menu Principal.
  - **Ingresos Fallidos:** Es un recuento de la cantidad de conversacione que no llegaron al Menu Principal.
  - **Cantidad de Usuarios:** Es un recuento de la cantidad de usuarios que iniciaron una conversacion en el bot.
  - **Usuarios Recurrentes:** Es un recuento de la cantidad de inicios de conversacion que tuvo cada usuario.

- ***Pestaña FeedBack:***
  - **Encuesta Reclamo:** Se refiere a la encuesta que se hace una vez terminado algun flujo del menu donde se consulta si su reclamo fue resuelto.
  - **Encuesta Satisfaccion:** Se refiere a la encuesta que se hace una vez respondido que si en la Encuesta Reclamo, donde se pregunta cual fue la satisfaccion del cliente.
  - **Usuarios:** Es un recuento de encuestas hechas por cada usuario.

- ***Pestaña Otras Consultas:***
  - **Cantidad de Otras Consultas:** Recuento de Otras Consultas que fueron realizadas.
  - **Clasificacion de Otras Consultas:** Es una clasificacion de las Otras Consultas realizadas segun filtros de palabras clave.
  - **Mensajes:** Aqui se muestran puntualmente las otras consultas realizadas y el usuario que las realizo.
  
