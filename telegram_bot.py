"""
Komara Agency — Bot Telegram (connecteur)
Polling long-getUpdates, zéro dépendance lourde.
Démarré automatiquement par app.py si TELEGRAM_BOT_TOKEN est défini.
Ne dit jamais que c'est un robot : ton humain de l'équipe Komara Agency.
"""

import os
import time
import logging
import threading

import requests

logger = logging.getLogger("komara.telegram")

API = "https://api.telegram.org"
WHATSAPP = "https://wa.me/212701986219"
PORTFOLIO = "https://ndinekomara2442-cmd.github.io/komara-agency-portfolio/"

WELCOME = (
    "Salut ! 👋 Bienvenue chez Komara Agency 🇬🇳\n\n"
    "On transforme ta vision en visuels pro : logos, affiches, retouches, "
    "vidéos, bots IA et agents d'automatisation.\n\n"
    "Tape /tarifs pour voir nos offres, ou écris-nous directement sur WhatsApp 👇"
)

TARIFS = (
    "Nos tarifs (en €) 💼\n\n"
    "• Visuels pro : à partir de 5 €\n"
    "• Logo : 80 €\n"
    "• Packs visuels : 120 € / 350 €\n"
    "• Sites web : 150 € à 550 €\n"
    "• Bots (WhatsApp, Telegram, TikTok) : 99 € à 300 €\n"
    "• Formation : 150 €\n\n"
    "Service express 24h : +30 %\n"
    "2 révisions offertes sur chaque commande ✨"
)

CONTACT = (
    "On est dispo 7j/7 ! 😊\n\n"
    f"WhatsApp : {WHATSAPP}\n"
    f"Portfolio : {PORTFOLIO}\n\n"
    "Envoie ton brief et on revient vers toi très vite 🚀"
)

DEFAULT = (
    "Merci pour ton message ! 🙏\n\n"
    "Pour qu'on te réponde au mieux : dis-nous ce que tu veux créer "
    "(logo, affiche, bot, vidéo...) et on s'occupe du reste.\n\n"
    "Tu peux aussi nous joindre direct sur WhatsApp 👇"
)


def keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "💬 WhatsApp", "url": WHATSAPP},
                {"text": "🎨 Portfolio", "url": PORTFOLIO},
            ]
        ]
    }


def _api(token, method, payload=None):
    r = requests.post(f"{API}/bot{token}/{method}", json=payload, timeout=25)
    r.raise_for_status()
    return r.json().get("result")


def reply(token, chat_id, text):
    _api(token, "sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": keyboard(),
        "parse_mode": "HTML",
    })


def handle_update(token, update):
    message = update.get("message")
    if not message:
        return
    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip().lower()

    if text.startswith("/start"):
        reply(token, chat_id, WELCOME)
    elif text.startswith("/tarifs"):
        reply(token, chat_id, TARIFS)
    elif text.startswith("/contact"):
        reply(token, chat_id, CONTACT)
    else:
        reply(token, chat_id, DEFAULT)


def start_polling():
    """Boucle de polling en arrière-plan. Retourne le thread démarré."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        logger.warning("TELEGRAM_BOT_TOKEN absent : bot Telegram inactif.")
        return None

    def loop():
        offset = 0
        logger.info("Bot Telegram Komara Agency démarré.")
        while True:
            try:
                updates = _api(token, "getUpdates", {
                    "offset": offset,
                    "timeout": 25,
                    "allowed_updates": ["message"],
                }) or []
                for update in updates:
                    offset = max(offset, update["update_id"] + 1)
                    handle_update(token, update)
            except requests.RequestException:
                logger.warning("Telegram injoignable, nouvelle tentative dans 5s.")
                time.sleep(5)
            except Exception:
                logger.exception("Erreur inattendue du bot Telegram.")
                time.sleep(5)

    thread = threading.Thread(target=loop, daemon=True, name="telegram-bot")
    thread.start()
    return thread
