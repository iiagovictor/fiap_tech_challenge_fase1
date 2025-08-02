from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")
    ativo: bool = True
    admin: bool = False


class LoginModel(BaseModel):
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
