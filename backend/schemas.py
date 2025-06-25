from pydantic import BaseModel
from typing import Optional, Any
from datetime import date, datetime

class VolBase(BaseModel):
    numero_vol: str
    compagnie_id: Optional[int]
    avion_id: Optional[int]
    type_vol: Optional[str]
    statut: Optional[str]
    aeroport_depart: Optional[str]
    aeroport_arrivee: Optional[str]
    porte_embarquement: Optional[str]
    poste_stationnement: Optional[str]
    date_vol: Optional[date]
    sobt: Optional[datetime]
    tobt: Optional[datetime]
    aobt: Optional[datetime]
    eta: Optional[datetime]
    ata: Optional[datetime]
    tsat: Optional[datetime]
    ctot: Optional[datetime]
    alertes: Optional[Any]

class VolCreate(VolBase):
    pass

class VolUpdate(VolBase):
    pass

class Vol(VolBase):
    id: int
    class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import Optional

class AvionBase(BaseModel):
    immatriculation: str
    type_avion: Optional[str] = None
    compagnie_id: Optional[int] = None
    capacite_sieges: Optional[int] = None
    capacite_fret: Optional[int] = None

class AvionCreate(AvionBase):
    immatriculation: str

class AvionUpdate(BaseModel):
    type_avion: Optional[str] = None
    compagnie_id: Optional[int] = None
    capacite_sieges: Optional[int] = None
    capacite_fret: Optional[int] = None

class Avion(AvionBase):
    id: int

    class Config:
        from_attributes = True  # pour la compatibilité SQLAlchemy <-> Pydantic

from pydantic import BaseModel

class CompagnieBase(BaseModel):
    nom: str
    code_oaci: str | None = None
    code_iata: str | None = None
    pays_origine: str | None = None

class CompagnieCreate(CompagnieBase):
    pass

class CompagnieUpdate(CompagnieBase):
    pass

