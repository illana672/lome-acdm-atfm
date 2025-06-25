import pytest

def test_create_porte(client):
    payload = {
        "terminal": "A",
        "nom_porte": "P10",
        "statut": "libre"
    }
    response = client.post("/portes_embarquement/", json=payload)
    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["terminal"] == "A"
    assert data["nom_porte"] == "P10"

def test_read_portes(client):
    client.post("/portes_embarquement/", json={"terminal": "A", "nom_porte": "P11", "statut": "occupee"})
    response = client.get("/portes_embarquement/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["nom_porte"] == "P11" for p in data)

def test_update_porte(client):
    resp = client.get("/portes-embarquement/")
    portes = resp.json()
    if not portes:
        test_create_porte(client)
        portes = client.get("/portes-embarquement/").json()
    porte_id = portes[0]["id"]
    resp = client.put(f"/portes-embarquement/{porte_id}", json={
        "terminal": "C",
        "nom_porte": "P14",
        "statut": "occupe"
    })
    print(resp.status_code, resp.json())  # Pour debug
    assert resp.status_code == 200
    assert resp.json()["nom_porte"] == "P14"

def test_delete_porte(client):
    resp = client.get("/portes-embarquement/")
    portes = resp.json()
    if not portes:
        test_create_porte(client)
        portes = client.get("/portes-embarquement/").json()
    porte_id = portes[0]["id"]
    resp = client.delete(f"/portes-embarquement/{porte_id}")
    print(resp.status_code, resp.json())  # Pour debug
    assert resp.status_code == 200
    assert resp.json().get("ok") is True