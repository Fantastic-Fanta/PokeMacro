from typing import Optional

import requests


def send_discord_webhook(webhook_url: str, message: str, username: Optional[str] = None) -> bool:
    if not webhook_url or not webhook_url.strip():
        return False
    
    try:
        response = requests.post(
            webhook_url,
            json={"content": message, "username": username or "Poopimon Notifier"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in (200, 204):
            return True
        
        print(f"Discord webhook error: {response.status_code} - {response.text}")
        return False
            
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord webhook: {e}")
        return False

