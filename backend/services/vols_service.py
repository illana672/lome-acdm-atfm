# services/vols_service.py

from sqlalchemy.orm import Session
from backend import models, schemas 


def create_vol(db: Session, vol_in: VolCreate) -> VolRead:
    avion = db.query(Avion).filter_by(id=vol_in.avion_id).first()
    compagnie = db.query(Compagnie).filter_by(id=vol_in.compagnie_id).first()
    if not avion or not compagnie:
        raise ValueError("Avion ou compagnie introuvable")
    db_vol = Vol(**vol_in.dict())
    db.add(db_vol)
    db.commit()
    db.refresh(db_vol)
    return VolRead.from_orm(db_vol)

def update_vol(db: Session, vol_id: int, vol_update: VolCreate) -> VolRead:
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    for field, value in vol_update.dict().items():
        setattr(vol, field, value)
    db.commit()
    db.refresh(vol)
    return VolRead.from_orm(vol)

def delete_vol(db: Session, vol_id: int) -> bool:
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        return False
    db.delete(vol)
    db.commit()
    return True

def list_vols(db: Session, compagnie_id: int = None):
    query = db.query(Vol)
    if compagnie_id:
        query = query.filter(Vol.compagnie_id == compagnie_id)
    return query.all()

def get_vol_by_id(db: Session, vol_id: int) -> VolRead:
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    return VolRead.from_orm(vol)

def import_vols_from_aodb(db: Session, vols_data: list):
    # vols_data = [dict, dict, ...]
    vols = []
    for data in vols_data:
        db_vol = Vol(**data)
        db.add(db_vol)
        vols.append(db_vol)
    db.commit()
    for v in vols:
        db.refresh(v)
    return vols


def set_statut_vol(db: Session, vol_id: int, nouveau_statut: str, user_id: int):
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    precedent = vol.statut
    vol.statut = nouveau_statut
    db.commit()
    # Historiser le changement
    histo = HistoriqueEtatVol(vol_id=vol_id, statut_avant=precedent, statut_apres=nouveau_statut, user_id=user_id)
    db.add(histo)
    db.commit()
    return vol

def update_tobt(db: Session, vol_id: int, nouvelle_tobt: str, user_id: int):
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    precedent = vol.tobt
    vol.tobt = nouvelle_tobt
    db.commit()
    # Historiser le changement de TOBT dans l’historique
   
    histo = HistoriqueEtatVol(vol_id=vol_id, champ_modifie="tobt", valeur_avant=precedent, valeur_apres=nouvelle_tobt, user_id=user_id)
    db.add(histo)
    db.commit()
    return vol

def assigner_porte(db: Session, vol_id: int, porte_id: int):
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    vol.porte_embarquement_id = porte_id
    db.commit()
    return vol



def assigner_poste_stationnement(db: Session, vol_id: int, poste_id: int):
    vol = db.query(Vol).filter_by(id=vol_id).first()
    if not vol:
        raise ValueError("Vol introuvable")
    vol.poste_stationnement_id = poste_id
    db.commit()
    return vol

def calculer_sequence_depart(db: Session, date_depart):
    # Exemple simplifié : trier les vols selon leur heure de départ
    vols = db.query(Vol).filter(Vol.date_depart == date_depart).order_by(Vol.heure_depart).all()
    return vols

def consulter_historique_vol(db: Session, vol_id: int):
    historique_etat = db.query(HistoriqueEtatVol).filter_by(vol_id=vol_id).all()
    historique_ops = db.query(HistoriqueOperations).filter_by(vol_id=vol_id).all()
    return {"etat": historique_etat, "ops": historique_ops}

def generer_reporting_vols(db: Session, periode_debut, periode_fin):
    from sqlalchemy import func
    retards = db.query(func.count()).filter(
        Vol.date_depart >= periode_debut,
        Vol.date_depart <= periode_fin,
        Vol.statut == "retard"
    ).scalar()
    totaux = db.query(func.count()).filter(
        Vol.date_depart >= periode_debut,
        Vol.date_depart <= periode_fin
    ).scalar()
    return {"retards": retards, "totaux": totaux}

def envoyer_notification(db: Session, vol_id: int, user_id: int, contenu: str, type_: str = "web"):
    notif = Notification(vol_id=vol_id, utilisateur_id=user_id, contenu=contenu, type=type_)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

def verifier_acces_vol(db: Session, user_id: int, vol_id: int, action: str):
    droit = db.query(GestionDroitsUtilisateurs).filter_by(utilisateur_id=user_id, vol_id=vol_id, action=action).first()
    return droit is not None
