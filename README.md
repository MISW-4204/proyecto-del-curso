# Proyecto del curso - Entrega 1

## Descripción

Este es el proyecto del curso para Desarrollo de Software en Nube(MISW 4204). Está compuesto por una aplicación de FastAPI que permite convertir archivos de un formato a otro. La aplicación de FastAPI se comunica con una base de datos Postgres para almacenar los archivos convertidos y con una cola de tareas de Celery para procesar las tareas de conversión.

## Tabla de contenido

- [Proyecto del curso - Entrega 1](#proyecto-del-curso---entrega-1)
  - [Descripción](#descripción)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Prerrequisitos](#prerrequisitos)
  - [Estrucutra del proyecto](#estrucutra-del-proyecto)
    - [Estructura de carpetas](#estructura-de-carpetas)
    - [Estructura de archivos](#estructura-de-archivos)
  - [Ejecución del proyecto](#ejecución-del-proyecto)
  - [Ejecución local del proyecto](#ejecución-local-del-proyecto)
    - [Creación de entorno virtual](#creación-de-entorno-virtual)
    - [Activar entorno virtual](#activar-entorno-virtual)
      - [Windows](#windows)
      - [Mac](#mac)
    - [Variables de entorno](#variables-de-entorno)
    - [Ejecución de la aplicación de FastAPI](#ejecución-de-la-aplicación-de-fastapi)
    - [Ejecución de la aplicación de Celery](#ejecución-de-la-aplicación-de-celery)

## Prerrequisitos

- Python 3.11
- Docker
- Docker Compose
- Postgres
- Redis

## Estrucutra del proyecto

### Estructura de carpetas

El proyecto está estructurado de la siguiente manera:

- **.vscode**: Contiene la configuración de VSCode para el proyecto.
- **converter_app**: Contiene el código fuente de la API de la aplicación de conversión.
- **tasks**: Contiene el código fuente de las tareas de Celery para la aplicación de conversión.

### Estructura de archivos

- **.gitignore**: Contiene los archivos y carpetas que se ignoran para subir al repositorio.
- **docker-compose.yml**: Contiene la configuración de Docker Compose para el proyecto.
- **nginx.conf**: Contiene la configuración de Nginx para el proyecto.
- **README.md**: Contiene la documentación del proyecto.

## Ejecución del proyecto

Para ejecutar el proyecto localmente se debe ejecutar el siguiente comando:

```bash
docker-compose up --build
```

## Ejecución local del proyecto

Para ejecutar el proyecto localmente se debe dirigir a la carpeta `converter_app`. Desde allí debe crear un entorno virtual.

### Creación de entorno virtual

```bash
python -m venv env
```

### Activar entorno virtual

#### Windows

```bash
env\Scripts\activate
```

#### Mac

```bash
source env/bin/activate
```

Una vez activado el entorno virtual, se debe instalar las dependencias del proyecto.

```bash
pip install -r requirements.txt
```

Para salir del entorno virtual ejecute el siguiente comando:

```bash
deactivate
```

### Variables de entorno

La aplicación de FastAPI utiliza las siguientes variables de entorno:

- **DB_NAME**: Nombre de la base de datos.
- **DB_USER**: Usuario de la base de datos.
- **DB_PASSWORD**: Contraseña de la base de datos.
- **DB_HOST**: Host de la base de datos.
- **DB_PORT**: Puerto de la base de datos.
- **JWT_ALGORITHM**: Algoritmo de encriptación de JWT.
- **JWT_SECRET_KEY**: Llave secreta de JWT.
- **JWT_TYPE**: Tipo de JWT.
- **JWT_NAME**: Nombre del JWT.
- **CELERY_QUEUE**: Nombre de la cola de tareas de Celery.

La aplicación de Celery utiliza las siguientes variables de entorno:

- **REDIS_HOST**: Host de Redis.
- **REDIS_PORT**: Puerto de Redis.

Si se desea correr la aplicación de forma local, se debe crear un archivo `.env` en la carpeta `converter_app` y `tasks` con las variables de entorno mencionadas anteriormente.

### Ejecución de la aplicación de FastAPI

Para ejecutar la aplicación de FastAPI debe ejecutar el siguiente comando:

```bash
cd converter_app
uvicorn src.main:app --reload
```

### Ejecución de la aplicación de Celery

Para ejecutar la aplicación de Celery debe ejecutar el siguiente comando:

```bash
cd tasks
celery -A convertions worker -l info -Q convertions
```
