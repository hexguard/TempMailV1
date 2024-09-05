# temp_mail_api.py
import httpx
import os
import logging
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://fresedgpt.space/v1"
API_KEY = os.getenv("API_KEY")

logger = logging.getLogger(__name__)

TIMEOUT = 10  # Timeout in seconds

async def generate_temp_mail():
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {}  # Empty JSON payload
        try:
            response = await client.post(f"{BASE_URL}/temp_mail/generate", headers=headers, json=payload, timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Generated temp mail: {data['email']}")
                return data["email"], data["identifier"]
            else:
                logger.error(f"Failed to generate temp mail: {response.text}")
                return None, None
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting: {exc}")
            return None, None

async def get_temp_mail_messages(identifier):
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        try:
            response = await client.get(f"{BASE_URL}/temp_mail/messages/{identifier}", headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                messages = response.json()["messages"]
                logger.info(f"Retrieved {len(messages)} messages")
                return messages
            else:
                logger.error(f"Failed to retrieve messages: {response.text}")
                return None
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting: {exc}")
            return None