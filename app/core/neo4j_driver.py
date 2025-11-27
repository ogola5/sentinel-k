# app/core/neo4j_driver.py
from neo4j import GraphDatabase
from app.core.config import settings

class Neo4jDriver:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )

    def close(self):
        self.driver.close()

    def add_node(self, entity_id: str, entity_type: str, timestamp: str, features: list[float], label: str):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (n:Threat {
                    id: $id, type: $type, timestamp: $timestamp,
                    feature1: $f1, feature2: $f2, label: $label
                })
                """,
                id=entity_id, type=entity_type, timestamp=timestamp,
                f1=features[0], f2=features[1], label=label
            )

    def add_edge(self, src: str, dst: str, relation: str, timestamp: str):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (a:Threat {id: $src}), (b:Threat {id: $dst})
                CREATE (a)-[r:REL {type: $relation, timestamp: $timestamp}]->(b)
                """,
                src=src, dst=dst, relation=relation, timestamp=timestamp
            )

    def get_graph_data(self):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (n:Threat) "
                "OPTIONAL MATCH (n)-[r:REL]->(m) "
                "RETURN n, collect(r) as rels, collect(m) as targets"
            )
            records = []
            for record in result:
                n = record["n"]
                rels = record["rels"]
                targets = record["targets"]
                for r, m in zip(rels or [], targets or []):
                    records.append({"n": dict(n), "r": r, "m": dict(m) if m else None})
                if not rels:
                    records.append({"n": dict(n), "r": None, "m": None})
            return records