--- 1)создаем базы данных ---
CREATE DATABASE auth_db;
CREATE DATABASE profile_db;

--- 2)создаем роль для kong for gateway ---
CREATE ROLE kong WITH LOGIN PASSWORD 'kong';

CREATE DATABASE kong_DB OWNER kong;

\connect kong_db


-- 3) даю права на существующие объекты в public
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO kong;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO kong;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO kong;

-- 4) делаю так, чтобы все будущие объекты в public автоматически доставались kong
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kong;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kong;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO kong;