# Internet Support Agent

An AI-assisted internet troubleshooting system designed to help users
diagnose connectivity problems through a structured support workflow.

The project separates the application logic, user-facing frontend, and
automated tests so that troubleshooting behavior can be developed and
verified independently.

## Overview

Internet connectivity problems are often reported with very general
messages such as:

-   "My internet is not working."
-   "Wi-Fi is connected but nothing loads."
-   "The connection keeps dropping."
-   "I cannot access websites."

The same symptom can have different causes. The purpose of this project
is to provide a structured way to handle these cases instead of relying
on a single generic troubleshooting response.

The repository currently contains three primary areas:

``` text
Internet-support-agent/
├── app/
├── frontend/
├── tests/
├── .env.example
├── conftest.py
├── requirements.txt
└── .gitignore
```

## Key Goals

-   Provide a structured internet-support workflow.
-   Maintain application state while troubleshooting an issue.
-   Separate backend logic from the frontend interface.
-   Keep configuration outside the source code through environment
    variables.
-   Provide automated tests for the application.
-   Support an architecture that can be extended with AI-based diagnosis
    and historical troubleshooting memory.

## Architecture

The project is organized around three main layers:

``` text
┌──────────────────────────────┐
│          Frontend            │
│     User Support Interface   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Application         │
│   API + Troubleshooting      │
│        Business Logic        │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│   Database   │  │ AI / Memory  │
│    State     │  │ Integrations │
└──────────────┘  └──────────────┘
```

The application layer is responsible for controlling the troubleshooting
flow, while external AI or memory services can be used as supporting
components rather than replacing the application's state management.

## Technology Stack

The repository currently declares the following core Python
dependencies:

  Technology          Purpose
  ------------------- ----------------------------------------------
  FastAPI             Backend API framework
  Uvicorn             ASGI application server
  SQLAlchemy          Database ORM and persistence layer
  Pydantic            Data validation and typed application models
  Pydantic Settings   Environment-based configuration
  python-dotenv       Loading environment variables
  Requests            HTTP communication
  Pytest              Automated testing

These dependencies are listed in the repository's `requirements.txt`.
citeturn1view3

## Configuration

The repository provides an `.env.example` file with placeholders for the
main runtime configuration:

``` env
GROK_API_KEY=
HINDSIGHT_API_KEY=
DATABASE_URL=sqlite:///./support_agent.db
DEBUG=True
```

The example configuration shows that the project can use a Grok API key,
Hindsight API key, a SQLite database URL, and a debug setting.
citeturn4view0

Create a local environment file before running the application:

``` bash
cp .env.example .env
```

Then fill in the required credentials.

> Never commit real API keys or other secrets to the repository.

The repository's `.gitignore` already excludes `.env`, database files,
logs, Python cache files, virtual environments, and common editor files.
citeturn4view1

## Installation

Clone the repository and enter the project directory:

``` bash
git clone https://github.com/Komerishetty-Revanth/Internet-support-agent.git
cd Internet-support-agent
```

Create a Python virtual environment:

``` bash
python -m venv venv
```

Activate it on Windows:

``` bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

``` bash
source venv/bin/activate
```

Install the project dependencies:

``` bash
pip install -r requirements.txt
```

## Running the Application

The repository uses FastAPI with Uvicorn, so the backend can be served
through an ASGI entry point inside the `app` package.

A typical development command is:

``` bash
uvicorn app.main:app --reload
```

If the application's entry module uses a different filename or object
name, use the corresponding entry point defined in the `app` package.

After starting the server, the FastAPI documentation is normally
available at:

``` text
http://127.0.0.1:8000/docs
```

## Frontend

The repository includes a separate `frontend/` directory.

Its role is to provide the user-facing support experience while the
application layer handles the backend workflow.

``` text
User
 │
 ▼
Frontend
 │
 │ HTTP request
 ▼
FastAPI Application
 │
 ├── Troubleshooting logic
 ├── Database state
 └── AI / memory integrations
 │
 ▼
Response
 │
 ▼
