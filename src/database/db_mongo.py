from pymongo import MongoClient
from src.helpers.funciones import genera_colmena_id

client = MongoClient("mongodb://localhost:27017/")
db = client["monitorBeehive"]

# Agrega un nuevo apicultor.
def add_apicultor(datos):
    coleccion = db["apicultor"]
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna un apicultor por su RUT y password.
def get_apicultor(rut, password):
    coleccion = db["apicultor"]
    apicultor = coleccion.find_one({"rut": rut, "password": password})
    return apicultor

# Retorna todos los apicultores.
def get_apicultores():
    coleccion = db["apicultor"]
    apicultores = list(coleccion.find())
    return apicultores

# Hacer rutas parar ingresar colmenas y cargar colmenas.
def add_colmena(datos):
    coleccion = db["colmena"]
    datos["colmena_id"] = genera_colmena_id()
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

def get_colmenas():
    coleccion = db["colmena"]
    colmenas = list(coleccion.find())
    return colmenas

# Retorna las colmenas a partir del id del apicultor.
def get_colmena_by_id(apicultor_id):
    coleccion = db["colmena"]
    colmena = list(coleccion.find({"id_apicultor": apicultor_id}))
    return colmena

# Retorna el id de la última colmena ingresada.
def get_id_ultima_colmena():
    coleccion = db["colmena"]
    ultima_colmena = coleccion.find().sort("colmena_id", -1).limit(1)
    return ultima_colmena[0]["colmena_id"]

# Ingresa datos de sensores a una colmena.
def add_datos_sensores(datos):
    coleccion = db["sensores"]
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

# Retorna los datos de sensores de una colmena.
def get_datos_sensores(colmena_id):
    coleccion = db["sensores"]
    print(type(colmena_id))
    datos_sensores = list(coleccion.find({"colmena_id": colmena_id}))
    return datos_sensores
