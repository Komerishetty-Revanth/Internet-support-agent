from enum import Enum
from app.llm.grok_client import grok_client
from app.agent.prompts import CLASSIFICATION_PROMPT

class IssueCategory(str, Enum):
    """Allowed issue categories"""
    NO_INTERNET = "NO_INTERNET"
    SLOW_INTERNET = "SLOW_INTERNET"
    WIFI_NO_INTERNET = "WIFI_NO_INTERNET"
    INTERMITTENT = "INTERMITTENT"
    ROUTER_PROBLEM = "ROUTER_PROBLEM"
    CABLE_PROBLEM = "CABLE_PROBLEM"
    DEVICE_PROBLEM = "DEVICE_PROBLEM"
    NETWORK_CONFIGURATION = "NETWORK_CONFIGURATION"
    POSSIBLE_ISP_PROBLEM = "POSSIBLE_ISP_PROBLEM"
    UNKNOWN = "UNKNOWN"

VALID_CATEGORIES = [cat.value for cat in IssueCategory]

async def classify_issue(user_message: str) -> str:
    """
    Classify user message into an issue category.
    
    Args:
        user_message: Customer's description of the problem
        
    Returns:
        One of the valid issue categories
    """
    try:
        # Use Grok to classify
        prompt = CLASSIFICATION_PROMPT.format(user_message=user_message)
        response = await grok_client.send_message(prompt)
        
        # Extract category from response
        category = response.strip().upper()
        
        # Validate against allowed categories
        if category not in VALID_CATEGORIES:
            # If invalid, default to UNKNOWN
            return "UNKNOWN"
        
        return category
        
    except Exception as e:
        print(f"Classification error: {e}")
        return "UNKNOWN"

def is_valid_category(category: str) -> bool:
    """Check if category is valid"""
    return category.upper() in VALID_CATEGORIES