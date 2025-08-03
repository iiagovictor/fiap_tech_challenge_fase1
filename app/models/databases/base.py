from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.config import Config

Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
