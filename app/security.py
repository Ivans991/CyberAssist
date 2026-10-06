import os
import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

USUARIO_CORRECTO = os.getenv("CYBERASSIST_USERNAME", "analista")
CONTRASENA_CORRECTA = os.getenv("CYBERASSIST_PASSWORD", "")


def verificar_credenciales(
    credenciales: HTTPBasicCredentials = Depends(security),
):
    usuario_correcto = secrets.compare_digest(
        credenciales.username,
        USUARIO_CORRECTO,
    )

    contrasena_correcta = secrets.compare_digest(
        credenciales.password,
        CONTRASENA_CORRECTA,
    )

    if not (usuario_correcto and contrasena_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credenciales.username