from pydantic import BaseModel

class ThreatInput(BaseModel):
    entities: list[dict]  # e.g., {'id': 'ent_001', 'type': 'IP', ...}

class PredictionOutput(BaseModel):
    risk_scores: list[float]
    clusters: list[int]
    anomalies: list[int]