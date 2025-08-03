from fastapi import APIRouter, HTTPException, Depends
from app.api.v1.auth import get_current_user
from app.models.databases.users import Usuario
from app.models.databases.base import SessionLocal
from app.models.schemas.users import (
    UserCreate,
    UsersListResponse
)

router = APIRouter(tags=["Users"])


@router.post("/api/v1/users/register", status_code=201)
def post_register_user(user: UserCreate, current_user=Depends(get_current_user)):  # noqa: E501
    """### 📝 Registrar Usuário
    Este endpoint permite o registro de um novo usuário no sistema.
    #### Como usar:
    - Faça uma requisição POST para `/api/v1/users/register` com os dados do usuário.
    - Os dados devem ser enviados no corpo da requisição no formato JSON.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    - O token deve ser de um usuário autenticado com permissão para registrar novos usuários.
    """  # noqa: E501
    if not current_user.get("admin", False):
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem registrar novos usuários."
        )
    session = SessionLocal()
    if session.query(Usuario).filter_by(email=user.email).first():
        session.close()
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
def get_users(current_user=Depends(get_current_user)):
    """### 👥 Listar Usuários
    Retorna uma lista de todos os usuários cadastrados. Apenas administradores podem acessar.

    #### Como usar:
    - Faça uma requisição GET para `/api/v1/users`.
    - A resposta incluirá uma lista de usuários com seus detalhes.
    - É necessário enviar o token JWT no header Authorization: Bearer <token>.
    - O token deve ser de um usuário autenticado com permissão para listar usuários.
    """  # noqa: E501
    if not current_user.get("admin", False):
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
    return {
        "success": True,
        "message": "Usuários listados com sucesso.",
        "data": users_list
    }
