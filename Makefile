.PHONY: all setup run test clean clean-all install setup-sys db-init list-users add-user delete-user change-password sync-users

VENV = venv
VENV_BIN = $(VENV)/bin
PYTHON = $(VENV_BIN)/python3
PIP = $(VENV_BIN)/pip
ALEMBIC = $(VENV_BIN)/alembic

# Default target
all: setup run

# Total reset and fresh install
setup: clean-all setup-sys install db-init add-admin

# System-level packages (Termux)
setup-sys:
	./scripts/setup_system.sh

# Install Python dependencies in venv
install: $(VENV)/bin/activate

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	python3 -m venv --system-site-packages $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Database initialization/migration
db-init:
	@echo "Running database migrations..."
	$(ALEMBIC) upgrade head

# Start the server
run:
	./scripts/run.sh

# Run tests
test:
	$(PYTHON) -m pytest app/tests

# User management
list-users:
	$(PYTHON) scripts/manage.py list-users

add-user:
	@if [ -z "$(user)" ]; then echo "Usage: make add-user user=<name> [perms=<r|rw|rwma|ADMIN|USER|GUEST>]"; exit 1; fi
	$(PYTHON) scripts/manage.py add-user $(user) --perms $(or $(perms),r)

add-admin:
	@USER="admin"; \
	PASS="admin_pass_a7b3c9d1e5f"; \
	echo "Adding default admin user ($$USER)..."; \
	printf "$$PASS\n$$PASS\n" | $(PYTHON) scripts/manage.py add-user $$USER --perms ADMIN

delete-user:
	@if [ -z "$(user)" ]; then echo "Usage: make delete-user user=<name>"; exit 1; fi
	$(PYTHON) scripts/manage.py delete-user $(user)

sync-users:
	$(PYTHON) scripts/manage.py sync

# Soft clean (logs and caches)
clean:
	rm -rf app/__pycache__ app/*/__pycache__ app/*/*/__pycache__
	rm -rf alembic/__pycache__
	rm -f logs/*.log storage/db/*.log
	find . -type d -name "__pycache__" -exec rm -rf {} +
	pkill -f uvicorn || true
	pkill -f copyparty || true

# Hard clean (everything including venv and DB)
clean-all: clean
	@echo "WARNING: This will delete the virtual environment and the database."
	rm -rf $(VENV)
	rm -f storage/db/server.db
	rm -f test_sync.py
