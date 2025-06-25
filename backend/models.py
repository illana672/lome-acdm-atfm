from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, JSON, ForeignKey, DateTime,  Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from backend.database import Base

Base = declarative_base()

class Vol(Base):
    __tablename__ = "vols"
    id = Column(Integer, primary_key=True, index=True)
    numero_vol = Column(String(20), unique=True, nullable=False)
    compagnie_id = Column(Integer, ForeignKey("compagnies.id"))
    avion_id = Column(Integer,ForeignKey("avions.id"))
    type_vol = Column(String(20))
    statut = Column(String(50))
    aeroport_depart = Column(String(10))
    aeroport_arrivee = Column(String(10))
    porte_embarquement = Column(String(10))
    poste_stationnement = Column(String(10))
    date_vol = Column(Date)
    sobt = Column(TIMESTAMP)
    tobt = Column(TIMESTAMP)
    aobt = Column(TIMESTAMP)
    eta = Column(TIMESTAMP)
    ata = Column(TIMESTAMP)
    tsat = Column(TIMESTAMP)
    ctot = Column(TIMESTAMP)
    alertes = Column(JSON)

    compagnie = relationship("Compagnie", back_populates="vols")
    avion = relationship("Avion", back_populates="vols")
    alertes = relationship("Alerte", back_populates="vol", cascade="all, delete")
    messages_atfm = relationship("MessageATFM", back_populates="vol", cascade="all, delete")
    milestones = relationship("Milestone", back_populates="vol", cascade="all, delete")
    sequences_depart = relationship("SequenceDepart", back_populates="vol", cascade="all, delete")
    documents = relationship("Document", back_populates="vol", cascade="all, delete")
    historiques_etat_vol = relationship("HistoriqueEtatVol", back_populates="vol", cascade="all, delete")
    affectations_ressources = relationship("AffectationRessource", back_populates="vol")
    incidents_techniques = relationship("IncidentTechnique", back_populates="vol")
    plans = relationship("PlanAeroportSVG", back_populates="vol", cascade="all, delete-orphan")
    slots_atfm = relationship("SlotATFM", back_populates="vol")
    gantt_sequencements = relationship("GanttSequencement", back_populates="vol", cascade="all, delete-orphan")
    historiques = relationship("HistoriqueVol", back_populates="vol")

class Avion(Base):
    __tablename__ = "avions"

    id = Column(Integer, primary_key=True, index=True)
    immatriculation = Column(String(20), unique=True, nullable=False)
    type_avion = Column(String(30))
    compagnie_id = Column(Integer, ForeignKey("compagnies.id"))  # Relation avec la table compagnies
    capacite_sieges = Column(Integer)
    capacite_fret = Column(Integer)

    # Si tu veux pouvoir accéder à la compagnie depuis l'avion
    compagnie = relationship("Compagnie", back_populates="avions")
    vols = relationship("Vol", back_populates="avion")
    historiques_vols = relationship("HistoriqueVol", back_populates="avion")
    

class Compagnie(Base):
    __tablename__ = "compagnies"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    code_oaci = Column(String(10))
    code_iata = Column(String(5))
    pays_origine = Column(String(50))

    avions = relationship("Avion", back_populates="compagnie")  # Doit exister
    vols = relationship("Vol", back_populates="compagnie")
    historiques_vols = relationship("HistoriqueVol", back_populates="compagnie")

class PorteEmbarquement(Base):
    __tablename__ = "portes_embarquement"

    id = Column(Integer, primary_key=True, index=True)
    terminal = Column(String(20))
    nom_porte = Column(String(10))
    statut = Column(String(20))

class PosteStationnement(Base):
    __tablename__ = "postes_stationnement"
    id = Column(Integer, primary_key=True, index=True)
    numero_poste = Column(String(20), nullable=False)
    localisation = Column(String(50), nullable=False)
    statut = Column(String(20), nullable=False)
    debut_occupation = Column(DateTime, nullable=True)
    fin_occupation = Column(DateTime, nullable=True)

