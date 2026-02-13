# PostgreSQL Docker Configuration

Configuration files for the PostgreSQL database container.

## Directory Structure

```
postgres/
├── init/              # Initialization scripts
│   └── 01-init.sql    # Initial database setup
└── README.md
```

## Initialization Scripts

Scripts in `init/` run automatically when the PostgreSQL container starts for the first time, in alphabetical order.

### Script Naming Convention

- `01-init.sql` - Create databases and extensions
- `02-users.sql` - Create application users
- `03-permissions.sql` - Grant permissions

## Multi-Tenant Setup

For django-tenants, the public schema contains:
- Tenant registry table
- Shared lookup tables

Each tenant gets their own schema automatically.
