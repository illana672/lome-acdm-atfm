import pytest

def test_create_pays(client):
    data = {"code_iso": "BEN", "nom": "Bénin", "continent": "Afrique"}
    resp = client.post("/pays/", json=data)
    assert resp.status_code == 201
    result = resp.json()
    assert result["code_iso"] == "BEN"
    assert result["nom"] == "Bénin"

def test_duplicate_code_iso(client):
    data = {"code_iso": "BEN", "nom": "Bénin", "continent": "Afrique"}
    resp = client.post("/pays/", json=data)
    assert resp.status_code == 400  # ou 409 si tu gères le conflit

def test_read_pays(client):
    resp = client.get("/pays/")
    assert resp.status_code == 200
    pays_list = resp.json()
    assert isinstance(pays_list, list)
    assert any(p["code_iso"] == "BEN" for p in pays_list)

def test_update_pays(client):
    pays = client.get("/pays/").json()[0]
    pays_id = pays["id"]
    data = {
        "code_iso": pays["code_iso"],
        "nom": "République du Bénin",
        "continent": pays["continent"]
    }
    resp = client.put(f"/pays/{pays_id}", json=data)
    print(resp.json())  # À enlever plus tard
    assert resp.status_code == 200
    assert resp.json()["nom"].startswith("République")

def test_delete_pays(client):
    pays_id = client.get("/pays/").json()[0]["id"]
    resp = client.delete(f"/pays/{pays_id}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True