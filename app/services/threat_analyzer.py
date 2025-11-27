# app/services/threat_analyzer.py
from app.logic.algorithms import analyze_threats
from app.core.neo4j_driver import Neo4jDriver
from torch_geometric.data import Data
import torch
import numpy as np

class ThreatAnalyzer:
    def load_graph(self):
        neo4j = Neo4jDriver()
        raw = neo4j.get_graph_data()
        neo4j.close()

        if not raw:
            x = torch.tensor([[0.5, 0.5]], dtype=torch.float)
            edge_index = torch.tensor([[0, 0]], dtype=torch.long).t()
            time = torch.tensor([1.0])
            labels = torch.tensor([0])
            return Data(x=x, edge_index=edge_index, time=time, y=labels)

        node_map = {}
        x_list = []
        time_list = []
        label_list = []

        for item in raw:
            n = item["n"]
            if n["id"] not in node_map:
                idx = len(node_map)
                node_map[n["id"]] = idx
                x_list.append([n.get("feature1", 0.5), n.get("feature2", 0.5)])
                ts = n.get("timestamp", "2025-01-01")
                time_list.append(np.datetime64(ts).astype('datetime64[s]').astype(float))
                label = n.get("label", "None")
                label_list.append(1 if label != "None" else 0)

        x = torch.tensor(x_list, dtype=torch.float)
        time = torch.tensor(time_list, dtype=torch.float)
        y = torch.tensor(label_list, dtype=torch.long)  # <-- THIS WAS MISSING

        edge_list = []
        for item in raw:
            r = item["r"]
            if r:
                src_id = r.start_node.element_id.split(":")[-1]
                dst_id = r.end_node.element_id.split(":")[-1]
                src = node_map.get(src_id)
                dst = node_map.get(dst_id)
                if src is not None and dst is not None:
                    edge_list.append([src, dst])

        if not edge_list:
            edge_list = [[0, 0]]

        edge_index = torch.tensor(edge_list, dtype=torch.long).t().contiguous()

        return Data(x=x, edge_index=edge_index, time=time, y=y)

    def analyze(self, data: Data) -> dict:
        return analyze_threats(data)