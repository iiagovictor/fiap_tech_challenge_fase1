from fastapi import APIRouter, HTTPException, status, Depends
from app.models.databases.users import Usuario
from app.models.databases.base import SessionLocal
from app.models.schemas.users import LoginModel
from app.models.schemas.auth import TokenResponse
from app.config import Config
import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

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
def login(request: LoginModel):
    """### 🔐 Login
    Este endpoint permite que um usuário faça login no sistema.
    #### Como usar:
    - Faça uma requisição POST para `/api/v1/login` com o email e senha do usuário.
    - Os dados devem ser enviados no corpo da requisição no formato JSON.
    - A resposta incluirá um token JWT que deve ser usado para autenticação em outros endpoints.
    """  # noqa: E501
    session = SessionLocal()
    user = session.query(Usuario).filter_by(email=request.email).first()
    session.close()
    if not user or user.senha != request.senha:
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
    return {
        "access_token": token,
        "token_type": "bearer",
        "expiration": expire.timestamp()
    }


@router.post('/api/v1/auth/refresh', response_model=TokenResponse, status_code=201)  # noqa: E501
def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):  # noqa: E501
    """### ♻️ Refresh Token
    Este endpoint permite renovar o token JWT antes do vencimento.
    - Envie o token atual no header Authorization (Bearer).
    - Retorna um novo token JWT com novo tempo de expiração.
    """
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
        return {
            "access_token": token,
            "token_type": "bearer",
            "expiration": expire.timestamp()
        }
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido para refresh."
            )
