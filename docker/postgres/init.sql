-- ==================================================
-- LankaCommerce Cloud - PostgreSQL Initialization
-- ==================================================
-- Purpose: Initialize databases, user, and extensions
-- Runs: On first container startup only
-- Databases: lankacommerce, lankacommerce_test
-- ==================================================

-- Create main database
CREATE DATABASE lankacommerce
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;

-- Create test database
CREATE DATABASE lankacommerce_test
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;

-- Create application user
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'lcc_user') THEN
        CREATE USER lcc_user WITH PASSWORD 'dev_password_change_me';
    END IF;
END
$$;

-- Grant database permissions
GRANT ALL PRIVILEGES ON DATABASE lankacommerce TO lcc_user;
GRANT ALL PRIVILEGES ON DATABASE lankacommerce_test TO lcc_user;

-- Main database setup
\connect lankacommerce

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";

GRANT ALL ON SCHEMA public TO lcc_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lcc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lcc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lcc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lcc_user;

-- Test database setup
\connect lankacommerce_test

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";

GRANT ALL ON SCHEMA public TO lcc_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO lcc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO lcc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO lcc_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO lcc_user;
