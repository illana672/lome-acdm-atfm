import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, PorteEmbarquement

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_and_read_porte(session):
    porte = PorteEmbarquement(terminal="A", nom_porte="P01", statut="libre")
    session.add(porte)
    session.commit()
    result = session.query(PorteEmbarquement).filter_by(nom_porte="P01").first()
    assert result is not None
    assert result.terminal == "A"
    assert result.statut == "libre"

def test_update_porte(session):
    porte = PorteEmbarquement(terminal="B", nom_porte="P02", statut="occupee")
    session.add(porte)
    session.commit()
    porte.statut = "libre"
    session.commit()
    result = session.query(PorteEmbarquement).filter_by(nom_porte="P02").first()
    assert result.statut == "libre"

def test_delete_porte(session):
    porte = PorteEmbarquement(terminal="C", nom_porte="P03", statut="libre")
    session.add(porte)
    session.commit()
    session.delete(porte)
    session.commit()
    result = session.query(PorteEmbarquement).filter_by(nom_porte="P03").first()
    assert result is None