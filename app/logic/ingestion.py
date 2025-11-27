from app.core.neo4j_driver import Neo4jDriver
from app.core.redis_driver import redis_driver  # <- use singleton
import pandas as pd
import io

def ingest_data(csv_path: str):
    with open(csv_path, 'r') as f:
        content = f.read()
    nodes_csv, edges_csv = content.split("\n=== EDGES ===\n")

    df_nodes = pd.read_csv(io.StringIO(nodes_csv.replace("=== NODES ===\n", "")))
    df_edges = pd.read_csv(io.StringIO(edges_csv))

    neo4j = Neo4jDriver()
    for _, row in df_nodes.iterrows():
        features = [row['feature1'], row['feature2']]
        neo4j.add_node(row['entity_id'], row['type'], row['timestamp'], features, row['label'])

    for _, row in df_edges.iterrows():
        neo4j.add_edge(row['src'], row['dst'], row['relation'], row['timestamp'])

    # Use singleton redis_driver
    for _, row in df_edges.iterrows():  # Simulate stream with edges
        redis_driver.add_to_stream('threat_stream', row.to_dict())

    neo4j.close()
