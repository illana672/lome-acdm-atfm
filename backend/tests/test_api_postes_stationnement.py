import pytest
from datetime import datetime

def test_create_poste(client):
    payload = {
        "numero_poste": "PS10",
        "localisation": "Zone 1",
        "statut": "libre",
        "debut_occupation": "2025-06-25T09:00:00",
        "fin_occupation": None
    }
    response = client.post("/postes-stationnement/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["numero_poste"] == "PS10"

def test_read_postes(client):
    client.post("/postes-stationnement/", json={"numero_poste": "PS11", "localisation": "Zone 2", "statut": "occupee"})
    response = client.get("/postes-stationnement/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["numero_poste"] == "PS11" for p in data)

def test_update_poste(client):
    client.post("/postes-stationnement/", json={"numero_poste": "PS12", "localisation": "Zone 3", "statut": "libre"})
    postes = client.get("/postes-stationnement/").json()
    poste_id = postes[0]["id"]
    resp = client.put(f"/postes-stationnement/{poste_id}", json={"statut": "occupee"})
    assert resp.status_code == 200
    assert resp.json()["statut"] == "occupee"

def test_delete_poste(client):
    client.post("/postes-stationnement/", json={"numero_poste": "PS13", "localisation": "Zone 4", "statut": "libre"})
    postes = client.get("/postes-stationnement/").json()
    poste_id = postes[0]["id"]
    resp = client.delete(f"/postes-stationnement/{poste_id}")
    assert resp.status_code == 200
    assert resp.json().get("ok") is True