class Alerte(Base):
    __tablename__ = "alertes"
    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"))  # Assure-toi que la table "vols" existe bien
    type_alerte = Column(String(50))
    description = Column(Text)
    niveau = Column(String(20))
    date_heure = Column(DateTime)
    statut = Column(String(20))

    vol = relationship("Vol", back_populates="alertes")

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    nom_complet = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    statut = Column(String(20))

    notifications = relationship("Notification", back_populates="utilisateur", cascade="all, delete")
    documents = relationship("Document", back_populates="utilisateur", cascade="all, delete")
    historique_operations = relationship("HistoriqueOperation", back_populates="utilisateur", cascade="all, delete")
    incidents_techniques = relationship("IncidentTechnique", back_populates="utilisateur")
    maintenances = relationship("Maintenance", back_populates="utilisateur")
    audit_logs = relationship("AuditLog", back_populates="utilisateur")
    role = relationship("Role", back_populates="utilisateurs")
    historiques_etat_vol = relationship("HistoriqueEtatVol", back_populates="utilisateur")
    personnalisations = relationship("PersonnalisationUtilisateur", back_populates="utilisateur")
    sessions_apoc = relationship("SessionAPOC", back_populates="utilisateur")
    chats_apoc = relationship("ChatAPOC", back_populates="utilisateur")
    droits_utilisateur = relationship("GestionDroitsUtilisateurs", back_populates="utilisateur", cascade="all, delete-orphan")
    notification = relationship("NotificationWebsocket", back_populates="utilisateur", cascade="all, delete-orphan")
    parametres_notifications = relationship( "ParametresNotifications", back_populates="utilisateur", cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="utilisateur", cascade="all, delete-orphan")
    logs_systeme = relationship("LogSysteme", back_populates="utilisateur")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    type = Column(String(20))
    contenu = Column(Text)
    date_heure = Column(DateTime)
    statut = Column(String(20))

    utilisateur = relationship("Utilisateur",back_populates="notifications" )  # Permet d'accéder à l'utilisateur associé

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nom_role = Column(String(50), nullable=False)
    permissions = Column(JSON)
    utilisateurs = relationship("Utilisateur", back_populates="role")


class MessageATFM(Base):
    __tablename__ = "messages_atfm"
    id = Column(Integer, primary_key=True, index=True)
    type_message = Column(String(10), nullable=False)
    vol_id = Column(Integer, ForeignKey("vols.id"), nullable=False)
    contenu = Column(JSON)
    statut = Column(String(20))
    date_emission = Column(DateTime)
    date_reception = Column(DateTime)

    # Optionnel : accès direct à l'objet Vol lié
    vol = relationship("Vol", back_populates="messages_atfm")

class Meteo(Base):
    __tablename__ = "meteo"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    direction_vent = Column(Integer)
    vitesse_vent = Column(Integer)
    visibilite = Column(Integer)
    rvr = Column(Integer)
    humidite = Column(Float)
    pression_qnh = Column(Integer)
    date_heure = Column(DateTime)


class HistoriqueOperation(Base):
    __tablename__ = "historique_operations"

    id = Column(Integer, primary_key=True, index=True)
    type_operation = Column(String(20), nullable=False)
    table_concernee = Column(String(50), nullable=False)
    details = Column(JSON, nullable=True)
    date_heure = Column(DateTime, nullable=False)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'), nullable=True)  # FK vers utilisateurs

    utilisateur = relationship("Utilisateur", back_populates="historique_operations")

class SourceDonnees(Base):
    __tablename__ = "sources_donnees"

    id = Column(Integer, primary_key=True, index=True)
    nom_source = Column(String(50), nullable=False)
    priorite = Column(String(10), nullable=True)
    statut = Column(String(20), nullable=True)

class SequenceDepart(Base):
    __tablename__ = "sequences_depart"

    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"), nullable=False)
    ordre = Column(Integer, nullable=True)
    tsat = Column(DateTime, nullable=True)
    demarrage_reel = Column(DateTime, nullable=True)
    statut = Column(String(20), nullable=True)
    vol = relationship("Vol", back_populates="sequences_depart")
class CommunicationInterne(Base):
    __tablename__ = "communication_interne"

    id = Column(Integer, primary_key=True, index=True)
    emetteur_id = Column(Integer, nullable=False)
    destinataires = Column(JSON, nullable=True)  # Liste d'IDs utilisateurs
    contenu = Column(Text, nullable=True)
    date_heure = Column(DateTime, nullable=True)

