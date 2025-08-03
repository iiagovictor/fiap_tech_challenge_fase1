from fastapi import APIRouter, HTTPException, Depends, Request
from app.api.v1.auth import get_current_user
from app.models.databases.users import Usuario
from app.models.databases.base import SessionLocal
from app.models.schemas.users import (
    UserCreate,
    UsersListResponse,
    UserResponse
)
from app.utils.app_logger import AppLogger
from app.models.logger import LoggerModel
import time

router = APIRouter(tags=["Users"])


@router.post("/api/v1/users/register", response_model=UserResponse, status_code=201)  # noqa: E501
async def post_register_user(request: Request, user: UserCreate, current_user=Depends(get_current_user)):  # noqa: E501
    """### 📝 Registrar Usuário
    Este endpoint permite o registro de um novo usuário no sistema.
    #### Como usar:
    - Faça uma requisição POST para `/api/v1/users/register` com os dados do usuário.
    - Os dados devem ser enviados no corpo da requisição no formato JSON.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    - O token deve ser de um usuário autenticado com permissão para registrar novos usuários.
    """  # noqa: E501
    start_time = time.time()
    if not current_user.get("admin", False):
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("users"),
            LoggerModel(
                status_code=403,
                endpoint="/api/v1/users/register",
                message="Tentativa de registro de usuário sem permissão.",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem registrar novos usuários."
        )
    session = SessionLocal()
    if session.query(Usuario).filter_by(email=user.email).first():
        session.close()
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("users"),
            LoggerModel(
                status_code=400,
                endpoint="/api/v1/users/register",
                message=f"Usuário já cadastrado: {user.email}",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=400,
            detail="Usuario já cadastrado com este e-mail."
            )
    novo_usuario = Usuario(
        nome=user.nome,
        email=user.email,
        senha=user.senha,
        ativo=user.ativo,
        admin=user.admin
    )
    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)
    session.close()
    latency = time.time() - start_time
    AppLogger().set_log_message(
        AppLogger().create_logger("users"),
        LoggerModel(
            status_code=201,
            endpoint="/api/v1/users/register",
            message=f"Usuário cadastrado com sucesso: {novo_usuario.email}",
            type="info",
            method=request.method,
            latency=latency
        )
    )
    return {
        "success": True,
        "message": "Usuário cadastrado com sucesso.",
        "data": {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email,
            "ativo": novo_usuario.ativo,
            "admin": novo_usuario.admin
            }
        }


@router.get("/api/v1/users", response_model=UsersListResponse)
async def get_users(request: Request, current_user=Depends(get_current_user)):
    """### 👥 Listar Usuários
    Retorna uma lista de todos os usuários cadastrados. Apenas administradores podem acessar.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/users`.
    - A resposta incluirá uma lista de usuários com seus detalhes.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    - O token deve ser de um usuário autenticado com permissão para listar usuários.
    """  # noqa: E501
    start_time = time.time()
    if not current_user.get("admin", False):
        latency = time.time() - start_time
        AppLogger().set_log_message(
            AppLogger().create_logger("users"),
            LoggerModel(
                status_code=403,
                endpoint="/api/v1/users",
                message="Tentativa de listagem de usuários sem permissão.",
                type="warning",
                method=request.method,
                latency=latency
            )
        )
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem listar usuários."
        )
    session = SessionLocal()
    usuarios = session.query(Usuario).all()
    session.close()
    users_list = [
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "ativo": u.ativo,
            "admin": u.admin
        } for u in usuarios
    ]
    latency = time.time() - start_time
    AppLogger().set_log_message(
        AppLogger().create_logger("users"),
        LoggerModel(
            status_code=200,
            endpoint="/api/v1/users",
            message="Usuários listados com sucesso.",
            type="info",
            method=request.method,
            latency=latency
        )
    )
    return {
        "success": True,
        "message": "Usuários listados com sucesso.",
        "data": users_list
    }
