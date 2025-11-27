import random

def generate_mock_graph():
    """
    Generates a fake crime ring for the demo.
    Target: 'John Kamau' laundering money to 'Skyline Ventures'.
    """
    nodes = []
    links = []

    # 1. The High Risk Core
    nodes.append({"id": "P_001", "group": "Person", "label": "John Kamau", "risk_score": 0.95})
    nodes.append({"id": "C_550", "group": "Company", "label": "Skyline Ventures", "risk_score": 0.88})
    nodes.append({"id": "IP_99", "group": "IP", "label": "192.168.1.105", "risk_score": 0.70})
    
    links.append({"source": "P_001", "target": "C_550", "type": "DIRECTOR_OF"})
    links.append({"source": "P_001", "target": "IP_99", "type": "LOGGED_IN_FROM"})
    links.append({"source": "C_550", "target": "IP_99", "type": "HOSTED_AT"})

    # 2. Add some 'Noise' (Normal people)
    for i in range(5):
        p_id = f"P_00{i+2}"
        nodes.append({"id": p_id, "group": "Person", "label": f"Citizen {i}", "risk_score": 0.1})
        # Link them randomly to John Kamau (Transactions)
        if i % 2 == 0:
            links.append({"source": "P_001", "target": p_id, "type": "SENT_MPESA"})

    return {"nodes": nodes, "links": links}

def get_alerts():
    return [
        {"id": "A1", "severity": "HIGH", "message": "Circular Trading Detected", "entity_id": "C_550"},
        {"id": "A2", "severity": "MEDIUM", "message": "Multiple IDs from single IP", "entity_id": "IP_99"}
    ]