class ParametreSysteme(Base):
    __tablename__ = "parametres_systeme"

    id = Column(Integer, primary_key=True, index=True)
    nom_parametre = Column(String(50), nullable=False)
    valeur = Column(Text, nullable=True)
    description = Column(Text, nullable=True)

class OrganisationPartenaire(Base):
    __tablename__ = "organisations_partenaires"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    contact_principal = Column(String(50), nullable=True)
    email = Column(String(50), nullable=True)
    telephone = Column(String(20), nullable=True)

class GroupeCommunication(Base):
    __tablename__ = "groupes_communication"

    id = Column(Integer, primary_key=True, index=True)
    nom_groupe = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    membres = Column(JSON, nullable=True)

class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    statut = Column(String(20), nullable=True)

class Milestone(Base):
    __tablename__ = "milestones"
    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"), nullable=False)
    sobt = Column(DateTime, nullable=True)
    tobt = Column(DateTime, nullable=True)
    aobt = Column(DateTime, nullable=True)
    tsat = Column(DateTime, nullable=True)
    ctot = Column(DateTime, nullable=True)
    eta = Column(DateTime, nullable=True)
    ata = Column(DateTime, nullable=True)
    mise_a_jour = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    vol = relationship("Vol", back_populates="milestones")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    cible = Column(String(50), nullable=False)
    cible_id = Column(Integer, nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    date_heure = Column(DateTime(timezone=True), server_default=func.now())
    commentaire = Column(Text, nullable=True)
    utilisateur = relationship("Utilisateur", back_populates="audit_logs")


class Tache(Base):
    __tablename__ = "taches"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    statut = Column(String(20), nullable=False)
    date_heure_demarrage = Column(DateTime)
    date_heure_fin = Column(DateTime)
    details = Column(JSON)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    chemin_fichier = Column(String(255), nullable=False)
    type_document = Column(String(50), nullable=False)
    vol_id = Column(Integer, ForeignKey("vols.id", ondelete="CASCADE"))
    ressource_id = Column(Integer, ForeignKey("ressources.id", ondelete="CASCADE"))
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    date_heure_upload = Column(DateTime(timezone=True), server_default=func.now())
    ressources = relationship("Ressource", back_populates="documents")

    # Optionnel: relations (pour accès direct)
    vol = relationship("Vol", back_populates="documents", lazy="joined")
    ressource = relationship("Ressource", back_populates="documents", lazy="joined")
    utilisateur = relationship("Utilisateur", back_populates="documents", lazy="joined")

class HistoriqueEtatVol(Base):
    __tablename__ = "historique_etat_vol"
    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id", ondelete="CASCADE"))
    ancien_statut = Column(String(50))
    nouveau_statut = Column(String(50))
    date_heure_changement = Column(DateTime(timezone=True), server_default=func.now())
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))

    vol = relationship("Vol", back_populates="historiques_etat_vol", lazy="joined")
    utilisateur = relationship("Utilisateur", back_populates="historiques_etat_vol", lazy="joined")
    


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    type_evenement = Column(String(50), nullable=False)
    actif = Column(Boolean, default=True)
    date_heure_creation = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(JSON)

class PersonnalisationUtilisateur(Base):
    __tablename__ = "personnalisation_utilisateur"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="CASCADE"), nullable=False)
    parametre = Column(String(50), nullable=False)
    valeur = Column(Text)
    utilisateur = relationship("Utilisateur", back_populates="personnalisations")

class IncidentTechnique(Base):
    __tablename__ = "incidents_techniques"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(100), nullable=False)
    description = Column(Text)
    niveau_criticite = Column(String(20))
    statut = Column(String(20))
    date_heure = Column(DateTime(timezone=True), server_default=func.now())
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    vol_id = Column(Integer, ForeignKey("vols.id", ondelete="CASCADE"))
    utilisateur = relationship("Utilisateur", back_populates="incidents_techniques")
    vol = relationship("Vol", back_populates="incidents_techniques")

