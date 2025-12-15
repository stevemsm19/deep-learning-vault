# Deep Learning Vault

The required *Python* version for this project is *3.12.x.*

## About me

Hello, my name is *Oscar*, I am 26 years old, and I am from Bogotá, Colombia. My experience in the world of software development is what I acquired during my time at university. This degree has been quite challenging for me because I also work at Airbnb in customer service, which is why I speak Portuguese and have an intermediate level of English. The reason I chose this career is because I love automating processes and really enjoy analyzing data on a small scale. I'm not the best at math, but I believe that with practice and study, anything is possible.

## Setup environment

As usual setup your virtual environment:

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip setuptools
$ pip install -r requirements-dev.txt
$ pip install -e .
```

> Or you can use `make setup` if you have a Linux environment and then `source venv/bin/activate` to activate the virtual environment.

## Basic code compliance

```bash
$ black .
All done! ✨ 🍰 ✨
X files left unchanged.
$ mypy .
Success: no issues found in X source files
```

## About the CI/CD pipeline

This `monorepo` comes with a pre-configured CI/CD pipeline that is triggered every time a push is made to a **merge request** or when a **merge request** is integrated into the **main** branch.

The pipeline is configured to:

* Execute **code compliance** checks.
* Generate documentation.

> You may add more stages or jobs to the pipeline, but make sure you **do not remove the existing ones**. In addition, make sure you do your best to **keep the pipeline green** at all times.

## Environment Variables (.env)

This project requires environment variables to be configured before running the application.

You must create a `.env` file at the root of the project based on the provided `.env.example` file.

Copy the example file:

```bash
cp .env.example .env
```

## Running the App

You can run the application in **two different ways**:

1. **Running services individually (local development)**
2. **Running everything with Docker Compose (recommended)**

Before starting, remember to complete the **Setup environment** step if you are going to run the application locally.

### Option 1: Running services individually

In this mode, the **backend**, **frontend**, and **ChromaDB** are started separately. This approach is useful for local development and debugging.

#### Required service: ChromaDB

This project uses **ChromaDB** as a vector database. When running services individually, you must start ChromaDB first.

**Windows**

```bash
docker run -d \
  --name chromadb \
  -p 8000:8000 \
  -v chroma_data:/chroma/chroma \
  chromadb/chroma
```

**Linux**

```bash
make chroma
```

#### Running the Backend

**Windows**

```bash
uvicorn src.app.backend.main:app
```

**Linux**

```bash
make backend
```

Once the backend is running, you can access it at:

* **Backend Server:** [http://localhost:8001](http://localhost:8001)

##### API Documentation

* Swagger UI: [http://localhost:8001/docs](http://localhost:8001/docs)
* ReDoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

#### Running the Frontend

**Windows**

```bash
streamlit run ./src/app/frontend/Finai_Bot.py
```

**Linux**

```bash
make frontend
```

Once the frontend is running, you can access it at:

* **Frontend:** [http://localhost:8501](http://localhost:8501)

### Option 2: Running everything with Docker Compose (recommended)

As an alternative, you can run the complete application using Docker Compose. This will automatically start **ChromaDB**, the **backend**, and the **frontend**.

```bash
docker compose up -d
```

Or, if you are on Linux:

```bash
make docker
```

Once the containers are running, access the application at:

* [http://localhost:8501/](http://localhost:8501/)

### Deployed Application

The application is currently running temporarily at:

* [https://deeplearning-oscar-munoz.streamlit.app/](https://deeplearning-oscar-munoz.streamlit.app/)

## Some technical details

- The project follows a **monorepo** structure, including both backend and frontend.
- An **MCP server** is used to manage and orchestrate interactions between components and AI-related services.
- The application integrates a **pre-trained YOLO model**, adapted to the project’s domain-specific dataset.
- The model is used for the detection of Colombian banknotes, leveraging transfer learning to reduce training time and computational cost.
- The **backend** is built with **FastAPI**, exposing REST endpoints and API documentation.
- The **frontend** is implemented using **Streamlit**, providing an interactive interface for model interaction.
- Docker and Docker Compose are used to simplify development and deployment.

## Project Architecture

This project follows a **clean, modular, and layered architecture**, organized as a **monorepo** that contains the backend, frontend, and MCP components in a single repository. The goal is to ensure **separation of concerns**, **scalability**, and **maintainability**.

### High-level structure

```
src
├── app
│   ├── backend        # FastAPI backend (API, business logic, persistence)
│   ├── frontend       # Streamlit frontend (UI and client-side logic)
│   └── mcp            # MCP client and server for AI orchestration
```

### Backend Architecture (FastAPI)

The backend follows a **layered / clean architecture approach**, where responsibilities are clearly separated:

```
src/app/backend
├── application
│   ├── schemas        # Request/response DTOs (Pydantic models)
│   ├── services       # Application use cases and business workflows
│   └── controllers    # FastAPI routers (API endpoints)
├── domain
│   ├── entities       # Core business entities
│   ├── interfaces    # Abstract interfaces (ports)
│   └── repositories  # Repository contracts
├── infrastructure
│   ├── persistence   # Database / vector store implementations (e.g. ChromaDB)
│   └── services      # External services (AI, file storage, etc.)
├── config             # Dependency injection, settings, environment config
├── utils              # Shared helpers and utilities
└── main.py            # FastAPI app entry point
```

### Frontend Architecture (Streamlit)

The frontend is built using **Streamlit**, structured by **features** to keep UI logic modular and easy to evolve.

```
src/app/frontend
├── streamlit
│   ├── config         # UI and app configuration
│   ├── features       # Feature-based UI components (chat, sidebar, state)
│   └── pages          # Streamlit pages
├── services
│   └── api_service.py # HTTP client for backend communication
├── utils              # Session state and shared utilities
└── Final_Bot.py       # Streamlit app entry point
```
### MCP (Model Context Protocol)

The `mcp` module handles communication between the backend and AI-related tooling using the **Model Context Protocol**.

```
src/app/mcp
├── mcp_client         # Client used by the backend to interact with MCP
└── mcp_server         # MCP server exposing tools and capabilities
```
