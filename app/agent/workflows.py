from typing import List, Dict

class TroubleshootingStep:
    """Single troubleshooting step"""
    def __init__(self, step_num: int, question: str, hint: str = ""):
        self.step_num = step_num
        self.question = question
        self.hint = hint

# Define workflows for each issue category
TROUBLESHOOTING_WORKFLOWS = {
    "NO_INTERNET": [
        TroubleshootingStep(1, "Is your router powered on? (yes/no)", "Check if the router has a power light indicator."),
        TroubleshootingStep(2, "Are the WAN/Internet indicator lights on or red? (on/red/off)", "Look for the WAN, Internet, or Status light on your router."),
        TroubleshootingStep(3, "Is the cable connected to the WAN port? (yes/no)", "Check that the network cable is firmly plugged into the WAN port."),
        TroubleshootingStep(4, "Can you restart your router? (yes/no)", "Unplug the router for 30 seconds, then plug it back in."),
        TroubleshootingStep(5, "Is the internet working now? (yes/no)", "Test by opening a website."),
        TroubleshootingStep(6, "Can you test from another device? (yes/no)", "Try another phone, laptop, or computer."),
    ],
    
    "SLOW_INTERNET": [
        TroubleshootingStep(1, "Are ALL devices slow or just one? (all/one)", "Test from multiple devices if possible."),
        TroubleshootingStep(2, "What is your Wi-Fi signal strength? (excellent/good/fair/poor)", "Check the Wi-Fi signal bars on your device."),
        TroubleshootingStep(3, "Is the router close to your device? (yes/no)", "Move closer to the router to test."),
        TroubleshootingStep(4, "Can you restart the router? (yes/no)", "Unplug for 30 seconds, then reconnect."),
        TroubleshootingStep(5, "Is the speed better now? (yes/no)", "Test speed after restart."),
        TroubleshootingStep(6, "Does this happen consistently? (always/sometimes/rarely)", "Check if the slowness is constant or intermittent."),
    ],
    
    "WIFI_NO_INTERNET": [
        TroubleshootingStep(1, "Is the device connected to the correct Wi-Fi network? (yes/no)", "Check the Wi-Fi network name in your device settings."),
        TroubleshootingStep(2, "Can you forget the network and reconnect? (yes/no)", "Go to Wi-Fi settings, forget the network, and rejoin."),
        TroubleshootingStep(3, "Is Wi-Fi on the router enabled? (yes/no)", "Check if the Wi-Fi light is on the router."),
        TroubleshootingStep(4, "Can you restart the router? (yes/no)", "Unplug for 30 seconds and reconnect."),
        TroubleshootingStep(5, "Can you test from another device? (yes/no)", "Try connecting another phone or device."),
        TroubleshootingStep(6, "Is the internet working now? (yes/no)", "Test if the connection is restored."),
    ],
    
    "INTERMITTENT": [
        TroubleshootingStep(1, "How often does it disconnect? (hourly/daily/multiple times daily)", "Help us understand the frequency."),
        TroubleshootingStep(2, "Does it affect all devices? (yes/no)", "Check if it's network-wide or device-specific."),
        TroubleshootingStep(3, "Have you checked the router temperature? (yes/no)", "Overheating can cause disconnections. Ensure proper ventilation."),
        TroubleshootingStep(4, "Can you restart the router? (yes/no)", "Unplug for 30 seconds, then reconnect."),
        TroubleshootingStep(5, "Check for loose cables. (done/yes/no)", "Ensure all cables are firmly connected."),
        TroubleshootingStep(6, "Has the disconnection stopped? (yes/no)", "Monitor for the next few hours."),
    ],
    
    "ROUTER_PROBLEM": [
        TroubleshootingStep(1, "Is the router powered on? (yes/no)", "Check power light indicator."),
        TroubleshootingStep(2, "Are there any error lights? (yes/no)", "Look for red or blinking error lights."),
        TroubleshootingStep(3, "Can you check the ventilation around the router? (yes/no)", "Ensure it's not blocked or overheating."),
        TroubleshootingStep(4, "Can you try restarting the router? (yes/no)", "Unplug for 1 minute, then reconnect."),
        TroubleshootingStep(5, "Have you tried a factory reset? (yes/no)", "Hold reset button for 10 seconds (if needed)."),
        TroubleshootingStep(6, "Is the router working now? (yes/no)", "If not, it may need replacement or repair."),
    ],
    
    "CABLE_PROBLEM": [
        TroubleshootingStep(1, "Can you visually inspect the cable? (yes/no)", "Look for cuts, bends, or damage."),
        TroubleshootingStep(2, "Can you reconnect the cable firmly? (yes/no)", "Unplug and reconnect at both ends."),
        TroubleshootingStep(3, "Is there visible damage or corrosion? (yes/no)", "Check connectors and cable insulation."),
        TroubleshootingStep(4, "Do you have another cable to test? (yes/no)", "Try a different cable if available."),
        TroubleshootingStep(5, "Does a new cable fix the issue? (yes/no)", "If yes, replace the damaged cable."),
        TroubleshootingStep(6, "Is the connection stable now? (yes/no)", "Test for 10 minutes to confirm."),
    ],
    
    "DEVICE_PROBLEM": [
        TroubleshootingStep(1, "Can other devices connect to the network? (yes/no)", "Test with another phone, laptop, or tablet."),
        TroubleshootingStep(2, "Does the problem device show the network? (yes/no)", "Check if the Wi-Fi network is visible."),
        TroubleshootingStep(3, "Can you forget and rejoin the network? (yes/no)", "In settings, forget the network and reconnect."),
        TroubleshootingStep(4, "Have you restarted the device? (yes/no)", "Power off and back on."),
        TroubleshootingStep(5, "Have you updated the device drivers/OS? (yes/no)", "Check for available updates."),
        TroubleshootingStep(6, "Can the device connect now? (yes/no)", "Test internet access."),
    ],
    
    "NETWORK_CONFIGURATION": [
        TroubleshootingStep(1, "Do you know your router's IP address? (yes/no)", "Usually 192.168.1.1 or 192.168.0.1"),
        TroubleshootingStep(2, "Have you checked DHCP settings? (yes/no)", "DHCP should be enabled on the router."),
        TroubleshootingStep(3, "Are DNS settings correct? (yes/no)", "Try using 8.8.8.8 or 1.1.1.1 as DNS."),
        TroubleshootingStep(4, "Can you restart the router? (yes/no)", "A restart can refresh network settings."),
        TroubleshootingStep(5, "Has the network stabilized? (yes/no)", "Check if devices can access the internet."),
        TroubleshootingStep(6, "Should we escalate to advanced support? (yes/no)", "This may need professional configuration help."),
    ],
    
    "POSSIBLE_ISP_PROBLEM": [
        TroubleshootingStep(1, "Have you checked your ISP's service status? (yes/no)", "Visit your ISP's website or call them."),
        TroubleshootingStep(2, "Are there outages reported in your area? (yes/no)", "Check local ISP outage maps."),
        TroubleshootingStep(3, "Is your internet bill current? (yes/no)", "Account suspension could cause outages."),
        TroubleshootingStep(4, "Can you contact your ISP support? (yes/no)", "They may need to check the line."),
        TroubleshootingStep(5, "Has your ISP confirmed the issue? (yes/no)", "They may send a technician."),
        TroubleshootingStep(6, "What did they recommend? (escalate/wait/action)", "Follow ISP recommendations."),
    ],

        "UNKNOWN": [
        TroubleshootingStep(1, "Are you able to connect to the internet at all? (yes/no)", "Try opening a website."),
        TroubleshootingStep(2, "Is the router powered on? (yes/no)", "Check for power light."),
        TroubleshootingStep(3, "Are the internet lights on the router? (yes/no/red)", "Look at the WAN/Internet indicator."),
        TroubleshootingStep(4, "Can you restart your router? (yes/no)", "Unplug for 30 seconds, then reconnect."),
        TroubleshootingStep(5, "Does this help? (yes/no)", "Check if internet works now."),
    ],

}

def get_workflow(issue_category: str) -> List[TroubleshootingStep]:
    """Get workflow steps for an issue category"""
    return TROUBLESHOOTING_WORKFLOWS.get(issue_category, [])

def get_step_count(issue_category: str) -> int:
    """Get total steps for a category"""
    return len(get_workflow(issue_category))

def get_current_step(issue_category: str, current_step_num: int) -> TroubleshootingStep:
    """Get a specific step"""
    workflow = get_workflow(issue_category)
    if 0 <= current_step_num < len(workflow):
        return workflow[current_step_num]
    return None