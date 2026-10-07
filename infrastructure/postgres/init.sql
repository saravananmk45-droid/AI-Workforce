-- ==============================================================================
-- AI WORKFORCE PLATFORM — POSTGRESQL 16 SYSTEM INITIALIZATION
-- Zero Mock Business Data — Pure Infrastructure & Extensions
-- ==============================================================================

-- Enable required cryptographic and UUID extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- Create dedicated schemas
CREATE SCHEMA IF NOT EXISTS audit;

-- Set up multi-tenant RLS session variable helper function
CREATE OR REPLACE FUNCTION current_app_org_id() 
RETURNS uuid AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_organization_id', true), '')::uuid;
EXCEPTION
    WHEN OTHERS THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

COMMENT ON FUNCTION current_app_org_id() IS 'Extracts active tenant organization UUID from session context for RLS evaluation';
