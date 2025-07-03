import jwt

class TokenManager:

    @classmethod
    def generar_token(cls, datos_apicultor):
        payload = {"id": str(datos_apicultor["_id"]), "rut": datos_apicultor["rut"]}
        token = jwt.encode(payload, "mi-secreto", algorithm="HS256")
        return token
    
    @classmethod
    def verificar_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    jwt.decode(encoded_token, "mi-secreto", algorithms=["HS256"])
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False