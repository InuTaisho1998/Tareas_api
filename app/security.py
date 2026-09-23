from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings

password_hash_context = PasswordHash.recommended()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCES_TOKENS_EXPIRE_MINUTES = 15



 ##Funciones de hashin
def generate_password_hash(password: str) ->str:
    return password_hash_context.hash(password)


def verify_password(password_plana: str, hash_guardado: str) -> bool:
    return password_hash_context.verify(password_plana,hash_guardado)


##Dunsiones de tokens

def create_access_token(data:dict) ->str:
    datos_a_firmar= data.copy()

    # Le agregamos una fecha de expiración al token
    expiracion=datetime.now(timezone.utc)+ timedelta(minutes=ACCES_TOKENS_EXPIRE_MINUTES)
    datos_a_firmar.update({"exp":expiracion})

    # Creamos y firmamos el token usando PyJWT
    tokens_jwt= jwt.encode(datos_a_firmar,SECRET_KEY,algorithm=ALGORITHM)
    return tokens_jwt

####Leer tokens