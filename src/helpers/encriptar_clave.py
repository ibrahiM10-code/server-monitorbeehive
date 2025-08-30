import bcrypt

def encriptar_clave(clave):
    bytes_array = clave.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_clave = bcrypt.hashpw(bytes_array, salt)
    return hash_clave
