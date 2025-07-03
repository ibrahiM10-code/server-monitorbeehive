from pymongo import MongoClient
import pprint

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
    resultado = coleccion.insert_one(datos)
    return resultado.inserted_id

def get_colmenas():
    coleccion = db["colmena"]
    colmenas = list(coleccion.find())
    return colmenas

def get_colmena_by_id(apicultor_id):
    coleccion = db["colmena"]
    colmena = list(coleccion.find({"id_apicultor": apicultor_id}))
    return colmena
# Carga en la base de datos datos de sensores, alertas y reportes.