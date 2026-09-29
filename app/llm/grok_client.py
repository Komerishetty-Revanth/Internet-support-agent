import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class GrokClient:
    """Client for Grok API"""
    
    def __init__(self):
        self.api_key = os.getenv("GROK_API_KEY", "")
        self.api_url = "https://api.x.ai/v1/chat/completions"
        self.model = "grok-2-latest"
    
    async def send_message(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Send message to Grok API.
        
        Args:
            prompt: The prompt to send
            temperature: Creativity level (0-1)
            
        Returns:
            Response text from Grok
        """
        if not self.api_key:
            raise ValueError("GROK_API_KEY not set in environment")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 500
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Grok API error {response.status}: {error_text}")
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error communicating with Grok: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calling Grok API: {str(e)}")

# Global instance
grok_client = GrokClient()