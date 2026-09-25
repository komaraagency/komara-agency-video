# Komara Agency — Vitrine + Bot Telegram 🇬🇳

Application web déployable sur **Railway** :
- Page vitrine du scénario vidéo publicitaire (style noir & doré Komara)
- Bot Telegram intégré (démarré automatiquement si le token est fourni)

## Déploiement sur Railway

1. Ouvre [railway.app](https://railway.app) et clique sur **New Project → Deploy from GitHub repo**
2. Sélectionne ce repository
3. Dans **Variables**, ajoute :
   - `TELEGRAM_BOT_TOKEN` : le token de ton bot [@BotFather](https://t.me/BotFather)
4. Railway détecte le `Dockerfile` et déploie automatiquement
5. Vérifie la santé du service sur `https://ton-app.up.railway.app/health`

## Variables d'environnement

| Variable | Obligatoire | Description |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Non | Active le bot Telegram si défini |
| `PORT` | Auto | Port fourni par Railway |

## Endpoints

- `GET /` — Page vitrine Komara Agency
- `GET /health` — Statut de l'application

## Commandes du bot Telegram

- `/start` — Message de bienvenue
- `/tarifs` — Nos tarifs en €
- `/contact` — WhatsApp et portfolio
