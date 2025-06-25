import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Adapter ces imports à ton projet
from backend.models import Base, Meteo

@pytest.fixture(scope="function")
def session():
    # 1. Crée un moteur SQLite en mémoire
    engine = create_engine("sqlite:///:memory:")
    # 2. Crée toutes les tables
    Base.metadata.create_all(engine)
    # 3. Crée une session
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_and_read_meteo(session):
    meteo = Meteo(
        temperature=25.7,
        direction_vent=120,
        vitesse_vent=8,
        visibilite=10000,
        rvr=700,
        humidite=60.0,
        pression_qnh=1013,
        date_heure=datetime(2025, 6, 24, 10, 0, 0)
    )
    session.add(meteo)
    session.commit()
    result = session.query(Meteo).first()
    assert result.temperature == 25.7
    assert result.direction_vent == 120
    assert result.vitesse_vent == 8
    assert result.visibilite == 10000
    assert result.rvr == 700
    assert result.humidite == 60.0
    assert result.pression_qnh == 1013
    assert result.date_heure == datetime(2025, 6, 24, 10, 0, 0)

def test_update_meteo(session):
    meteo = Meteo(
        temperature=20,
        direction_vent=100,
        vitesse_vent=12,
        visibilite=9000,
        rvr=600,
        humidite=55,
        pression_qnh=1009,
        date_heure=datetime(2025, 6, 24, 11, 0, 0)
    )
    session.add(meteo)
    session.commit()
    meteo.temperature = 22
    session.commit()
    result = session.query(Meteo).filter_by(direction_vent=100).first()
    assert result.temperature == 22

def test_delete_meteo(session):
    meteo = Meteo(
        temperature=19,
        direction_vent=90,
        vitesse_vent=7,
        visibilite=8500,
        rvr=580,
        humidite=65,
        pression_qnh=1007,
        date_heure=datetime(2025, 6, 24, 12, 0, 0)
    )
    session.add(meteo)
    session.commit()
    session.delete(meteo)
    session.commit()
    result = session.query(Meteo).filter_by(direction_vent=90).first()
    assert result is None