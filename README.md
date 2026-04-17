# Service Monitor API

An asynchronous API for monitoring availability and latency of external services, designed with a strong focus on clean architecture, observability, and scalability.

## Tech Stack

- **Linguagem:** Python 3.12
- **Framework:** FastAPI (Async)
- **Persistência:** SQLAlchemy + SQLite
- **Validação:** Pydantic (DTO Pattern)
- **DevOps:** Docker & Docker Compose
- **Package Management:** uv

---

## Architecture Overview

The project follows **Clean Architecture** principles with strict separation of concerns between layers:

- **API Layer (`api/`)**: Handles HTTP requests, routing, and dependency injection.
- **Schemas / DTOs (`schemas/`)**: Defines input/output contracts using Pydantic, isolating external data representation from internal models.
- **Service Layer (`services/`)**: Contains business logic and orchestration of operations.
- **Repository Layer (`repositories/`)**: Encapsulates database access and query logic.
- **Models (`models/`)**: SQLAlchemy ORM definitions representing database structure.
- **Core (`core/`)**: Infrastructure setup such as database connection and engine configuration.
- **Clients (`services/http_checker.py`)**: External integrations isolated for testability and resilience.

---

## Architecture Diagram

```mermaid
flowchart TD
    Client[HTTP Client] --> API[API Layer]

    API --> DTO[DTO / Schemas]
    API --> Service[Service Layer]

    Service --> Repo[Repository Layer]
    Service --> External[HTTP Client / External Services]

    Repo --> Model[ORM Models]
    Model --> DB[(SQLite Database)]

    style API fill:#dbeafe,stroke:#93c5fd
    style Service fill:#dcfce7,stroke:#86efac
    style Repo fill:#ede9fe,stroke:#c4b5fd
    style Model fill:#fce7f3,stroke:#f9a8d4