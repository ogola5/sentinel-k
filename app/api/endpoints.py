from fastapi import APIRouter
from app.models.schemas import GraphResponse, Alert
from app.services.graph_service import generate_mock_graph, get_alerts
from typing import List

router = APIRouter()

@router.get("/graph", response_model=GraphResponse)
async def get_sovereign_graph():
    """
    Returns the National Threat Graph topology.
    Used by the Frontend 3D visualizer.
    """
    data = generate_mock_graph()
    return data

@router.get("/alerts", response_model=List[Alert])
async def get_threat_alerts():
    """
    Returns real-time AI alerts.
    """
    return get_alerts()