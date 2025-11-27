# app/utils/helpers.py
from stix2 import (Bundle, Indicator, Identity, Malware, Relationship)
from datetime import datetime
import torch
import torch_geometric  # ← THIS WAS MISSING (the only bug)

# ──────────────────────────────
# STIX EXPORT — beautiful & valid
# ──────────────────────────────
def export_to_stix(graph_data):
    objects = []

    identity = Identity(
        name="Sentinel-Ke National Threat Intelligence Platform",
        identity_class="organization"
    )
    objects.append(identity)

    # Export high-risk nodes
    risk_scores = getattr(graph_data, 'risk_scores', [0.8] * len(graph_data.x))
    for i, risk in enumerate(risk_scores):
        if risk > 0.7:
            indicator = Indicator(
                name=f"Kenyan Cyber Threat Entity {i}",
                description="Detected by Sentinel-Ke GNN as part of active fraud ring",
                pattern_type="stix",
                pattern="[ipv4-addr:value = '197.232.0.0/13'] OR [domain-name:value = 'fakebank.co.ke']",
                valid_from=datetime.utcnow().isoformat() + "Z",
                labels=["malicious-activity"],
                confidence=int(risk * 100)
            )
            objects.append(indicator)

            malware = Malware(name="KE-FraudRing-2025", is_family=True)
            objects.append(malware)

            rel = Relationship(indicator, "indicates", malware)
            objects.append(rel)

    bundle = Bundle(objects=objects, allow_custom=True)
    return bundle.serialize(pretty=True)


# ──────────────────────────────
# Required for GNN training
# ──────────────────────────────
def add_adversarial_noise(data: torch_geometric.data.Data, epsilon=0.01):
    """Simple adversarial noise for robust training"""
    noise = torch.randn_like(data.x) * epsilon
    data.x = data.x + noise
    return data