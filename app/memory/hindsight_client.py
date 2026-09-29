import os
import aiohttp
from dotenv import load_dotenv
from typing import Dict, List, Optional

load_dotenv()

class HindsightClient:
    """Client for Hindsight memory service"""
    
    def __init__(self):
        self.api_key = os.getenv("HINDSIGHT_API_KEY", "")
        self.api_url = "https://api.hindsight.ai/v1"
        self.enabled = bool(self.api_key)
    
    async def store_memory(self, customer_id: str, memory_type: str, content: str) -> bool:
        """
        Store memory about customer interaction.
        
        Args:
            customer_id: Customer identifier
            memory_type: Type of memory (issue, resolution, etc.)
            content: Memory content
            
        Returns:
            True if stored successfully, False otherwise
        """
        if not self.enabled:
            print(f"⚠️ Hindsight disabled. Memory not stored: {memory_type}")
            return False
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "customer_id": customer_id,
                "memory_type": memory_type,
                "content": content
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/memory/store",
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        print(f"✅ Memory stored: {memory_type}")
                        return True
                    else:
                        print(f"⚠️ Failed to store memory: {response.status}")
                        return False
        
        except Exception as e:
            print(f"⚠️ Hindsight error: {str(e)}")
            return False
    
    async def retrieve_memory(self, customer_id: str) -> List[Dict]:
        """
        Retrieve relevant memories for customer.
        
        Returns:
            List of relevant memories
        """
        if not self.enabled:
            return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_url}/memory/retrieve",
                    params={"customer_id": customer_id},
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("memories", [])
                    else:
                        return []
        
        except Exception as e:
            print(f"⚠️ Hindsight retrieval error: {str(e)}")
            return []


# Global instance
hindsight_client = HindsightClient()