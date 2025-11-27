import torch
from torch_geometric.nn import GCNConv, GATConv  # For basic temporal, use GAT with time features
from torch_geometric.data import Data
from sklearn.ensemble import IsolationForest
from hdbscan import HDBSCAN
import numpy as np
from app.utils.helpers import add_adversarial_noise

class TemporalGNN(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super().__init__()
        self.conv1 = GATConv(num_features + 1, 16)  # +1 for time feature (normalized timestamp)
        self.conv2 = GATConv(16, num_classes)

    def forward(self, data):
        x = torch.cat([data.x, data.time.unsqueeze(1)], dim=1)  # Append time as feature
        x = self.conv1(x, data.edge_index).relu()
        x = self.conv2(x, data.edge_index)
        return x  # Anomaly scores or embeddings

def train_gnn(model, data, labels, epochs=10):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = torch.nn.CrossEntropyLoss()
    for epoch in range(epochs):
        model.train()
        noisy_data = add_adversarial_noise(data)  # Remedy: Adversarial robustness
        out = model(noisy_data)
        loss = criterion(out, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    return model

def analyze_threats(graph_data: Data) -> dict:
    # Hybrid: GNN for embeddings
    model = TemporalGNN(num_features=2, num_classes=2)  # Binary: threat/none
    # Mock train (use pre-trained in prod)
    labels = graph_data.y  # Assume labels in data
    model = train_gnn(model, graph_data, labels)
    embeddings = model(graph_data).detach().numpy()

    # Anomaly detection fallback
    iso_forest = IsolationForest(contamination=0.1)
    anomalies = iso_forest.fit_predict(embeddings)

    # Clustering
    clusterer = HDBSCAN(min_cluster_size=5)
    clusters = clusterer.fit_predict(embeddings)

    risk_scores = embeddings[:, 1]  # Threat prob
    return {
        "risk_scores": risk_scores.tolist(),
        "clusters": clusters.tolist(),
        "anomalies": anomalies.tolist()
    }