from fastapi import FastAPI
from backend.models import Base
from backend.database import engine
from backend.routes.vols import router as vols_router
from backend.routes.avions import router as avions_router
from backend.routes.compagnies import router as compagnies_router
from backend.routes.portes_embarquement import router as portes_embarquement_router
from backend.routes import postes_stationnement
from backend.routes.alertes import router as alertes_router
from backend.routes import utilisateurs as utilisateurs_router
from backend.routes import notifications as notifications_router
from backend.routes import roles
from backend.routes import messages_atfm
from backend.routes import meteo
from backend.routes import historique_operations
from backend.routes import sources_donnees
from backend.routes import sequences_depart
from backend.routes import communication_interne
from backend.routes import parametres_systeme
from backend.routes import organisations_partenaires
from backend.routes import groupes_communication
from backend.routes import evenements
from backend.routes import milestones
from backend.routes import audit_logs
from backend.routes import taches
from backend.routes import documents
from backend.routes import historique_etat_vol
from backend.routes import webhooks
from backend.routes import personnalisation_utilisateur
from backend.routes import incidents_techniques
from backend.routes import maintenance
from backend.routes import ressources
from backend.routes import affectations_ressources
from backend.routes import logs_systeme
from backend.routes import sessions_apoc
from backend.routes import chat_apoc
from backend.routes import alertes_meteo
from backend.routes import plan_aeroport_svg
from backend.routes import slots_atfm
from backend.routes import integration_systemes_externes
from backend.routes import gantt_sequencement
from backend.routes import gestion_droits_utilisateurs
from backend.routes import notifications_websocket
from backend.routes import parametres_notifications
from backend.routes import sessions
from backend.routes import pays
from backend.routes import aeroports
from backend.routes import historiques_vols
from backend.routes import priorites_source
from backend.routes import planifications_nationales




Base.metadata.create_all(bind=engine)
app = FastAPI()
print("INCLUSIONS", app.routes)

app.include_router(vols_router)

app.include_router(avions_router)

app.include_router(compagnies_router)

app.include_router(portes_embarquement_router)

app.include_router(postes_stationnement.router)

app.include_router(alertes_router)

app.include_router(utilisateurs_router.router)

app.include_router(notifications_router.router)

app.include_router(roles.router)

app.include_router(messages_atfm.router)

app.include_router(meteo.router)

app.include_router(historique_operations.router)

app.include_router(sources_donnees.router)

app.include_router(sequences_depart.router)

app.include_router(communication_interne.router)

app.include_router(parametres_systeme.router)

app.include_router(organisations_partenaires.router)

app.include_router(groupes_communication.router)

app.include_router(evenements.router)

app.include_router(milestones.router)

app.include_router(audit_logs.router)

app.include_router(taches.router)

app.include_router(documents.router)

app.include_router(historique_etat_vol.router)

app.include_router(webhooks.router)

app.include_router(personnalisation_utilisateur.router)

app.include_router(incidents_techniques.router)

app.include_router(maintenance.router)

app.include_router(ressources.router)

app.include_router(affectations_ressources.router)

app.include_router(logs_systeme.router)

app.include_router(sessions_apoc.router)

app.include_router(chat_apoc.router)

app.include_router(alertes_meteo.router)

app.include_router(plan_aeroport_svg.router)

app.include_router(slots_atfm.router)

app.include_router(integration_systemes_externes.router)

app.include_router(gantt_sequencement.router)

app.include_router(gestion_droits_utilisateurs.router)

app.include_router(notifications_websocket.router)

app.include_router(parametres_notifications.router)

app.include_router(sessions.router)

app.include_router(pays.router)

app.include_router(aeroports.router)

app.include_router(historiques_vols.router)

app.include_router(priorites_source.router)

app.include_router(planifications_nationales.router)