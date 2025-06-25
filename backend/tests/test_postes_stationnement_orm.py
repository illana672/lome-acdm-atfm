import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, PosteStationnement
from datetime import datetime

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_and_read_poste(session):
    poste = PosteStationnement(
        numero_poste="PS01", localisation="Zone A", statut="libre",
        debut_occupation=datetime(2025, 6, 25, 8, 0), fin_occupation=None
    )
    session.add(poste)
    session.commit()
    result = session.query(PosteStationnement).filter_by(numero_poste="PS01").first()
    assert result is not None
    assert result.statut == "libre"

def test_update_poste(session):
    poste = PosteStationnement(numero_poste="PS02", localisation="Zone B", statut="libre")
    session.add(poste)
    session.commit()
    poste.statut = "occupee"
    session.commit()
    result = session.query(PosteStationnement).filter_by(numero_poste="PS02").first()
    assert result.statut == "occupee"

def test_delete_poste(session):
    poste = PosteStationnement(numero_poste="PS03", localisation="Zone C", statut="libre")
    session.add(poste)
    session.commit()
    session.delete(poste)
    session.commit()
    result = session.query(PosteStationnement).filter_by(numero_poste="PS03").first()
    assert result is None