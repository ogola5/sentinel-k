import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

# Generate 100 nodes (Kenyan threat-inspired: IPs, users, etc.)
node_types = ['IP', 'User', 'Domain', 'Transaction', 'Device']
threat_labels = ['None', 'Phishing', 'Ransomware', 'SIM_Swap', 'Fraud', 'Malware']
num_nodes = 100

nodes_data = {
    'entity_id': [f'ent_{i:04d}' for i in range(num_nodes)],
    'type': [random.choice(node_types) for _ in range(num_nodes)],
    'timestamp': [(datetime.now() - timedelta(days=random.randint(0, 30))).isoformat() for _ in range(num_nodes)],
    'feature1': np.random.uniform(0, 1, num_nodes).tolist(),
    'feature2': np.random.uniform(0, 1, num_nodes).tolist(),
    'label': [random.choice(threat_labels) for _ in range(num_nodes)]
}
df_nodes = pd.DataFrame(nodes_data)

# Generate 200 edges
edge_relations = ['CONNECTED_TO', 'PHISHED', 'TRANSFERRED', 'INFECTED', 'ACCESSED']
num_edges = 200

edges_data = {
    'src': [random.choice(df_nodes['entity_id']) for _ in range(num_edges)],
    'dst': [random.choice(df_nodes['entity_id']) for _ in range(num_edges)],
    'relation': [random.choice(edge_relations) for _ in range(num_edges)],
    'timestamp': [(datetime.now() - timedelta(days=random.randint(0, 30))).isoformat() for _ in range(num_edges)]
}
df_edges = pd.DataFrame(edges_data)

# Save in the required format (string with separators)
with open('data/synthetic_kenya.csv', 'w') as f:
    f.write("=== NODES ===\n")
    df_nodes.to_csv(f, index=False, lineterminator='\n')
    f.write("\n=== EDGES ===\n")
    df_edges.to_csv(f, index=False, lineterminator='\n')

print("File created at data/synthetic_kenya.csv")