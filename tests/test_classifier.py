from app.agent.classifier import is_valid_category

def test_valid_category():
    """Test valid category checking"""
    assert is_valid_category("NO_INTERNET") is True
    assert is_valid_category("SLOW_INTERNET") is True
    assert is_valid_category("UNKNOWN") is True
    assert is_valid_category("INVALID_CATEGORY") is False

def test_all_valid_categories():
    """Test all valid categories exist"""
    categories = [
        "NO_INTERNET",
        "SLOW_INTERNET",
        "WIFI_NO_INTERNET",
        "INTERMITTENT",
        "ROUTER_PROBLEM",
        "CABLE_PROBLEM",
        "DEVICE_PROBLEM",
        "NETWORK_CONFIGURATION",
        "POSSIBLE_ISP_PROBLEM",
        "UNKNOWN"
    ]
    for cat in categories:
        assert is_valid_category(cat) is True