# FastAPI Simple Order Microservice

This repository contains a FastAPI microservice built strictly using Test-Driven Development (TDD) and Clean Architecture principles. It focuses on asynchronous execution, robust dependency injection, and centralized logging, adhering strictly to SOLID design principles.

## Features

- **Asynchronous Execution**: Fully utilizes Python's `async`/`await` across HTTP handlers, business logic, external client calls (using `httpx`), and data persistence.
- **Clean Architecture**: Separated into distinct layers (`domain`, `services`, `infrastructure`, `api`, `core`) to decouple business logic from framework specifics and data storage.
- **Dependency Injection**: Leverages FastAPI's powerful `Depends` system combined with Python `Protocol`s to achieve true Dependency Inversion, making components highly testable and loosely coupled.
- **Strict TDD**: Built exclusively through the Red-Green-Refactor cycle ensuring 100% test coverage and deliberate design choices.
- **Centralized Logging**: Standard Python logging configured gracefully to prevent multiple handler attachment and output structured console logs.

## Getting Started

### Prerequisites

- Python 3.10+
- `pip`

### Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install the project along with its development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

Run the fully-asynchronous test suite using `pytest`:
```bash
pytest
```

### Starting the Server

Start the application locally using `uvicorn`:
```bash
uvicorn app.main:app --reload
```
You can then access the Swagger UI documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
