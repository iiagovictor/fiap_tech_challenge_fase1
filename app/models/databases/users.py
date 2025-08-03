from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import declarative_base
from app.config import Config

db = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String(80), unique=True, nullable=False)
    email = Column("email", String, unique=True, nullable=False)
    senha = Column("senha", String(120), nullable=False)
    ativo = Column("ativo", Boolean, default=True, nullable=False)
    admin = Column("admin", Boolean, default=False, nullable=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
