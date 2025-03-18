from fastapi import FastAPI
from pydantic import BaseModel
import networkx as nx

app = FastAPI()

class UserConnections(BaseModel):
    connections: list

@app.post("/analyze_network")
def analyze_network(data: UserConnections):
    G = nx.Graph()
    for conn in data.connections:
        G.add_edge(conn[0], conn[1])
    clustering = nx.average_clustering(G)
    return {"clustering_coefficient": clustering}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
