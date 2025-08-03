class Config:
    SECRET_KEY = "b7f8e1c2-4d5a-4e6b-9c3d-2f1a8e7b6c5d"
    ALGORITHM = "HS256"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///banco.db"
    VERSION = "1.0.0"
    TITLE = "FIAP - Biblioteca Digital API"
    DESCRIPTION = "API para consulta, pesquisa e análise de livros da Biblioteca Digital FIAP. Permite acesso a informações detalhadas, categorias, estatísticas e health check dos dados."  # noqa: E501