class Maintenance(Base):
    __tablename__ = "maintenance"
    id = Column(Integer, primary_key=True, index=True)
    ressource_id = Column(Integer, ForeignKey("ressources.id", ondelete="CASCADE"))
    type = Column(String(50), nullable=False)
    date_heure_debut = Column(DateTime(timezone=True))
    date_heure_fin = Column(DateTime(timezone=True))
    commentaire = Column(Text)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id", ondelete="SET NULL"))
    ressource = relationship("Ressource", back_populates="maintenances")
    utilisateur = relationship("Utilisateur", back_populates="maintenances")

class Ressource(Base):
    __tablename__ = "ressources"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50))
    nom = Column(String(50))
    disponibilite = Column(Boolean, default=True)
    details = Column(JSON)
    maintenances = relationship("Maintenance", back_populates="ressource")
    affectations_ressources = relationship("AffectationRessource", back_populates="ressource")
    documents = relationship("Document", back_populates="ressource")


class AffectationRessource(Base):
    __tablename__ = "affectations_ressources"
    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"))
    ressource_id = Column(Integer, ForeignKey("ressources.id"))
    date_heure_debut = Column(DateTime)
    date_heure_fin = Column(DateTime)
    statut = Column(String(20))
    notes = Column(Text)
    vol = relationship("Vol", back_populates="affectations_ressources")
    ressource = relationship("Ressource", back_populates="affectations_ressources")

class LogSysteme(Base):
    __tablename__ = "logs_systeme"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"))
    action = Column(Text)
    date_heure = Column(DateTime, default=datetime.utcnow)
    ip = Column(String(50))
    details = Column(JSON)
    utilisateur = relationship("Utilisateur", back_populates="logs_systeme")

class SessionAPOC(Base):
    __tablename__ = "sessions_apoc"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    date_heure_connexion = Column(DateTime, default=datetime.utcnow)
    date_heure_deconnexion = Column(DateTime, nullable=True)
    statut = Column(String(20), nullable=True)
    remarques = Column(Text, nullable=True)
    
    utilisateur = relationship("Utilisateur", back_populates="sessions_apoc")
    chats_apoc = relationship("ChatAPOC", back_populates="session_apoc")

class ChatAPOC(Base):
    __tablename__ = "chat_apoc"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    message = Column(Text, nullable=False)
    date_heure = Column(DateTime, default=datetime.utcnow)
    session_apoc_id = Column(Integer, ForeignKey("sessions_apoc.id"), nullable=False)
    
    utilisateur = relationship("Utilisateur", back_populates="chats_apoc")
    session_apoc = relationship("SessionAPOC", back_populates="chats_apoc")

class AlerteMeteo(Base):
    __tablename__ = "alertes_meteo"
    id = Column(Integer, primary_key=True, index=True)
    type_alerte = Column(String(50), nullable=False)
    description = Column(Text)
    niveau_criticite = Column(String(20))
    date_heure_debut = Column(DateTime, nullable=False)
    date_heure_fin = Column(DateTime, nullable=False)
    statut = Column(String(20), nullable=True)

class PlanAeroportSVG(Base):
    __tablename__ = "plan_aeroport_svg"
    id = Column(Integer, primary_key=True, index=True)
    nom_element = Column(String(50), nullable=False)
    type_element = Column(String(20), nullable=False)
    id_svg = Column(String(50), unique=True, nullable=False)
    statut = Column(String(20), nullable=True)
    vol_id = Column(Integer, ForeignKey("vols.id"))
    coordonnees = Column(JSON, nullable=True)  # JSON pour SQLite, JSONB pour Postgres

    vol = relationship("Vol", back_populates="plans")

class SlotATFM(Base):
    __tablename__ = "slots_atfm"
    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"), nullable=False)
    ctot = Column(DateTime, nullable=True)
    type_slot = Column(String(20), nullable=True)
    date_heure_attribution = Column(DateTime, nullable=True)
    statut = Column(String(20), nullable=True)
    commentaire = Column(Text, nullable=True)

    vol = relationship("Vol", back_populates="slots_atfm")


class IntegrationSystemesExternes(Base):
    __tablename__ = "integration_systemes_externes"

    id = Column(Integer, primary_key=True, index=True)
    systeme_externe = Column(String(50), nullable=False)
    endpoint = Column(String(255), nullable=False)
    protocole = Column(String(20), nullable=False)
    date_heure = Column(DateTime(timezone=True), server_default=func.now())
    details = Column(JSON, nullable=True)

