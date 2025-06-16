# ✈️ LOMÉ A-CDM/ATFM Plateforme Collaborative

![Statut build](https://img.shields.io/badge/build-passing-brightgreen)  
![Licence](https://img.shields.io/badge/licence-MIT-blue)  
![Tech-Stack](https://img.shields.io/badge/FastAPI-React-blueviolet)


## 📢 Présentation

Cette application est la première plateforme de gestion collaborative A-CDM/ATFM pour l’aéroport de Lomé (Togo).  
Elle centralise la gestion :
- des vols (suivi, édition, séquencement)
- des ressources (stands, pistes, équipes…)
- des alertes (slot, météo, DPI/FUM…)
- de la météo en temps réel
- de la supervision collaborative (chat, logs, notifications)
- du reporting et des statistiques

**Objectif** : Fluidifier la coordination entre APOC, compagnies, handlers, contrôle aérien, administration aéroportuaire.

---

## 🌳 Arborescence du projet

lome-acdm-atfm/
│
├── backend/ # FastAPI, WebSocket, PostgreSQL
│ ├── main.py
│ ├── models.py
│ ├── routers/
│ ├── requirements.txt
│ └── ...
│
├── frontend/ # React, Tailwind, Dashboard
│ ├── src/
│ │ ├── components/
│ │ ├── App.js
│ │ ├── index.js
│ │ └── ...
│ ├── public/
│ └── ...
│
├── docker-compose.yml
├── README.md
└── docs/



---

## ⚡️ Démarrage rapide

**1. Cloner le dépôt**
```sh
git clone https://github.com/Illana672/lome-acdm-atfm.git
cd lome-acdm-atfm
2. Backend (API FastAPI)

sh
Copier
Modifier
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
Pour la configuration BDD : adapter .env

3. Frontend (React)

sh
Copier
Modifier
cd ../frontend
npm install
npm start
4. Déploiement complet (avec Docker)

sh
Copier
Modifier
docker-compose up --build
Voir aussi les scripts de seed pour données de test.

🔑 Fonctionnalités principales
Tableau de bord temps réel : tous les vols, stats, couleurs, milestones, filtres, export PDF/Excel

WebSocket : notifications live (retards, météo, affectations…)

Gestion utilisateur : rôles, droits, JWT, invitations/email, reset mot de passe

Ressources & affectations : stands, parkings, Gantt, drag & drop

Alertes/DPI/FUM : messages ATFM, popups, badges, logs d’audit, reporting

Météo : table dédiée, overlay SVG sur la carte, historique

Dashboard stats : KPIs, graphiques, taux de ponctualité, exports

Mode APOC mobile : QR code, notifications silencieuses, prise de contrôle

Documentation API : Swagger (http://localhost:8000/docs)

📸 Aperçu (screenshots à compléter)
Tableau de bord

Carte tarmac SVG

Panel notifications

🛠 Stack technique
Backend : FastAPI, SQLAlchemy, PostgreSQL, WebSocket

Frontend : React, Tailwind CSS, shadcn/ui, Material UI, lucide-react

DevOps : Docker, docker-compose, tests Pytest/Jest/Cypress

📚 Documentation
API : http://localhost:8000/docs

Guide d’installation détaillé : docs/installation.md

Dumps de base et scripts init : dossier /backend/scripts/

CI/CD, scénarios de tests : à venir (/.github/workflows/)

🙋 Support et Contributeurs
Auteur principal : Illana Feussa

Contributions ouvertes (issues/pull requests bienvenues)

Pour toute question : feuslana@gmail.com

📄 Licence
MIT — Utilisation libre pour la communauté aéroportuaire togolaise.