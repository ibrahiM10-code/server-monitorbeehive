from dotenv import load_dotenv
import smtplib, ssl, os

load_dotenv()

def enviar_correo(correo_destino, codigo_verificacion):
    port = 587  # For starttls
    context = ssl.create_default_context()
    smtp_server = os.getenv("SMTP_SERVER")
    correo_de_envio = os.getenv("CORREO_DE_ENVIO")
    password = os.getenv("PASSWORD_CORREO_DE_ENVIO")

    message = f"From: <{correo_de_envio}> To: <{correo_destino}>\nSubject: Código de verificación\n\nIngresa el siguiente código para restaurar tu contraseña: {codigo_verificacion} en la siguiente dirección URL: http://localhost:5173/forgot-password."
    
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(correo_de_envio, password)
        server.sendmail(correo_de_envio, correo_destino, message.encode("utf-8"))
        return True
    return False