from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

class Neo4jConnector:
    def __init__(self):
        # Default to local Neo4j if .env is missing
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password") # Change this!
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_session(self):
        return self.driver.session()

# Create a singleton instance
db = Neo4jConnector()

def get_db():
    # Dependency Injection helper
    return db