class GanttSequencement(Base):
    __tablename__ = "gantt_sequencement"
    id = Column(Integer, primary_key=True)
    vol_id = Column(Integer, ForeignKey("vols.id"), nullable=False)
    debut = Column(DateTime, nullable=False)
    fin = Column(DateTime, nullable=False)
    ordre = Column(Integer, nullable=False)
    statut = Column(String(20), nullable=False)

    # Relation avec Vol
    vol = relationship("Vol", back_populates="gantt_sequencements")

class GestionDroitsUtilisateurs(Base):
    __tablename__ = "gestion_droits_utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    permission = Column(String(50), nullable=False)
    statut = Column(Boolean, default=True)

    utilisateur = relationship("Utilisateur", back_populates="droits_utilisateur")

class NotificationWebsocket(Base):
    __tablename__ = "notifications_websocket"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    contenu = Column(Text, nullable=True)
    type = Column(String(20), nullable=True)
    date_heure = Column(DateTime(timezone=True), server_default=func.now())
    vu = Column(Boolean, default=False)

    utilisateur = relationship("Utilisateur", back_populates="notification")

class ParametresNotifications(Base):
    __tablename__ = "parametres_notifications"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    type_notification = Column(String(50), nullable=False)
    actif = Column(Boolean, default=True)

    utilisateur = relationship("Utilisateur", back_populates="parametres_notifications")

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    jeton_session = Column(String(255), unique=True, nullable=False)
    debut_session = Column(DateTime, nullable=False, default=datetime.utcnow)
    fin_session = Column(DateTime, nullable=True)
    adresse_ip = Column(String(45), nullable=True)

    utilisateur = relationship("Utilisateur", back_populates="sessions")

class Pays(Base):
    __tablename__ = "pays"

    id = Column(Integer, primary_key=True, index=True)
    code_iso = Column(String(3), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    continent = Column(String(50))
    aeroports = relationship("Aeroport", back_populates="pays", cascade="all, delete")

class Aeroport(Base):
    __tablename__ = "aeroports"

    id = Column(Integer, primary_key=True, index=True)
    code_oaci = Column(String(10), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    ville = Column(String(100))
    pays_id = Column(Integer, ForeignKey("pays.id"))
    description = Column(Text)

    pays = relationship("Pays", back_populates="aeroports")
    planifications = relationship("PlanificationNationale", back_populates="aeroport")

class HistoriqueVol(Base):
    __tablename__ = "historiques_vols"

    id = Column(Integer, primary_key=True, index=True)
    vol_id = Column(Integer, ForeignKey("vols.id"))
    numero_vol = Column(String(20))
    compagnie_id = Column(Integer, ForeignKey("compagnies.id"))
    avion_id = Column(Integer, ForeignKey("avions.id"))
    aeroport_depart = Column(String(10))
    aeroport_arrivee = Column(String(10))
    date_vol = Column(Date)

    sobt = Column(DateTime)
    tobt = Column(DateTime)
    hobt = Column(DateTime)
    eta = Column(DateTime)
    sta = Column(DateTime)
    atat = Column(DateTime)
    statut = Column(String(50))
    ctot = Column(DateTime)
    enregistrement_date = Column(DateTime, nullable=False)

    # Relations (si tu veux les objets associés)
    vol = relationship("Vol", back_populates="historiques")
    compagnie = relationship("Compagnie", back_populates="historiques_vols")
    avion = relationship("Avion", back_populates="historiques_vols")

class PrioriteSource(Base):
    __tablename__ = "priorites_source"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(100), unique=True, nullable=False)
    niveau_priorite = Column(Integer, nullable=False)
    description = Column(Text)

class PlanificationNationale(Base):
    __tablename__ = "planifications_nationales"
    id = Column(Integer, primary_key=True, index=True)
    date_planification = Column(Date, nullable=False)
    aeroport_id = Column(Integer, ForeignKey("aeroports.id"))
    capacite_maximale = Column(Integer, nullable=False)
    capacite_utilisee = Column(Integer)
    commentaires = Column(Text)

    # Relation vers Aeroport
    aeroport = relationship("Aeroport", back_populates="planifications")
