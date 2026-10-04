# MonitorBeehive API

API backend para monitorear colmenas y gestionar la información de apicultores, sensores, alertas y reportes. Está construida con Flask y MongoDB.

This is the backend API for monitoring beehives and managing beekeeper, sensor, alert, and report data. It is built with Flask and MongoDB.

## Idioma / Language

- [Español](#español)
- [English](#english)

---

## Español

### Funcionalidades

- Registro e inicio de sesión de apicultores y administradores.
- Gestión de colmenas y asociación de placas Raspberry Pi mediante su número de serie.
- Consulta y actualización de datos e historial de sensores.
- Gestión de alertas y umbrales.
- Generación y descarga de reportes PDF y exportación del historial a CSV.
- Recuperación de contraseña por correo y registro de tokens Expo Push.

### Tecnologías

- Python y Flask
- MongoDB Atlas con PyMongo
- JWT para autenticación
- SMTP para correos de recuperación de contraseña
- FPDF para generar documentos PDF

### Requisitos

- Python 3.12 o posterior.
- Una instancia de MongoDB accesible por la aplicación.
- Credenciales SMTP si se necesita habilitar la recuperación de contraseña por correo.

### Instalación y ejecución

En Windows PowerShell:

```powershell
git clone https://github.com/ibrahiM10-code/server-monitorbeehive.git
cd server-monitorbeehive
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

En macOS o Linux:

```bash
git clone https://github.com/ibrahiM10-code/server-monitorbeehive.git
cd server-monitorbeehive
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz del proyecto:

```dotenv
MONGODB_ATLAS_CONNECTION=mongodb+srv://<usuario>:<password>@<cluster>/
MONGODB_ATLAS_DBNAME=<nombre_de_base_de_datos>
JWT_SECRET=<secreto_largo_y_aleatorio>

# Requerido solo para enviar correos de recuperación de contraseña
SMTP_SERVER=<servidor_smtp>
CORREO_DE_ENVIO=<cuenta_de_correo>
PASSWORD_CORREO_DE_ENVIO=<clave_o_contrasena_de_aplicacion>
```

No compartas ni subas el archivo `.env` ni sus credenciales al control de versiones. La aplicación carga estas variables al iniciar.

Inicia el servidor de desarrollo:

```bash
python run.py
```

La API queda disponible en `http://localhost:5000`. El servidor se inicia en modo de depuración; no uses `python run.py` como servidor de producción. Configura un servidor WSGI y valores seguros para producción.

### Rutas principales

Las rutas se agrupan bajo estas bases (no hay un prefijo `/api`):

| Base        | Uso                                                                                |
| ----------- | ---------------------------------------------------------------------------------- |
| `/auth`     | Registro, inicio de sesión, recuperación de contraseña y token Expo Push           |
| `/colmenas` | Crear, consultar, actualizar y eliminar colmenas                                   |
| `/sensores` | Consultar datos actuales e historial, y actualizar sensores                        |
| `/alertas`  | Crear, consultar y actualizar alertas                                              |
| `/umbrales` | Crear, consultar y actualizar umbrales                                             |
| `/reportes` | Generar, filtrar y descargar reportes PDF o CSV; consultar descripciones de estado |
| `/rpi`      | Registrar/asignar una placa Raspberry Pi a una colmena                             |

Las rutas concretas y sus métodos HTTP están definidas en `src/routes/`. Las rutas que requieren autenticación esperan el JWT en el encabezado `Authorization` usando el esquema `Bearer`.

### Estructura del proyecto

```text
.
├── run.py                  # Punto de entrada de Flask
├── requirements.txt        # Dependencias de Python
├── src/
│   ├── __init__.py         # Creación de la aplicación y registro de blueprints
│   ├── config.py           # Configuración de Flask
│   ├── database/           # Acceso a MongoDB
│   ├── helpers/            # Lógica de sensores, alertas, correo y PDF
│   ├── routes/             # Endpoints HTTP
│   └── utils/               # Gestión de tokens
└── static/                 # Recursos estáticos
```

---

## English

### Features

- Sign-up and login for beekeepers and administrators.
- Beehive management and Raspberry Pi board assignment by device serial number.
- Sensor readings and history retrieval and updates.
- Alert and threshold management.
- PDF report generation/download and CSV sensor-history export.
- Password recovery by email and Expo Push token registration.

### Tech stack

- Python and Flask
- MongoDB Atlas with PyMongo
- JWT authentication
- SMTP for password-recovery emails
- FPDF for PDF generation

### Requirements

- Python 3.12 or later.
- A MongoDB instance reachable by the application.
- SMTP credentials if password-recovery emails are required.

### Installation and running

On Windows PowerShell:

```powershell
git clone https://github.com/ibrahiM10-code/server-monitorbeehive.git
cd server-monitorbeehive
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
git clone https://github.com/ibrahiM10-code/server-monitorbeehive.git
cd server-monitorbeehive
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
MONGODB_ATLAS_CONNECTION=mongodb+srv://<username>:<password>@<cluster>/
MONGODB_ATLAS_DBNAME=<database_name>
JWT_SECRET=<long_random_secret>

# Required only for password-recovery emails
SMTP_SERVER=<smtp_server>
CORREO_DE_ENVIO=<sender_email_account>
PASSWORD_CORREO_DE_ENVIO=<password_or_app_password>
```

Do not share or commit the `.env` file or its credentials. The application loads these variables at startup.

Start the development server:

```bash
python run.py
```

The API is available at `http://localhost:5000`. The development server runs with debugging enabled; do not use `python run.py` in production. Use a WSGI server and secure production settings.

### Main route groups

All routes are grouped under these base paths (there is no `/api` prefix):

| Base path   | Purpose                                                                         |
| ----------- | ------------------------------------------------------------------------------- |
| `/auth`     | Sign-up, login, password recovery, and Expo Push token registration             |
| `/colmenas` | Create, retrieve, update, and delete beehives                                   |
| `/sensores` | Retrieve current readings and history, and update sensor data                   |
| `/alertas`  | Create, retrieve, and update alerts                                             |
| `/umbrales` | Create, retrieve, and update thresholds                                         |
| `/reportes` | Generate, filter, and download PDF or CSV reports; retrieve status descriptions |
| `/rpi`      | Register/assign a Raspberry Pi board to a beehive                               |

Exact routes and HTTP methods are defined in `src/routes/`. Endpoints that require authentication expect the JWT in the `Authorization` header using the `Bearer` scheme.

### Project structure

```text
.
├── run.py                  # Flask entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py         # Application factory and blueprint registration
│   ├── config.py           # Flask configuration
│   ├── database/           # MongoDB access
│   ├── helpers/            # Sensor, alert, email, and PDF logic
│   ├── routes/             # HTTP endpoints
│   └── utils/               # Token management
└── static/                 # Static assets
```
