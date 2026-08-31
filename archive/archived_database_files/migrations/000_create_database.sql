-- Run once as a MySQL account allowed to create databases.
-- The application connection values in .env expect this database name.

CREATE DATABASE IF NOT EXISTS moffat_bay
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

