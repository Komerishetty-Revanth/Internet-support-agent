from app.agent.workflows import get_workflow, get_current_step, get_step_count
from app.database.models import TroubleshootingStage

class Troubleshooter:
    """Manages troubleshooting workflow"""
    
    @staticmethod
    def get_next_question(issue_category: str, current_step: int) -> str:
        """Get the next troubleshooting question"""
        step = get_current_step(issue_category, current_step)
        if step:
            return step.question
        return "Thank you for your patience. Let me review our findings."
    
    @staticmethod
    def get_hint(issue_category: str, current_step: int) -> str:
        """Get hint for current step"""
        step = get_current_step(issue_category, current_step)
        if step and step.hint:
            return step.hint
        return ""
    
    @staticmethod
    def should_escalate(issue_category: str, current_step: int) -> bool:
        """Determine if issue should be escalated"""
        total_steps = get_step_count(issue_category)
        # Escalate if we've gone through all steps without resolution
        return current_step >= total_steps
    
    @staticmethod
    def get_escalation_reason(issue_category: str) -> str:
        """Get reason for escalation"""
        reasons = {
            "NO_INTERNET": "Internet remains offline after troubleshooting. May require ISP technician or hardware replacement.",
            "SLOW_INTERNET": "Speed issue persists despite troubleshooting. May be ISP limitation or line issue.",
            "WIFI_NO_INTERNET": "Wi-Fi connectivity issue unresolved. May need router service or configuration.",
            "INTERMITTENT": "Disconnections continue. Requires deeper investigation or ISP involvement.",
            "ROUTER_PROBLEM": "Router malfunction confirmed. May need replacement or professional service.",
            "CABLE_PROBLEM": "Cable damage confirmed or suspected. Physical replacement needed.",
            "DEVICE_PROBLEM": "Device connectivity issue unresolved. May need device repair or professional support.",
            "NETWORK_CONFIGURATION": "Configuration issue requires advanced technical support.",
            "POSSIBLE_ISP_PROBLEM": "Issue appears to be with ISP service. Contact your ISP support team.",
        }
        return reasons.get(issue_category, "Issue requires escalation to technical support team.")

troubleshooter = Troubleshooter()