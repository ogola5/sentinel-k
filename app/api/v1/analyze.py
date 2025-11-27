from fastapi import APIRouter, Depends
from app.models.schemas import ThreatInput, PredictionOutput
from app.services.threat_analyzer import ThreatAnalyzer
from app.utils.helpers import export_to_stix

router = APIRouter(prefix="/analyze", tags=["analyze"])

analyzer = ThreatAnalyzer()  # Dependency if needed

@router.post("/predict", response_model=PredictionOutput)
def predict_threat(input: ThreatInput):
    # Mock: Add to graph, analyze
    graph_data = analyzer.load_graph()  # From Neo4j
    result = analyzer.analyze(graph_data)
    return PredictionOutput(**result)

@router.get("/cluster")
def get_clusters():
    graph_data = analyzer.load_graph()
    result = analyzer.analyze(graph_data)
    return {"clusters": result["clusters"]}

@router.get("/risk-score/{entity_id}")
def get_risk_score(entity_id: str):
    graph_data = analyzer.load_graph()
    # Mock index
    idx = 0  # Find by id
    return {"risk_score": analyzer.analyze(graph_data)["risk_scores"][idx]}

@router.get("/export-stix")
def export_stix():
    graph_data = analyzer.load_graph()
    stix_bundle = export_to_stix(graph_data)
    return stix_bundle