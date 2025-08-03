from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.models.databases.users import Usuario
from app.models.databases.base import SessionLocal
from app.models.schemas.users import LoginModel
from app.models.schemas.auth import TokenResponse
from app.config import Config
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Authentication"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa: E501
    try:
        payload = jwt.decode(
            credentials.credentials,
            Config.SECRET_KEY,
            algorithms=[getattr(Config, 'ALGORITHM', 'HS256')]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


@router.post('/api/v1/auth/login', response_model=TokenResponse, status_code=201)  # noqa: E501
async def login(request: Request, body: LoginModel):
    """### 🔐 Login
    Este endpoint permite que um usuário faça login no sistema.
    #### Como usar:
    - Faça uma requisição POST para `/api/v1/login` com o email e senha do usuário.
    - Os dados devem ser enviados no corpo da requisição no formato JSON.
    - A resposta incluirá um token JWT que deve ser usado para autenticação em outros endpoints.
    """  # noqa: E501
    start_time = time.time()
    session = SessionLocal()
    user = session.query(Usuario).filter_by(email=body.email).first()
    session.close()
    latency = time.time() - start_time
    if not user or user.senha != body.senha:
        AppLogger().set_log_message(
            AppLogger().create_logger("auth"),
            LoggerModel(
                status_code=401,
                endpoint="/api/v1/auth/login",
                message="Email ou senha inválidos.",
                method=request.method,
                type="warning",
                latency=latency
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos."
        )
    expire = datetime.utcnow() + timedelta(minutes=5)
    payload = {
        "sub": user.email,
        "name": user.nome,
        "admin": user.admin,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=getattr(Config, 'ALGORITHM', 'HS256')
    )
    latency = time.time() - start_time
    AppLogger().set_log_message(
        AppLogger().create_logger("auth"),
        LoggerModel(
            status_code=201,
            endpoint="/api/v1/auth/login",
            message=f"Login realizado com sucesso para o usuário: {user.email}",  # noqa: E501
            method=request.method,
            type="info",
            latency=latency
        )
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expiration": expire.timestamp()
    }


@router.post('/api/v1/auth/refresh', response_model=TokenResponse, status_code=201)  # noqa: E501
async def refresh_token(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa: E501
    """### ♻️ Refresh Token
    Este endpoint permite renovar o token JWT antes do vencimento.
    - Envie o token atual no header Authorization (Bearer).
    - Retorna um novo token JWT com novo tempo de expiração.
    """
    start_time = time.time()
    try:
        payload = jwt.decode(
            credentials.credentials,
            Config.SECRET_KEY,
            algorithms=getattr(Config, 'ALGORITHM', 'HS256'),
            options={
                "verify_exp": False
                }
        )
        expire = datetime.utcnow() + timedelta(minutes=5)
        payload["exp"] = expire
        token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm=getattr(Config, 'ALGORITHM', 'HS256')
        )
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("auth"),
            LoggerModel(
                status_code=201,
                endpoint="/api/v1/auth/refresh",
                message=f"Token renovado para o usuário: {payload.get('sub', 'desconhecido')}",  # noqa: E501
                method=request.method,
                type="info",
                latency=latency
            )
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "expiration": expire.timestamp()
        }
    except jwt.InvalidTokenError:
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("auth"),
            LoggerModel(
                status_code=401,
                endpoint="/api/v1/auth/refresh",
                message="Token inválido para refresh.",
                method=request.method,
                type="warning",
                latency=latency
            )
        )
        raise HTTPException(
            status_code=401,
            detail="Token inválido para refresh."
            )