Frontend
```

The exact frontend start command should be taken from the files inside
`frontend/`, since the repository page exposes the directory but does
not currently expose its internal files through the public page crawler.
citeturn0view0

## Troubleshooting Workflow

A typical support interaction can follow this sequence:

``` text
User reports connectivity issue
            │
            ▼
      Classify the issue
            │
            ▼
   Check current session state
            │
            ▼
     Run diagnostic checks
            │
       ┌────┴────┐
       │         │
    Resolved   Unresolved
       │         │
       ▼         ▼
   Complete   Continue or
    session   escalate
```

The important architectural principle is to keep workflow progression
deterministic. AI-generated language can assist with interpretation, but
application state should control what happens next.

## AI and Memory Integration

The environment configuration indicates two external AI-oriented
credentials:

-   `GROK_API_KEY`
-   `HINDSIGHT_API_KEY`

The intended architecture can use these services for language-based
support and historical troubleshooting context.

A simplified interaction looks like:

``` text
Current user symptom
        │
        ▼
Issue interpretation
        │
        ▼
Relevant historical context
        │
        ▼
Diagnostic action
        │
        ▼
Current result
        │
        ├── Resolved → store useful outcome
        │
        └── Not resolved → next diagnostic stage
```

Historical information should be treated as supporting evidence. Current
diagnostic observations should remain the basis for deciding whether a
previous resolution applies.

## Database

The provided environment example uses SQLite by default:

``` env
DATABASE_URL=sqlite:///./support_agent.db
```

SQLAlchemy is included in the project's dependency list, providing the
database abstraction layer. citeturn1view3

The database can be used to persist application state such as:

-   Support sessions
-   Diagnostic progress
-   Issue information
-   Conversation context
-   Resolution information

The exact models and relationships should be referenced directly from
the `app/` implementation.

## Testing

The repository includes a dedicated `tests/` directory and Pytest is
listed as a dependency. citeturn0view0turn1view3

Run the test suite with:

``` bash
pytest
```

The repository also contains `conftest.py`, which adds the project root
to Python's import path for tests. citeturn4view2

A useful development cycle is:

``` text
Implement
   ↓
Run tests
   ↓
Fix failures
   ↓
Run tests again
   ↓
Verify API behavior
```

## Project Structure

``` text
Internet-support-agent/
│
├── app/
│   └── Backend application and troubleshooting logic
│
├── frontend/
│   └── User-facing support interface
│
├── tests/
│   └── Automated application tests
│
├── .env.example
│   └── Environment configuration template
│
├── conftest.py
│   └── Pytest configuration
│
├── requirements.txt
│   └── Python dependencies
│
└── .gitignore
    └── Local files and secrets excluded from Git
```

## Security Notes

Keep credentials outside the repository.

The example environment file contains empty placeholders rather than
real credentials, and the repository's ignore rules exclude `.env` and
other local runtime artifacts. citeturn4view0turn4view1

Recommended practice:

``` text
.env
  ↓
Local development only

.env.example
  ↓
Safe configuration template

GitHub
  ↓
Source code without secrets
```

## Future Improvements

Potential areas for extending the system include:

-   More detailed network issue classification.
-   Additional diagnostic checks.
-   Stronger session and escalation handling.
-   More historical resolution retrieval.
-   Better frontend feedback during diagnosis.
-   Expanded automated test coverage.
-   Production database configuration.
-   Monitoring and structured diagnostic logging.
-   Deployment configuration for hosted environments.

## Development Principles

The project can be developed around a few core principles:

1.  **Keep state explicit** --- troubleshooting progress should be
    controlled by the application.
2.  **Use AI as a supporting layer** --- generated responses should
    operate within defined application boundaries.
3.  **Validate current evidence** --- historical solutions should not
    automatically override present network conditions.
4.  **Test the workflow** --- changes to diagnostic logic should be
    covered by automated tests.
5.  **Protect credentials** --- API keys and local database files should
    remain outside source control.

## Repository

**GitHub:**
https://github.com/Komerishetty-Revanth/Internet-support-agent

## License

No license file is currently visible in the repository root. Add an
appropriate license before distributing the project publicly under
specific open-source terms. \`\`\`

# Summary

Internet Support Agent provides a foundation for an AI-assisted
connectivity troubleshooting application, combining a FastAPI-based
application layer, persistent state, a separate frontend, automated
testing, and configurable AI/memory integrations.

The repository is structured so that the troubleshooting workflow can
evolve without coupling the user interface directly to the diagnostic
implementation.
