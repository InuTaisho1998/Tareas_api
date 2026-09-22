from unittest.mock import MagicMock

from app.routers.tasks import get_current_user
from app.security import create_access_token, generate_password_hash, verify_password


def test_generar_contraena():
    plain_password = "contrasena_prueba"
    hashed = generate_password_hash(plain_password)

    assert plain_password != hashed 
    assert hashed is not None 
    assert isinstance(hashed, str) 


def test_verficar_contrasena():
    plain_password = "contrasena_prueba"
    hashed = generate_password_hash(plain_password)  
    verificar = verify_password(plain_password, hashed)

    assert isinstance(verificar, bool)
    assert verificar is True


def test_vericar_incorrecto():
    plain_password = "contrasena_prueba"
    hashed = generate_password_hash(plain_password)
    verificar = verify_password("otracontrasena", hashed)

    assert isinstance(verificar, bool)
    assert verificar is False

def test_crear_token():
    data= {"sub": "username"}
    token = create_access_token(data)

    assert isinstance(token, str)
    assert token is not None

def test_verificar_token():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = {"username": "fakeusername", "email": "fakeemail"}
    data= {"sub": "username"}
    token = create_access_token(data)
    verficar_token= get_current_user(token, mock_db)

    assert verficar_token == {"username": "fakeusername", "email": "fakeemail"}
    assert verficar_token is not None