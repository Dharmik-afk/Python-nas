# Security & Jail Confinement Context

## Jail Root
- **Configuration**: Managed via `CUSTOM_SERVE_DIR` in `.env`.
- **Default**: `storage/files`.
- **Invariant**: All file operations MUST be confined to this directory.

## Confinement Rules
- **Path Validation**: Strict validation ensures no access outside the jail.
- **Blocked Paths**: Critical system paths (`/usr`, `/etc`) and the Project Root are explicitly blocked.
- **Traversal Prevention**: `..` path components must be sanitized or rejected.

## Obfuscation
- **Response**: Restricted paths MUST return `404 Not Found` to prevent directory enumeration/discovery.

## Session Management
- **Persistence**: User sessions are persisted in `storage/db/sessions.json` to survive restarts.
