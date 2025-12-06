from fastapi import FastAPI
from pydantic import BaseModel
import docker
import ollama
import json

app = FastAPI()
docker_client = docker.from_env()

class ChatRequest(BaseModel):
    message: str

def list_containers():
    """Elenca tutti i container Docker"""
    containers = docker_client.containers.list(all=True)
    return [{"name": c.name, "status": c.status, "id": c.short_id} for c in containers]

def start_container(container_name: str):
    """Avvia un container Docker specifico"""
    try:
        container = docker_client.containers.get(container_name)
        container.start()
        return f"Container {container_name} avviato con successo"
    except Exception as e:
        return f"Errore: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_containers",
            "description": "Elenca tutti i container Docker disponibili nel sistema",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "start_container",
            "description": "Avvia un container Docker specifico",
            "parameters": {
                "type": "object",
                "properties": {
                    "container_name": {"type": "string", "description": "Nome del container da avviare"}
                },
                "required": ["container_name"]
            }
        }
    }
]

@app.post("/chat")
async def chat(request: ChatRequest):
    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": request.message}],
        tools=tools
    )
    
    if response["message"].get("tool_calls"):
        for tool_call in response["message"]["tool_calls"]:
            if tool_call["function"]["name"] == "list_containers":
                result = list_containers()
            elif tool_call["function"]["name"] == "start_container":
                args = tool_call["function"]["arguments"]
                result = start_container(args["container_name"])
            
            final_response = ollama.chat(
                model="llama3.1",
                messages=[
                    {"role": "user", "content": request.message},
                    response["message"],
                    {"role": "tool", "content": json.dumps(result), "name": tool_call["function"]["name"]}
                ]
            )
            return {"response": final_response["message"]["content"]}
    
    return {"response": response["message"]["content"]}
