import bcrypt

def evaluar_clave(clave, hash_clave):
    clave_descifrada = clave.encode("utf-8")
    resultado = bcrypt.checkpw(clave_descifrada, hash_clave)
    return resultado