class Compagnie(CompagnieBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel

class PorteEmbarquementBase(BaseModel):
    terminal: str
    nom_porte: str
    statut: str

class PorteEmbarquementCreate(PorteEmbarquementBase):
    pass

class PorteEmbarquementUpdate(BaseModel):
    terminal: Optional[str] = None
    nom_porte: Optional[str] = None
    statut: Optional[str] = None

class PorteEmbarquement(PorteEmbarquementBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PosteStationnementBase(BaseModel):
    numero_poste: str
    localisation: str
    statut: str
    debut_occupation: Optional[datetime]
    fin_occupation: Optional[datetime]

class PosteStationnementCreate(PosteStationnementBase):
    pass

class PosteStationnementUpdate(PosteStationnementBase):
    pass

class PosteStationnement(PosteStationnementBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlerteBase(BaseModel):
    vol_id: int
    type_alerte: str
    description: Optional[str] = None
    niveau: Optional[str] = None
    date_heure: Optional[datetime] = None
    statut: Optional[str] = None

class AlerteCreate(AlerteBase):
    pass

class AlerteUpdate(AlerteBase):
    pass

class Alerte(AlerteBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr
from typing import Optional

class UtilisateurBase(BaseModel):
    nom_complet: str
    email: EmailStr
    role_id: Optional[int] = None
    statut: Optional[str] = None

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class UtilisateurUpdate(BaseModel):
    nom_complet: Optional[str] = None
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None
    role_id: Optional[int] = None
    statut: Optional[str] = None

class Utilisateur(UtilisateurBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schéma de base pour Notification
class NotificationBase(BaseModel):
    utilisateur_id: int
    type: str
    contenu: Optional[str] = None
    date_heure: Optional[datetime] = None
    statut: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    type: Optional[str] = None
    contenu: Optional[str] = None
    date_heure: Optional[datetime] = None
    statut: Optional[str] = None

class Notification(NotificationBase):
    id: int
    utilisateur: Optional[Utilisateur] = None  # pour inclure l'utilisateur lié dans la réponse
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Any, Dict

class RoleBase(BaseModel):
    nom_role: str
    permissions: Optional[Dict[str, Any]] = None  # JSON = dict

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime

class MessageATFMBase(BaseModel):
    type_message: str
    vol_id: int
    contenu: Optional[Dict[str, Any]] = None  # JSONB = dict
    statut: Optional[str] = None
    date_emission: Optional[datetime] = None
    date_reception: Optional[datetime] = None

class MessageATFMCreate(MessageATFMBase):
    pass

class MessageATFMUpdate(BaseModel):
    type_message: Optional[str] = None
    contenu: Optional[Dict[str, Any]] = None
    statut: Optional[str] = None
    date_emission: Optional[datetime] = None
    date_reception: Optional[datetime] = None

class MessageATFM(MessageATFMBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MeteoBase(BaseModel):
    temperature: Optional[float] = None
    direction_vent: Optional[int] = None
    vitesse_vent: Optional[int] = None
    visibilite: Optional[int] = None
    rvr: Optional[int] = None
    humidite: Optional[float] = None
    pression_qnh: Optional[int] = None
    date_heure: Optional[datetime] = None

class MeteoCreate(MeteoBase):
    pass

class MeteoUpdate(MeteoBase):
    pass

class Meteo(MeteoBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class HistoriqueOperationBase(BaseModel):
    type_operation: str
    table_concernee: str
    details: Optional[Any]
    date_heure: datetime
    utilisateur_id: Optional[int]  # FK vers utilisateur

class HistoriqueOperationCreate(HistoriqueOperationBase):
    pass

class HistoriqueOperationUpdate(HistoriqueOperationBase):
    pass

class HistoriqueOperation(HistoriqueOperationBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class SourceDonneesBase(BaseModel):
    nom_source: str
    priorite: Optional[str] = None
    statut: Optional[str] = None

class SourceDonneesCreate(SourceDonneesBase):
    pass

class SourceDonneesUpdate(SourceDonneesBase):
    pass

class SourceDonnees(SourceDonneesBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SequenceDepartBase(BaseModel):
    vol_id: int
    ordre: Optional[int] = None
    tsat: Optional[datetime] = None
    demarrage_reel: Optional[datetime] = None
    statut: Optional[str] = None

class SequenceDepartCreate(SequenceDepartBase):
    pass

class SequenceDepartUpdate(SequenceDepartBase):
    pass

class SequenceDepart(SequenceDepartBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class CommunicationInterneBase(BaseModel):
    emetteur_id: int
    destinataires: Optional[List[int]] = None   # ou List[Any] si tu veux autoriser plus de souplesse
    contenu: Optional[str] = None
    date_heure: Optional[datetime] = None

class CommunicationInterneCreate(CommunicationInterneBase):
    pass

class CommunicationInterneUpdate(CommunicationInterneBase):
    pass

class CommunicationInterne(CommunicationInterneBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class ParametreSystemeBase(BaseModel):
    nom_parametre: str
    valeur: Optional[str] = None
    description: Optional[str] = None

class ParametreSystemeCreate(ParametreSystemeBase):
    pass

class ParametreSystemeUpdate(ParametreSystemeBase):
    pass

class ParametreSysteme(ParametreSystemeBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr
from typing import Optional

class OrganisationPartenaireBase(BaseModel):
    nom: str
    contact_principal: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None

class OrganisationPartenaireCreate(OrganisationPartenaireBase):
    pass

class OrganisationPartenaireUpdate(OrganisationPartenaireBase):
    pass

class OrganisationPartenaire(OrganisationPartenaireBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, List, Any

class GroupeCommunicationBase(BaseModel):
    nom_groupe: str
    description: Optional[str] = None
    membres: Optional[Any] = None  # Any ou List selon structure des membres

class GroupeCommunicationCreate(GroupeCommunicationBase):
    pass

class GroupeCommunicationUpdate(GroupeCommunicationBase):
    pass

class GroupeCommunication(GroupeCommunicationBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EvenementBase(BaseModel):
    nom: str
    description: Optional[str] = None
    date_debut: datetime
    date_fin: datetime
    statut: Optional[str] = None

class EvenementCreate(EvenementBase):
    pass

class EvenementUpdate(EvenementBase):
    pass

class Evenement(EvenementBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MilestoneBase(BaseModel):
    vol_id: int
    sobt: Optional[datetime] = None
    tobt: Optional[datetime] = None
    aobt: Optional[datetime] = None
    tsat: Optional[datetime] = None
    ctot: Optional[datetime] = None
    eta: Optional[datetime] = None
    ata: Optional[datetime] = None

class MilestoneCreate(MilestoneBase):
    pass

class MilestoneUpdate(MilestoneBase):
    pass

class Milestone(MilestoneBase):
    id: int
    mise_a_jour: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AuditLogBase(BaseModel):
    utilisateur_id: Optional[int] = None
    action: str
    cible: str
    cible_id: Optional[int] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    commentaire: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogUpdate(BaseModel):
    commentaire: Optional[str] = None

class AuditLog(AuditLogBase):
    id: int
    date_heure: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class TacheBase(BaseModel):
    type: str
    statut: str
    date_heure_demarrage: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    details: Optional[Any] = None

class TacheCreate(TacheBase):
    pass

class TacheUpdate(TacheBase):
    pass

class Tache(TacheBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    nom: str
    chemin_fichier: str
    type_document: str
    vol_id: Optional[int]
    ressource_id: Optional[int]
    utilisateur_id: Optional[int]

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    nom: Optional[str]
    chemin_fichier: Optional[str]
    type_document: Optional[str]
    vol_id: Optional[int]
    ressource_id: Optional[int]
    utilisateur_id: Optional[int]

class Document(DocumentBase):
    id: int
    date_heure_upload: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistoriqueEtatVolBase(BaseModel):
    vol_id: int
    ancien_statut: Optional[str] = None
    nouveau_statut: Optional[str] = None
    utilisateur_id: Optional[int] = None

class HistoriqueEtatVolCreate(HistoriqueEtatVolBase):
    pass

class HistoriqueEtatVolUpdate(BaseModel):
    ancien_statut: Optional[str] = None
    nouveau_statut: Optional[str] = None
    utilisateur_id: Optional[int] = None

class HistoriqueEtatVol(HistoriqueEtatVolBase):
    id: int
    date_heure_changement: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WebhookBase(BaseModel):
    url: str
    type_evenement: str
    actif: Optional[bool] = True
    details: Optional[dict] = None

class WebhookCreate(WebhookBase):
    pass

class WebhookUpdate(BaseModel):
    url: Optional[str] = None
    type_evenement: Optional[str] = None
    actif: Optional[bool] = None
    details: Optional[dict] = None

class Webhook(WebhookBase):
    id: int
    date_heure_creation: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class PersonnalisationUtilisateurBase(BaseModel):
    utilisateur_id: int
    parametre: str
    valeur: Optional[str] = None

class PersonnalisationUtilisateurCreate(PersonnalisationUtilisateurBase):
    pass

class PersonnalisationUtilisateurUpdate(BaseModel):
    parametre: Optional[str] = None
    valeur: Optional[str] = None

class PersonnalisationUtilisateur(PersonnalisationUtilisateurBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IncidentTechniqueBase(BaseModel):
    titre: str
    description: Optional[str] = None
    niveau_criticite: Optional[str] = None
    statut: Optional[str] = None
    utilisateur_id: Optional[int] = None
    vol_id: Optional[int] = None

class IncidentTechniqueCreate(IncidentTechniqueBase):
    pass

class IncidentTechniqueUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    niveau_criticite: Optional[str] = None
    statut: Optional[str] = None
    utilisateur_id: Optional[int] = None
    vol_id: Optional[int] = None

class IncidentTechnique(IncidentTechniqueBase):
    id: int
    date_heure: Optional[datetime]
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MaintenanceBase(BaseModel):
    ressource_id: int
    type: str
    date_heure_debut: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    commentaire: Optional[str] = None
    utilisateur_id: Optional[int] = None

class MaintenanceCreate(MaintenanceBase):
    pass

class MaintenanceUpdate(BaseModel):
    ressource_id: Optional[int] = None
    type: Optional[str] = None
    date_heure_debut: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    commentaire: Optional[str] = None
    utilisateur_id: Optional[int] = None

class Maintenance(MaintenanceBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class RessourceBase(BaseModel):
    type: str
    nom: str
    disponibilite: Optional[bool] = True
    details: Optional[dict] = None

class RessourceCreate(RessourceBase):
    pass

class RessourceUpdate(BaseModel):
    type: Optional[str] = None
    nom: Optional[str] = None
    disponibilite: Optional[bool] = None
    details: Optional[dict] = None

class Ressource(RessourceBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AffectationRessourceBase(BaseModel):
    vol_id: int
    ressource_id: int
    date_heure_debut: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    statut: Optional[str] = None
    notes: Optional[str] = None

class AffectationRessourceCreate(AffectationRessourceBase):
    pass

class AffectationRessourceUpdate(BaseModel):
    date_heure_debut: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    statut: Optional[str] = None
    notes: Optional[str] = None

class AffectationRessource(AffectationRessourceBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class LogSystemeBase(BaseModel):
    utilisateur_id: Optional[int]
    action: Optional[str]
    date_heure: Optional[datetime]
    ip: Optional[str]
    details: Optional[Dict[str, Any]]

class LogSystemeCreate(BaseModel):
    utilisateur_id: int
    action: str
    ip: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class LogSystemeUpdate(BaseModel):
    action: Optional[str] = None
    ip: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class LogSysteme(LogSystemeBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionAPOCBase(BaseModel):
    utilisateur_id: int
    date_heure_connexion: Optional[datetime] = None
    date_heure_deconnexion: Optional[datetime] = None
    statut: Optional[str] = None
    remarques: Optional[str] = None

class SessionAPOCCreate(SessionAPOCBase):
    pass

class SessionAPOCUpdate(SessionAPOCBase):
    pass

class SessionAPOC(SessionAPOCBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatAPOCBase(BaseModel):
    utilisateur_id: int
    message: str
    date_heure: Optional[datetime] = None
    session_apoc_id: int

class ChatAPOCCreate(ChatAPOCBase):
    pass

class ChatAPOCUpdate(BaseModel):
    message: Optional[str] = None
    date_heure: Optional[datetime] = None

class ChatAPOC(ChatAPOCBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlerteMeteoBase(BaseModel):
    type_alerte: str
    description: Optional[str] = None
    niveau_criticite: Optional[str] = None
    date_heure_debut: datetime
    date_heure_fin: datetime
    statut: Optional[str] = None

class AlerteMeteoCreate(AlerteMeteoBase):
    pass

class AlerteMeteoUpdate(BaseModel):
    type_alerte: Optional[str] = None
    description: Optional[str] = None
    niveau_criticite: Optional[str] = None
    date_heure_debut: Optional[datetime] = None
    date_heure_fin: Optional[datetime] = None
    statut: Optional[str] = None

class AlerteMeteo(AlerteMeteoBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Dict, Any

class PlanAeroportSVGBase(BaseModel):
    nom_element: str
    type_element: str
    id_svg: str
    statut: Optional[str] = None
    vol_id: Optional[int] = None
    coordonnees: Optional[Dict[str, Any]]

class PlanAeroportSVGCreate(PlanAeroportSVGBase):
    pass

class PlanAeroportSVGUpdate(PlanAeroportSVGBase):
    pass

class PlanAeroportSVG(PlanAeroportSVGBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SlotATFMBase(BaseModel):
    vol_id: int
    ctot: Optional[datetime] = None
    type_slot: Optional[str] = None
    date_heure_attribution: Optional[datetime] = None
    statut: Optional[str] = None
    commentaire: Optional[str] = None

class SlotATFMCreate(SlotATFMBase):
    pass

class SlotATFMUpdate(SlotATFMBase):
    pass

class SlotATFM(SlotATFMBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class IntegrationSystemesExternesBase(BaseModel):
    systeme_externe: str
    endpoint: str
    protocole: str
    details: Optional[Dict[str, Any]] = None

class IntegrationSystemesExternesCreate(IntegrationSystemesExternesBase):
    pass

class IntegrationSystemesExternesUpdate(IntegrationSystemesExternesBase):
    pass

class IntegrationSystemesExternes(IntegrationSystemesExternesBase):
    id: int
    date_heure: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GanttSequencementBase(BaseModel):
    vol_id: int
    debut: datetime
    fin: datetime
    ordre: int
    statut: str

class GanttSequencementCreate(GanttSequencementBase):
    pass

class GanttSequencementUpdate(BaseModel):
    debut: Optional[datetime]
    fin: Optional[datetime]
    ordre: Optional[int]
    statut: Optional[str]

class GanttSequencement(GanttSequencementBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class GestionDroitsUtilisateursBase(BaseModel):
    utilisateur_id: int
    permission: str
    statut: bool

class GestionDroitsUtilisateursCreate(GestionDroitsUtilisateursBase):
    pass

class GestionDroitsUtilisateursUpdate(BaseModel):
    permission: Optional[str]
    statut: Optional[bool]

class GestionDroitsUtilisateurs(GestionDroitsUtilisateursBase):
    id: int
    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationWebsocketBase(BaseModel):
    utilisateur_id: int
    contenu: Optional[str] = None
    type: Optional[str] = None

class NotificationWebsocketCreate(NotificationWebsocketBase):
    pass

class NotificationWebsocketUpdate(BaseModel):
    contenu: Optional[str]
    type: Optional[str]
    vu: Optional[bool]

class NotificationWebsocketOut(NotificationWebsocketBase):
    id: int
    date_heure: datetime
    vu: bool

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class ParametresNotificationsBase(BaseModel):
    utilisateur_id: int
    type_notification: str
    actif: Optional[bool] = True

class ParametresNotificationsCreate(ParametresNotificationsBase):
    pass

class ParametresNotificationsUpdate(BaseModel):
    type_notification: Optional[str]
    actif: Optional[bool]

class ParametresNotificationsOut(ParametresNotificationsBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionBase(BaseModel):
    utilisateur_id: int
    jeton_session: str
    debut_session: Optional[datetime] = None
    fin_session: Optional[datetime] = None
    adresse_ip: Optional[str] = None

class SessionCreate(SessionBase):
    jeton_session: str
    utilisateur_id: int
    adresse_ip: Optional[str]

class SessionUpdate(BaseModel):
    fin_session: Optional[datetime]
    adresse_ip: Optional[str]

class SessionOut(SessionBase):
    id: int

    class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import Optional

class PaysBase(BaseModel):
    code_iso: str
    nom: str
    continent: Optional[str] = None

class PaysCreate(PaysBase):
    pass

class PaysUpdate(BaseModel):
    nom: Optional[str]
    continent: Optional[str]

class PaysOut(PaysBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional

class AeroportBase(BaseModel):
    code_oaci: str
    nom: str
    ville: Optional[str] = None
    pays_id: Optional[int] = None
    description: Optional[str] = None

class AeroportCreate(AeroportBase):
    pass

class AeroportUpdate(AeroportBase):
    pass

class AeroportOut(AeroportBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class HistoriqueVolBase(BaseModel):
    vol_id: Optional[int] = None
    numero_vol: Optional[str] = None
    compagnie_id: Optional[int] = None
    avion_id: Optional[int] = None
    aeroport_depart: Optional[str] = None
    aeroport_arrivee: Optional[str] = None
    date_vol: Optional[date] = None
    sobt: Optional[datetime] = None
    tobt: Optional[datetime] = None
    hobt: Optional[datetime] = None
    eta: Optional[datetime] = None
    sta: Optional[datetime] = None
    atat: Optional[datetime] = None
    statut: Optional[str] = None
    ctot: Optional[datetime] = None

class HistoriqueVolCreate(HistoriqueVolBase):
    pass

class HistoriqueVolUpdate(HistoriqueVolBase):
    pass

class HistoriqueVolOut(HistoriqueVolBase):
    id: int
    enregistrement_date: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel

class PrioriteSourceBase(BaseModel):
    source: str
    niveau_priorite: int
    description: str | None = None

class PrioriteSourceCreate(PrioriteSourceBase):
    pass

class PrioriteSourceUpdate(PrioriteSourceBase):
    pass

class PrioriteSourceInDBBase(PrioriteSourceBase):
    id: int

    class Config:
        orm_mode = True

class PrioriteSource(PrioriteSourceInDBBase):
    pass

from pydantic import BaseModel
from datetime import date
from typing import Optional

class PlanificationNationaleBase(BaseModel):
    date_planification: date
    aeroport_id: int
    capacite_maximale: int
    capacite_utilisee: Optional[int] = None
    commentaires: Optional[str] = None

class PlanificationNationaleCreate(PlanificationNationaleBase):
    pass

class PlanificationNationaleUpdate(PlanificationNationaleBase):
    pass

class PlanificationNationaleInDBBase(PlanificationNationaleBase):
    id: int
    class Config:
        orm_mode = True

class PlanificationNationale(PlanificationNationaleInDBBase):
    pass