import pytest

def test_create_meteo(client):
    payload = {
        "temperature": 19.7,
        "direction_vent": 310,
        "vitesse_vent": 9,
        "visibilite": 6000,
        "rvr": 650,
        "humidite": 70.5,
        "pression_qnh": 1013,
        "date_heure": "2025-06-24T21:00:00"
    }
    response = client.post("/meteo/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["temperature"] == 19.7
    assert data["direction_vent"] == 310

def test_read_meteos(client):
    # Crée un enregistrement au préalable
    payload = {
        "temperature": 22.2,
        "direction_vent": 270,
        "vitesse_vent": 12,
        "visibilite": 7000,
        "rvr": 750,
        "humidite": 65.0,
        "pression_qnh": 1008,
        "date_heure": "2025-06-25T12:30:00"
    }
    client.post("/meteo/", json=payload)
    response = client.get("/meteo/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "temperature" in data[0]

def test_update_meteo(client):
    # Crée un enregistrement à modifier
    payload = {
        "temperature": 23.5,
        "direction_vent": 180,
        "vitesse_vent": 15,
        "visibilite": 8000,
        "rvr": 700,
        "humidite": 60.0,
        "pression_qnh": 1012,
        "date_heure": "2025-06-26T15:00:00"
    }
    resp = client.post("/meteo/", json=payload)
    meteo_id = resp.json()["id"]
    update_payload = {
        "temperature": 24.1
    }
    response = client.put(f"/meteo/{meteo_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["temperature"] == 24.1

def test_delete_meteo(client):
    # Crée un enregistrement à supprimer
    payload = {
        "temperature": 20.5,
        "direction_vent": 200,
        "vitesse_vent": 11,
        "visibilite": 8500,
        "rvr": 780,
        "humidite": 68.0,
        "pression_qnh": 1010,
        "date_heure": "2025-06-27T16:00:00"
    }
    resp = client.post("/meteo/", json=payload)
    meteo_id = resp.json()["id"]
    response = client.delete(f"/meteo/{meteo_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}