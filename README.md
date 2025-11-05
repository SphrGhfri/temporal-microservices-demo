# Temporal Workflow Orchestration: Python, Go & Node.js

A multi-language microservices demonstration using Temporal.io workflow orchestration. This project showcases how Temporal can coordinate activities across different programming languages (Python, Go, and Node.js) in a distributed system.

## Description

This project implements a calculation workflow that processes a number through three sequential activities, each powered by a different programming language:

1. **Power of 2** (Python) - Calculates `number²`
2. **Power of 4** (Go) - Calculates `result⁴`
3. **Power of 6** (Node.js/TypeScript) - Calculates `result⁶`

The workflow is orchestrated by Temporal, demonstrating:
- Multi-language service integration
- Asynchronous activity execution
- Fault-tolerant workflow orchestration
- RESTful API for workflow triggering

## Architecture

- **Producer Service**: FastAPI application that exposes REST endpoints to start workflows and retrieve results
- **Consumer Services**: Three independent worker services that execute activities:
  - `power_of_2_service`: Python-based activity (deployed with 2 replicas)
  - `power_of_4_service`: Go-based activity
  - `power_of_6_service`: Node.js/TypeScript-based activity
- **Temporal Server**: Workflow orchestration engine
- **PostgreSQL**: Temporal's persistence layer
- **Temporal UI**: Web interface for monitoring workflows

## Project Structure

```
temporal_test_project/
├── consumers/                      # Activity worker services
│   ├── power_of_2_python/         # Python activity service
│   │   ├── activities.py          # Power of 2 activity implementation
│   │   ├── main.py                # Worker entry point
│   │   └── Dockerfile
│   ├── power_of_4_golang/         # Go activity service
│   │   ├── activities.go          # Power of 4 activity implementation
│   │   ├── main.go                # Worker entry point
│   │   ├── go.mod
│   │   └── Dockerfile
│   └── power_of_6_nodejs/         # Node.js activity service
│       ├── src/
│       │   ├── activities.ts      # Power of 6 activity implementation
│       │   └── main.ts            # Worker entry point
│       ├── package.json
│       ├── tsconfig.json
│       └── Dockerfile
├── producers/                      # Workflow producer service
│   ├── main.py                    # FastAPI application
│   ├── workflows.py               # Workflow definition
│   └── Dockerfile
├── docker-compose.yml             # Container orchestration
├── pyproject.toml                 # Python dependencies
└── README.md
```

## Prerequisites

- Docker
- Docker Compose

## How to Run

### 1. Start All Services

```powershell
docker compose up -d
```

This command will:
- Start PostgreSQL database
- Start Temporal server
- Start Temporal UI
- Build and start all consumer services (power_of_2, power_of_4, power_of_6)
- Build and start the producer service (FastAPI)

### 2. Verify Services are Running

```powershell
docker compose ps
```

All services should show a "healthy" or "running" status.

### 3. Access the Temporal UI

Open your browser and navigate to:
```
http://localhost:8080
```

### 4. Access the API Swagger
Open your browser and navigate to:
```
http://localhost:8000/docs
```

This interface allows you to monitor workflows, view activity executions, and debug issues.

### 4. Start a Workflow

Send a POST request to the producer service:

```shell
# Using curl
curl -X POST "http://localhost:8000/?number=2"
```

The response will include a `workflow_id` that you can use to track the workflow.

### 5. Get Workflow Result

Retrieve the result using the workflow ID:

```shell
# Using curl
curl "http://localhost:8000/result/{workflow_id}"
```

## Environment Variables

Each service can be configured with environment variables defined in `docker-compose.yml`:

- `TEMPORAL_ADDRESS`: Temporal server address (default: `temporal:7233`)
- `ACTIVITY_1_WAIT_TIMEOUT`: Simulated processing time for power_of_2 activity (seconds)
- `ACTIVITY_2_WAIT_TIMEOUT`: Simulated processing time for power_of_4 activity (seconds)
- `ACTIVITY_3_WAIT_TIMEOUT`: Simulated processing time for power_of_6 activity (seconds)

## Stopping the Services

```powershell
# Stop and remove containers
docker compose down

# Stop, remove containers, and clean up volumes
docker compose down -v
```

## Development

### Rebuild Services After Code Changes

```powershell
# Rebuild and restart specific service
docker compose up -d --build power_of_2_service

# Rebuild and restart all services
docker compose up -d --build
```

### View Logs

```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f power_of_2_service
docker compose logs -f producer_service
```

## API Endpoints

### Producer Service (Port 8000)

- **POST /** - Start a new workflow
  - Query Parameter: `number` (int) - The initial number to process
  - Response: `{ "message": "workflow started", "workflow_id": "..." }`

- **GET /result/{workflow_id}** - Get workflow result
  - Path Parameter: `workflow_id` (string)
  - Response: `{ "message": "completed", "result": ... }` or error message

## Example Calculation

For input `number = 2`:
1. Power of 2: `2² = 4`
2. Power of 4: `4⁴ = 256`
3. Power of 6: `256⁶ = 281,474,976,710,656`

Final result: `281474976710656`

## Technologies Used

- **Temporal.io**: Workflow orchestration
- **Python**: Producer service (FastAPI) and power_of_2 consumer
- **Go**: power_of_4 consumer
- **Node.js/TypeScript**: power_of_6 consumer
- **Docker & Docker Compose**: Containerization
- **PostgreSQL**: Temporal persistence
- **FastAPI**: REST API framework
- **Uvicorn**: ASGI server

