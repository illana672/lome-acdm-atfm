import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Récupérer la variable d'environnement TESTING (0 par défaut)
TESTING = os.environ.get("TESTING", "0") == "1"

if TESTING:
    # Base SQLite en mémoire pour les tests
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    connect_args = {}  # NE PAS mettre check_same_thread ici
else:
    # Utilise PostgreSQL en production/développement (mets ta vraie URL)
    SQLALCHEMY_DATABASE_URL = "postgresql://acdm_user:motdepassefort@localhost/lome_acdm_atfm"
    connect_args = {}

# Création de l'engine SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    **connect_args
)

# Session locale pour l'accès à la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modèle pour les ORM
Base = declarative_base()

# Fonction utilitaire pour obtenir une session de base de données (Dépendance FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()