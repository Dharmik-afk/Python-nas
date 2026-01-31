.PHONY: all setup run test clean clean-all install setup-sys db-init list-users add-user delete-user change-password sync-users set-debug

VENV = .venv
VENV_BIN = $(VENV)/bin
PYTHON = uv run python3
ALEMBIC = uv run alembic

# Default target
all: setup run

# Total reset and fresh install
setup: clean-all setup-sys install db-init add-admin

# System-level packages (Termux)
setup-sys:
	./scripts/setup_system.sh

# Install Python dependencies in venv
install:
	@echo "Initializing environment and dependencies with uv..."
	uv venv --system-site-packages $(VENV)
	uv sync

# Database initialization/migration
db-init:
	@echo "Running database migrations..."
	$(ALEMBIC) upgrade head

# Start the server
run:
	./scripts/run.sh

# Run with custom serve directory
# Usage: make run-custom dir=/path/to/media
run-custom:
	@if [ -z "$(dir)" ]; then echo "Usage: make run-custom dir=<path>"; exit 1; fi
	CUSTOM_SERVE_DIR="$(dir)" ./scripts/run.sh

# Set persistent serve directory in .env
# Usage: make set-dir dir=/path/to/media
set-dir:
	@if [ -z "$(dir)" ]; then echo "Usage: make set-dir dir=<path>"; exit 1; fi
	@sed -i 's|^CUSTOM_SERVE_DIR=.*|CUSTOM_SERVE_DIR=$(dir)|' .env || echo "CUSTOM_SERVE_DIR=$(dir)" >> .env
	@echo "Updated .env with CUSTOM_SERVE_DIR=$(dir)"

# Set debug mode in .env
# Usage: make set-debug debug=<True|False>
set-debug:
	@if [ -z "$(debug)" ]; then echo "Usage: make set-debug debug=<True|False>"; exit 1; fi
	@grep -q "^DEBUG=" .env && sed -i 's|^DEBUG=.*|DEBUG=$(debug)|' .env || echo "DEBUG=$(debug)" >> .env
	@echo "Updated .env with DEBUG=$(debug)"
	echo "setting stream directory to default (storage/files/)"
	CUSTOM_SERVE_DIR=
# Run tests
test:
	PYTHONPATH=. uv run pytest app/tests

# User management
list-users:
	uv run python3 scripts/manage.py list-users

add-user:
	@if [ -z "$(user)" ]; then echo "Usage: make add-user user=<name> [perms=<r|rw|rwma|ADMIN|USER|GUEST>]"; exit 1; fi
	uv run python3 scripts/manage.py add-user $(user) --perms $(or $(perms),r)

add-admin:
	@USER="admin"; \
	PASS="admin_pass_a7b3c9d1e5f"; \
	echo "Adding default admin user ($$USER)..."; \
	printf "$$PASS\n$$PASS\n" | uv run python3 scripts/manage.py add-user $$USER --perms ADMIN

delete-user:
	@if [ -z "$(user)" ]; then echo "Usage: make delete-user user=<name>"; exit 1; fi
	uv run python3 scripts/manage.py delete-user $(user)

change-password:
	@if [ -z "$(user)" ]; then echo "Usage: make change-password user=<name>"; exit 1; fi
	uv run python3 scripts/manage.py change-password $(user)

sync-users:
	uv run python3 scripts/manage.py sync

# Soft clean (logs and caches)
clean:
	rm -rf app/__pycache__ app/*/__pycache__ app/*/*/__pycache__
	rm -rf alembic/__pycache__
	rm -f logs/*.log storage/db/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} +
	-pkill -f "supervisor/supervisor.py"
	-pkill -f "app.main:app"
	-pkill -f "copyparty"

clean-log:
	 rm -f logs/*.log storage/db/*.log
# Hard clean (everything including venv and DB)
clean-all: clean
	@echo "WARNING: This will delete the virtual environment and the database."
	rm -rf $(VENV)
	rm -f storage/db/server.db
	rm -f test_sync.py
