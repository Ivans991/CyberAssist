from sqlalchemy import create_engine
#engine será el encargado de establecer la comunicación entre Python/SQLAlchemy y SQLite.
from sqlalchemy.orm import declarative_base, sessionmaker
#declarative_base → nos permitirá crear luego nuestros modelos.
#sessionmaker → permitirá crear sesiones para interactuar con la base de datos.
DATABASE_URL = "sqlite:///./cyberassist.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
