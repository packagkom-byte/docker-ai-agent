# Docker AI Agent

Agente AI che permette di controllare Docker attraverso linguaggio naturale usando Ollama e LLaMA 3.1.

## Struttura del Progetto

```
docker-ai-agent/
├── docker-compose.yml
├── README.md
└── agent/
    ├── Dockerfile
    └── main.py
```

## Installazione

### 1. Clona il repository
```bash
git clone https://github.com/packagkom-byte/docker-ai-agent.git
cd docker-ai-agent
```

### 2. Avvia i servizi
```bash
docker compose up -d
```

### 3. Scarica il modello LLaMA 3.1
```bash
docker exec -it ollama ollama pull llama3.1
```

## Utilizzo

### Elenca tutti i container Docker
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Mostrami tutti i container Docker"}'
```

### Avvia un container specifico
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Avvia il container chiamato postgres"}'
```

## Funzionalità

- **Linguaggio naturale italiano**: Interpreta richieste in linguaggio naturale
- **Elenca container**: Visualizza tutti i container Docker e il loro stato
- **Avvia container**: Avvia container specifici tramite nome
- **Function Calling**: Usa Ollama per selezionare automaticamente il tool appropriato
- **API REST**: Espone un'API FastAPI sulla porta 8000

## Architettura

- **Ollama**: Server LLM locale sulla porta 11434
- **Agent**: API FastAPI con accesso al socket Docker
- **LLaMA 3.1**: Modello linguistico per interpretare le richieste

## Troubleshooting

```bash
# Visualizza i log dell'agent
docker logs docker-ai-agent

# Visualizza i log di Ollama
docker logs ollama

# Riavvia i servizi
docker compose restart
```

## Requisiti

- Docker Engine
- Docker Compose
- Almeno 8GB di RAM per il modello LLaMA 3.1
