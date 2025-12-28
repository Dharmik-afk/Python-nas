# Python FastAPI File Server

A lightweight, extendable Python-based file server designed for private network use. This server uses FastAPI as its web framework and is designed to be a frontend for the `copyparty` file-serving engine.

## Documentation

- [User Manual](manuals/USER_MANUAL.md): Guide for browsing, downloading, and using the media gallery.
- [Administrator Manual](manuals/ADMIN_MANUAL.md): Guide for server configuration, user management, and maintenance.

## New Architecture

The server has been refactored to a modern Python web application structure:

- **Backend**: A [FastAPI](https://fastapi.tiangolo.com/) application located in the `backend/` directory. It handles routing, logic, and serves HTML templates.
- **Database**: Uses [SQLAlchemy](https://www.sqlalchemy.org/) with a SQLite backend for data persistence (users, metadata, etc.). Database migrations are managed by [Alembic](https://alembic.sqlalchemy.org/).
- **Frontend**: The UI is rendered server-side using [Jinja2](https://jinja.palletsprojects.com/) templates. It is enhanced with [htmx](https://htmx.org/) to provide a dynamic, single-page application feel without the complexity of a full JavaScript framework.

## Setup and Installation

1.  **Initialize and Verify**: Use the Makefile to install all dependencies and run health checks.
    ```bash
    make setup
    ```

## Running the Server

Start the server using the Makefile (which uses `run.sh` under the hood). By default, it serves the `~/projects` directory.

```bash
make run
```

Or run the script directly with a custom directory:
```bash
./run.sh --dir /path/to/your/folder
```

The server will be available at `http://<your-ip>:8000`. Both the FastAPI frontend and the `copyparty` backend are started and managed automatically.

## Maintenance

- **Tests**: `make test`
- **Stats**: `make stats` (view real-time server metrics)
- **Clean**: `make clean` (remove logs and stop running servers)
# Python-nas
