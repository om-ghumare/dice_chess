# Architecture

```mermaid
flowchart LR
  subgraph Client["Flutter Client"]
    UI[Board + Lobby + Profile UI]
    WSClient[WebSocket Client]
    RESTClient[REST Client]
    LocalMode[Local Pass-and-Play]
  end

  subgraph Backend["FastAPI Backend"]
    API[REST API]
    WSHub[WebSocket Hub]
    MatchSvc[Match Orchestrator]
    MM[Matchmaking Service]
    Auth[Auth Service]
  end

  subgraph Engine["dice_chess_engine"]
    Rules[Deterministic Rules]
    Replay[Event Replay]
  end

  DB[(PostgreSQL)]
  Redis[(Redis)]

  UI --> RESTClient
  UI --> WSClient
  UI --> LocalMode
  RESTClient --> API
  WSClient --> WSHub
  API --> Auth
  API --> MM
  API --> MatchSvc
  WSHub --> MatchSvc
  MatchSvc --> Rules
  LocalMode --> Rules
  MatchSvc --> DB
  API --> DB
  MM --> Redis
  WSHub --> Redis
```

## Core principles

- Server-authoritative online game state.
- Deterministic engine as single source of truth for rule validation.
- Event log + snapshots for resync and replay.
- Shared protocol contract in `protocol.md`.
