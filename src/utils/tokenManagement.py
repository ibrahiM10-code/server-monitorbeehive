from dotenv import load_dotenv
import jwt, datetime, pytz, os
load_dotenv()

class TokenManager:

    zona_horaria = pytz.timezone("America/Santiago")
    secreto = os.getenv("JWT_SECRET")
    
    @classmethod
    def configurar_secreto(cls, secret_key):
        
        cls.secreto = str(secret_key) if secret_key else None
        if not cls.secreto:
            raise ValueError("SECRET_KEY no está definido")
    
    @classmethod
    def generar_token(cls, datos_apicultor):
        payload = {
            "id": str(datos_apicultor["_id"]), 
            "rut": datos_apicultor["rut"],
            "iat": datetime.datetime.now(tz=cls.zona_horaria),
            "exp": datetime.datetime.now(tz=cls.zona_horaria) + datetime.timedelta(hours=2)
            }
        token = jwt.encode(payload, cls.secreto, algorithm="HS256")
        return token
    
    @classmethod
    def verificar_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    jwt.decode(encoded_token, cls.secreto, algorithms=["HS256"])
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False