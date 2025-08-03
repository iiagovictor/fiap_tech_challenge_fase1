from fastapi import APIRouter, HTTPException, status, Depends
from app.models.databases.users import Usuario, db
from sqlalchemy.orm import Session
from app.config import Config
from app.models.schemas.users import LoginModel, TokenResponse
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


@router.post('/api/v1/login', response_model=TokenResponse)
def login(request: LoginModel):
    """### 🔐 Login
    Este endpoint permite que um usuário faça login no sistema.
    #### Como usar:
    - Faça uma requisição POST para `/api/v1/login` com o email e senha do usuário.
    - Os dados devem ser enviados no corpo da requisição no formato JSON.
    - A resposta incluirá um token JWT que deve ser usado para autenticação em outros endpoints.
    """  # noqa: E501
    session = Session(bind=db)
    user = session.query(Usuario).filter_by(email=request.email).first()
    session.close()
    if not user or user.senha != request.senha:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos."
        )
    expire = datetime.utcnow() + timedelta(minutes=1)
    payload = {
        "sub": user.email,
        "name": user.nome,
        "admin": user.admin,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        Config.SECRET_KEY,
        algorithm=getattr(
            Config,
            'ALGORITHM',
            'HS256'
        )
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
